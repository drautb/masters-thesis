import os
import json

from datetime import datetime
from subprocess import STDOUT, run

benchmarks = {
    'cryptominisat': {},
    'unigen': {},
    'd4': {},
    'kus': {},
    'spur': {}
}

for f in os.listdir('cnfs'):

    # CRYPTO
    start = datetime.now()
    run(['cryptominisat5', 'cnfs/' + f], stderr=STDOUT, timeout=3600)
    end = datetime.now()
    elapsed = (end - start).seconds
    benchmarks['cryptominisat'][f] = elapsed

    # UNIGEN
    start = datetime.now()
    run(['unigen', '--verbosity=0', '--maxTotalTime=36000', '--samples=10', 'cnfs/' + f], stderr=STDOUT, timeout=39600)
    end = datetime.now()
    elapsed = (end - start).seconds
    benchmarks['unigen'][f] = elapsed

    # KUS
    # Generate the d-DNNFs
    start = datetime.now()
    run(['/home/drautb/GitHub/meelgroup/KUS/d4', 'cnfs/' + f, '-out="d-DNNFs/' + f + '.ddnnf'], stderr=STDOUT, timeout=36000)
    end = datetime.now()
    elapsed = (end - start).seconds
    benchmarks['d4'][f] = elapsed

    # Run KUS
    start = datetime.now()
    run(['python', '/home/drautb/GitHub/meelgroup/KUS/KUS.py', '--dDNNF', 'd-DNNFs/' + f + '.ddnnf'], stderr=STDOUT, timeout=36000)
    end = datetime.now()
    elapsed = (end - start).seconds
    benchmarks['kus'][f] = elapsed

    # SPUR
    start = datetime.now()
    run(['/home/drautb/GitHub/ZaydH/spur/build/Release/spur', '-cnf', 'cnfs/' + f, '-s', '10'], stderr=STDOUT, timeout=36000)
    end = datetime.now()
    elapsed = (end - start).seconds
    benchmarks['spur'][f] = elapsed


# Save benchmarks to disk
with open('benchmarks.json', 'w') as f:
    f.write(json.dumps(benchmarks))


