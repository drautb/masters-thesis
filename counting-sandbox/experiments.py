from sweetpea import fully_cross_block, save_cnf, synthesize_trials_non_uniform
from sweetpea.primitives import Factor
from sweetpea.constraints import AtMostKInARow


# Stroop 2 Basic
color_list = ["red", "blue"]
color = Factor("color", color_list)
text  = Factor("text",  color_list)

design = [color, text]
crossing = [color, text]
block  = fully_cross_block(design, crossing, [])

save_cnf(block, "stroop-2-basic-24.cnf")


# Stroop 2 with additional uncrossed factor.
direction = Factor("direction", ["left", "right"])
design = [color, text, direction]
block = fully_cross_block(design, crossing, [])

save_cnf(block, "stroop-2-with-2-directions-384.cnf")


# Stroop 2 with 4 directions uncrossed
direction = Factor("direction", ["left", "right", "up", "down"])
design = [color, text, direction]
block = fully_cross_block(design, crossing, [])

save_cnf(block, "stroop-2-with-4-direction-6144.cnf")


# Stroop 2 with 2 directions and 3 letters uncrossed.
direction = Factor("direction", ["left", "right"])
letter = Factor("letter", ["a", "b", "c"])
design = [color, text, direction, letter]
crossing = [color, text]
block = fully_cross_block(design, crossing, [])

save_cnf(block, "stroop-2-with-2-directions-3-letters-31104.cnf")


# Stroop 3 with 1 constraint
color_list = ["red", "orange", "blue"]
color = Factor("color", color_list)
text  = Factor("text",  color_list)
design = [color, text]
crossing = [color, text]
constraints = [AtMostKInARow(1, ("color", "red"))]
block = fully_cross_block(design, crossing, constraints)

save_cnf(block, "stroop-3-with-1-red-constraint.cnf")


# Stroop 4 with 1 constraint
color_list = ["red", "orange", "blue", "green"]
color = Factor("color", color_list)
text  = Factor("text",  color_list)
design = [color, text]
crossing = [color, text]
constraints = [AtMostKInARow(1, ("color", "red"))]
block = fully_cross_block(design, crossing, constraints)

save_cnf(block, "stroop-4-with-1-red-constraint.cnf")


# Stroop 5 with 1 constraint
color_list = ["red", "orange", "blue", "green", "yellow"]
color = Factor("color", color_list)
text  = Factor("text",  color_list)
design = [color, text]
crossing = [color, text]
constraints = [AtMostKInARow(1, ("color", "red"))]
block = fully_cross_block(design, crossing, constraints)

save_cnf(block, "stroop-5-with-1-red-constraint.cnf")



