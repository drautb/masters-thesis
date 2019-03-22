from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Window
from sweetpea.constraints import Exclude
from sweetpea import fully_cross_block, synthesize_trials_non_uniform, print_experiments


"""
Task Switching Paradigm
******************************
factors (levels):
- current task (1, 2, 3)
- task transition (A-B-A, A-B-C): factor dependent on task.
- congruency (congruent, incongruent): factor dependent on color and word.
- correct response (up, down, left right): factor dependent on color, word and task.
- response transition (repetition, switch). factor dependent on response:

constraints:
- counterbalancing color x word x correct response
- no more than 7 response repetitions in a row
- no more than 7 response switches in a row

original experiment:
- Assignment of deviants to object locations and assignment of dimensional values occurred randomly.
- Successive relevant dimensions were selected in a random manner with the constraint that no immediate repetitions of dimensions could occur.

"""

# DEFINE STIMULUS FACTORS

deviantColor             = Factor("deviant color",  ["pink", "purple"])
deviantOrientation       = Factor("deviant orientation", ["left", "right"])
deviantMovement          = Factor("deviant movement", ["vertical", "horizontal"])

deviantColorObject          = Factor("color deviant", ["object 1", "object 2", "object 3", "object 4"])
deviantOrientationObject    = Factor("orientation deviant", ["object 1", "object 2", "object 3", "object 4"])
deviantMovementObject       = Factor("movement deviant", ["object 1", "object 2", "object 3", "object 4"])


def legalObjectConfiguration(deviantColorObject, deviantOrientationObject, deviantMovementObject):
    return (deviantColorObject != deviantOrientationObject) and (deviantColorObject != deviantMovementObject) and (deviantOrientationObject != deviantMovementObject)

def illegalObjectConfiguration(deviantColorObject, deviantOrientationObject, deviantMovementObject):
    return not legalObjectConfiguration(deviantColorObject, deviantOrientationObject, deviantMovementObject)

illegalLevel = DerivedLevel("illegal", WithinTrial(illegalObjectConfiguration,   [deviantColorObject, deviantOrientationObject, deviantMovementObject]))
legalLevel = DerivedLevel("legal", WithinTrial(legalObjectConfiguration,   [deviantColorObject, deviantOrientationObject, deviantMovementObject]))

objectConfiguration = Factor("object configuration", [
    illegalLevel,
    legalLevel
])

# DEFINE TASK AND TASK TRANSITION

task              = Factor("task", ["color task", "movement task", "orientation task"])

def A_B_A(tasks):
    return (tasks[0] == tasks[2]) and (tasks[0] != tasks[1])

def A_B_C(tasks):
    return (tasks[0] != tasks[2]) and (tasks[0] != tasks[1]) and (tasks[1] != tasks[2])

def other_transition(tasks):
    return (not(A_B_A(tasks) or A_B_C(tasks)))


task_transition = Factor("task transition", [
    DerivedLevel("A-B-A", Window(A_B_A, [task], 3, 1)),
    DerivedLevel("A-B-C", Window(A_B_C, [task], 3, 1)),
])

# DEFINE CONSTRAINTS

constraints = [Exclude("object configuration", "illegal")]

# DEFINE EXPERIMENT
design       = [deviantColorObject, deviantOrientationObject, deviantMovementObject, objectConfiguration, task, task_transition]
crossing     = [deviantColorObject, deviantOrientationObject, deviantMovementObject, task, task_transition]

block        = fully_cross_block(design, crossing, constraints, require_complete_crossing=False)

# SOLVE

# from sweetpea.encoding_diagram import print_encoding_diagram
# print_encoding_diagram(block)

#from sweetpea import save_json_request
#save_json_request(block, 10, "long-runner-request.json")

from sweetpea.metrics import collect_design_metrics
metrics = collect_design_metrics(block)

from pprint import pprint
pprint(metrics)
