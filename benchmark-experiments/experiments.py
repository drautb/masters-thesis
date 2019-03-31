import operator as op
import json

from datetime import datetime

from sweetpea.blocks import Block
from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Window
from sweetpea.constraints import AtMostKInARow, ExactlyKInARow
from sweetpea.metrics import collect_design_metrics
from sweetpea import fully_cross_block, __generate_cnf

# Generate all the blocks, and store them in a hash.
blocks = {}

color_list = ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
def __build_stroop_block(color_count):
    color = Factor("color", color_list[:color_count])
    text = Factor("text", color_list[:color_count])

    congruent = Factor("congruent?", [
        DerivedLevel("yes", WithinTrial(op.eq, [color, text])),
        DerivedLevel("no",  WithinTrial(op.ne, [color, text]))
    ])

    constraints = [AtMostKInARow(1, ("congruent?", "yes"))]

    return fully_cross_block([color, text, congruent], [color, text], constraints)

for n in range(2, 21):
    blocks["stroop-" + str(n)] = __build_stroop_block(n)


# GENERATE METRICS, CNF FOR EACH BLOCK
# for name, block in blocks.items():

#     # Save metrics
#     metrics = collect_design_metrics(block)
#     with open('metrics/' + name + '.json', 'w') as f:
#         f.write(json.dumps(metrics))

#     # Save CNFs
#     t_start = datetime.now()
#     cnf_str = __generate_cnf(block)
#     t_end = datetime.now()
#     seconds_elapsed = str((t_end - t_start).seconds) + "s"
#     cnf_str = "c Generated in " + seconds_elapsed + "\n" + cnf_str

#     with open('cnfs/' + name + '.cnf', 'w') as f:
#         f.write(cnf_str)

from sweetpea.sampling_strategies.uniform_combinatoric import UniformCombinatoricSamplingStrategy

def sample():
    sampling_result = UniformCombinatoricSamplingStrategy.sample(blocks['stroop-20'], 10000)
    from pprint import pprint
    pprint(sampling_result.metrics['avg_rejected'])

import timeit
result = timeit.timeit("sample()", setup="from __main__ import sample", number=1)

print(result)


