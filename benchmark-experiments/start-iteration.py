import math


count = 20922789888000


kappa = 0.638
pivotUniGen = math.ceil(4.03 * (1 + 1 / kappa) * (1 + 1 / kappa))
logCount = math.log(count, 2)
startIteration = int(round(logCount + math.log(1.8, 2) - math.log(pivotUniGen, 2))) - 2

print(startIteration)