import glob
import json
import os
import re

from subprocess import check_output


path_to_benchmarks = "/home/drautb/GitHub/meelgroup/sampling-benchmarks/unigen-benchmarks/**/*.cnf"

data = {}

for filename in glob.glob(path_to_benchmarks):
	print("Counting solutions for {}...".format(filename))

	try:
		output = check_output("/home/drautb/GitHub/ZaydH/spur/build/Release/spur -count-only -cnf {}".format(filename), shell=True)
		output = output.decode('utf-8')

		m = re.search('\n# solutions \n(\\d+)\n', output)
		count = int(m.groups(0)[0])

		m = re.search('\ntime: (\\d+\\.\\d+)s\n', output)
		total_time = float(m.groups(0)[0])

		data[filename] = {
			'count': count,
			'time': total_time
		}

		with open('data.json', 'w') as f:
			f.write(json.dumps(data))

	except:
		continue

