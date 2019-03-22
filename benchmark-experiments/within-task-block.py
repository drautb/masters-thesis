from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Transition
from sweetpea.constraints import NoMoreThanKInARow
from sweetpea import fully_cross_block, synthesize_trials_non_uniform, print_experiments


"""
Extended Stroop Task
******************************
factors (levels):
- current color (red, blue, green, brown)
- color transition (repetition, switch): factor dependent on color.
- current word (red, blue, green, brown)
- word transition (repetition, switch): factor dependent on word.
- current location (up, down, left, right)
- location transition (repetition, switch): factor dependent on location.
- congruency (congruent, incongruent): factor dependent on color and word.
- correct response (up, down, left right): factor dependent on color.
- response transition (repetition, switch). factor dependent on response.

constraints:
- counterbalancing color x location x congruency x resp_transition
- no more than 2 color repetitions in a row
- no more than 2 word repetitions in a row
- no more than 2 location repetitions in a row

"""

# DEFINE COLOR AND WORD FACTORS

color      = Factor("color",  ["red", "blue", "green", "brown"])
word       = Factor("motion", ["red", "blue", "green", "brown"])
location       = Factor("location", ["up", "down", "left", "right"])

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

def response_up(color):
    return color == "red"
def response_down(color):
    return color == "blue"
def response_left(color):
    return color == "green"
def response_right(color):
    return color == "brown"

response = Factor("response", [
    DerivedLevel("up", WithinTrial(response_up,   [color])),
    DerivedLevel("down", WithinTrial(response_down,   [color])),
    DerivedLevel("left", WithinTrial(response_left,   [color])),
    DerivedLevel("right", WithinTrial(response_right,   [color])),
])

# DEFINE WORD TRANSITION FACTOR

def word_repeat(word):
    return word[0] == word[1]

def word_switch(word):
    return not word_repeat(word)

word_transition = Factor("word_transition", [
    DerivedLevel("repeat", Transition(word_repeat, [word])),
    DerivedLevel("switch", Transition(word_switch, [word]))
])

# DEFINE COLOR TRANSITION FACTOR

def color_repeat(color):
    return color[0] == color[1]

def color_switch(color):
    return not color_repeat(color)

color_transition = Factor("color_transition", [
    DerivedLevel("repeat", Transition(color_repeat, [color])),
    DerivedLevel("switch", Transition(color_switch, [color]))
])

# DEFINE LOCATION TRANSITION FACTOR

def location_repeat(location):
    return location[0] == location[1]

def location_switch(location):
    return not location_repeat(location)

location_transition = Factor("location_transition", [
    DerivedLevel("repeat", Transition(location_repeat, [location])),
    DerivedLevel("switch", Transition(location_switch, [location]))
])

# DEFINE RESPONSE TRANSITION FACTOR

def response_repeat(response):
    return response[0] == response[1]

def response_switch(response):
    return not response_repeat(response)

resp_transition = Factor("response_transition", [
    DerivedLevel("repeat", Transition(response_repeat, [response])),
    DerivedLevel("switch", Transition(response_switch, [response]))
])

# DEFINE SEQUENCE CONSTRAINTS

k = 7
constraints = [NoMoreThanKInARow(2, word_transition),
               NoMoreThanKInARow(2, location_transition),
               NoMoreThanKInARow(2, color_transition)]

# DEFINE EXPERIMENT

design       = [color, word, congruency, location, response, resp_transition, word_transition, color_transition, location_transition]
crossing     = [color, congruency, location, resp_transition]
block        = fully_cross_block(design, crossing, constraints)

# SOLVE

from sweetpea.metrics import collect_design_metrics
metrics = collect_design_metrics(block)

from pprint import pprint
pprint(metrics)
