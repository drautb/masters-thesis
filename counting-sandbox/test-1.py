import operator as op

from sweetpea.primitives import Factor, DerivedLevel, WithinTrial
from sweetpea.constraints import AtMostKInARow
from sweetpea import fully_cross_block, synthesize_trials_non_uniform, print_experiments


color_list = ["red", "blue"]
color = Factor("color", color_list)
text  = Factor("text",  color_list)

conLevel  = DerivedLevel("con", WithinTrial(op.eq, [color, text]))
incLevel  = DerivedLevel("inc", WithinTrial(op.ne, [color, text]))
conFactor = Factor("congruent?", [conLevel, incLevel])

design       = [color, text]
crossing     = [color, text]

constraints = [AtMostKInARow(1, ("color", "red"))]

block        = fully_cross_block(design, crossing, constraints)

# Synthesize 5 unique, but non-uniformly sampled, trials.
experiments  = synthesize_trials_non_uniform(block, 50)

print(str(len(experiments))) # Should be 12



