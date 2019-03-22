from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Transition
from sweetpea.constraints import NoMoreThanKInARow
from sweetpea import fully_cross_block, synthesize_trials_non_uniform, print_experiments


"""
Task Switching Paradigm
******************************
factors (levels):
- current color (red, blue, green, brown)
- current word (red, blue, green, brown)
- task (color naming, word reading)
- task transition (task switch, task repetition): factor dependent on task.
- congruency (congruent, incongruent): factor dependent on color and word.
- correct response (up, down, left right): factor dependent on color, word and task.
- response transition (repetition, switch). factor dependent on response:

design:
- counterbalancing color x word x task x task transition x correct response
- no more than 7 response repetitions in a row
- no more than 7 response switches in a row
- no more than 7 task repetitions in a row
- no more than 7 task switches in a row

"""

# DEFINE COLOR AND WORD FACTORS

color      = Factor("color",  ["red", "blue", "green", "brown"])
word       = Factor("motion", ["red", "blue", "green", "brown"])
task       = Factor("task", ["color naming", "word reading"])

# DEFINE TASK TRANSITION

def task_repeat(tasks):
    return tasks[0] == tasks[1]

def task_switch(tasks):
    return not task_repeat(tasks)

task_transition = Factor("task_transition", [
    DerivedLevel("repeat", Transition(task_repeat, [task])),
    DerivedLevel("switch", Transition(task_switch, [task]))
])

# DEFINE CONGRUENCY FACTOR

def congruent(color, word):
    return color == word

def incongruent(color, word):
    return not congruent(color, word)


conLevel = DerivedLevel("con", WithinTrial(congruent,   [color, word]))
incLevel = DerivedLevel("inc", WithinTrial(incongruent,   [color, word]))

congruency = Factor("congruency", [
    conLevel,
    incLevel
])

# DEFINE RESPONSE FACTOR

def response_up(task, color, word):
    return (task == "color naming" and color == "red") or (task == "word reading" and word == "red")
def response_down(task, color, word):
    return (task == "color naming" and color == "blue") or (task == "word reading" and word == "blue")
def response_left(task, color, word):
    return (task == "color naming" and color == "green") or (task == "word reading" and word == "green")
def response_right(task, color, word):
    return (task == "color naming" and color == "brown") or (task == "word reading" and word == "brown")

response = Factor("response", [
    DerivedLevel("up", WithinTrial(response_up,   [task, color, word])),
    DerivedLevel("down", WithinTrial(response_down,   [task, color, word])),
    DerivedLevel("left", WithinTrial(response_left,   [task, color, word])),
    DerivedLevel("right", WithinTrial(response_right,   [task, color, word])),
])

# DEFINE RESPONSE TRANSITION FACTOR

def response_repeat(response):
    return response[0] == response[1]

def response_switch(response):
    return not response_repeat(response)

response_transition = Factor("response_transition", [
    DerivedLevel("repeat", Transition(response_repeat, [response])),
    DerivedLevel("switch", Transition(response_switch, [response]))
])

# DEFINE SEQUENCE CONSTRAINTS

# k = 7
# constraints = [NoMoreThanKInARow(k, task_transition),
#                NoMoreThanKInARow(k, response_transition)]

constraints = []


# DEFINE EXPERIMENT

design       = [color, word, task, task_transition, congruency, response, response_transition]
crossing     = [color, word, task]
block        = fully_cross_block(design, crossing, constraints)

# SOLVE

from sweetpea.metrics import collect_design_metrics
metrics = collect_design_metrics(block)

from pprint import pprint
pprint(metrics)
