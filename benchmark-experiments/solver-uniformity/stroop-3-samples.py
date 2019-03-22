import operator as op
import json

from datetime import datetime

from sweetpea.blocks import Block
from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Window
from sweetpea.constraints import AtMostKInARow
from sweetpea.metrics import collect_design_metrics
from sweetpea import fully_cross_block, __generate_cnf

# Generate all the blocks, and store them in a hash.
blocks = {}

color_list = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
def __build_stroop_block(color_count):
    color = Factor("color", color_list[:color_count])
    text = Factor("text", color_list[:color_count])

    congruent = Factor("congruent?", [
        DerivedLevel("yes", WithinTrial(op.eq, [color, text])),
        DerivedLevel("no",  WithinTrial(op.ne, [color, text]))
    ])

    constraints = [AtMostKInARow(1, ("congruent?", "yes"))]

    return fully_cross_block([color, text, congruent], [color, text], constraints)

block = __build_stroop_block(3)

solutions = {}

from sweetpea.server import submit_job, get_job_result

# 100 loops of 100 samples = 10,000 total
for n in range(100):
    backend_request = block.build_backend_request()
    json_data = {
        'action': 'SampleNonUniform',
        'sampleCount': 100,
        'support': block.variables_per_sample(),
        'fresh': backend_request.fresh - 1,
        'cnfs': backend_request.get_cnfs_as_json(),
        'requests': backend_request.get_requests_as_json()
    }

    job_id = submit_job(json_data)
    job_result_str = get_job_result(job_id)

    solutions_obj = json.loads(job_result_str)['solutions']
    assignments = list(map(lambda s: s['assignment'], solutions_obj))
    for a in assignments:
        if str(a) in solutions:
            solutions[str(a)] += 1
        else:
            solutions[str(a)] = 1

with open('solutions.json', 'w') as f:
    f.write(json.dumps(solutions))
