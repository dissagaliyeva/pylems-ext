from utils import *
import lems.api as lems

FILE = '../examples/50healthy_code.py'
content = []

# instantiate the model
model = lems.Model()

with open(FILE) as f:
    for line in f.readlines():
        if not line.startswith('#') and not line.startswith('import') and not line.startswith('from') and line != '\n':
            content.append(line.strip('\n').strip())

print(content)

for c in content:
    if 'rose' in c.lower():
        pass

