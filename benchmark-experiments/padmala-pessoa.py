from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Transition
from sweetpea.constraints import AtMostKInARow
from sweetpea.encoding_diagram import print_encoding_diagram
from sweetpea.metrics import collect_design_metrics
from sweetpea import fully_cross_block, synthesize_trials_non_uniform, print_experiments


"""
Padmala & Pessoa design
***********************
factors (levels):
- congruency (congruent, incongruent, neutral)
- reward (rewarded, non-rewarded)
- response (left, right)
- congruency transition (congruent-congruent, congruent-incongruent, congruent-neutral, incongruent-congruent, incongruent-incongruent, incongruent-neutral, neutral-congruent, neutral-incongruent, neutral-neutral)
constraints:
- counterbalancing congruency x reward x response x congruency transition (3*2*2*9 = 108)
- counterbalancing all transitions <-- ????
Total number of trials: around 120
"""

congruency  = Factor("congruency", ["congruent", "incongruent", "neutral"])
reward      = Factor("reward",     ["rewarded", "non-rewarded"])
response    = Factor("response",   ["building", "house"])

congruency_transition = Factor("congruency_transition", [
    DerivedLevel("congruent-congruent",     Transition(lambda c: c[0] == "congruent"   and c[1] == "congruent",   [congruency])),
    DerivedLevel("congruent-incongruent",   Transition(lambda c: c[0] == "congruent"   and c[1] == "incongruent", [congruency])),
    DerivedLevel("congruent-neutral",       Transition(lambda c: c[0] == "congruent"   and c[1] == "neutral",     [congruency])),
    DerivedLevel("incongruent-congruent",   Transition(lambda c: c[0] == "incongruent" and c[1] == "congruent",   [congruency])),
    DerivedLevel("incongruent-incongruent", Transition(lambda c: c[0] == "incongruent" and c[1] == "incongruent", [congruency])),
    DerivedLevel("incongruent-neutral",     Transition(lambda c: c[0] == "incongruent" and c[1] == "neutral",     [congruency])),
    DerivedLevel("neutral-congruent",       Transition(lambda c: c[0] == "neutral"     and c[1] == "congruent",   [congruency])),
    DerivedLevel("neutral-incongruent",     Transition(lambda c: c[0] == "neutral"     and c[1] == "incongruent", [congruency])),
    DerivedLevel("neutral-neutral",         Transition(lambda c: c[0] == "neutral"     and c[1] == "neutral",     [congruency]))
])

response_transition = Factor("resp_transition", [
    DerivedLevel("repeat", Transition(lambda r: r[0] == r[1], [response])),
    DerivedLevel("switch", Transition(lambda r: r[0] != r[1], [response]))
])

k = 7
constraints = [AtMostKInARow(k, congruency_transition),
               AtMostKInARow(k, response_transition)]

design       = [congruency, reward, response, congruency_transition, response_transition]
crossing     = [congruency, reward, response, congruency_transition]
block        = fully_cross_block(design, crossing, constraints)

print_encoding_diagram(block)
metrics = collect_design_metrics(block)

# experiments  = synthesize_trials_non_uniform(block, 5)

# print_experiments(block, experiments)
