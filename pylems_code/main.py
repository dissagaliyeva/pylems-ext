"""
What I want to do in this project:
1. Use it for the app's traversal over code
2. Extend the usage and send to PyLEMS community


App requirements:
1. path to input code file
2. path to output folders: eq (1 file containing equations)  and params (2 files: params that include just the
components and their values, and model TYPE as xml containing equations and params)
3. user-specific info on voltage, time, and capacitance
4. units (ms, s, ...) -> taken from the JSON files

PyLEMS:
1. CLI usage
2. Jupyter notebook implementaion tutorial
3. usual python code

Solution:
1. Store CLI and other usage separate
2. Add


Features:
1. Add logger that shows the steps and if there were any mistakes

"""

import re
from pylems_code.utils import *
from pylems_code.models import *


class XML:
    def __init__(self, input_path='../examples/50healthy_code.py', output_path='../examples',
                 unit='s', uid='default', usage='app', store_numeric=True, suffix=None):
        self.model = None
        self.temp_params = None
        self.input_path = input_path
        self.output_path = output_path
        self.unit = unit
        self.uid = uid
        self.usage = usage
        self.store_numeric = store_numeric
        self.suffix = suffix

        self.model_name = None
        self.params = None

        self.content = open_file(input_path)                # get content from the input path
        self.models = ['hindmarshrose', 'wongwang']         # supported models

        self.get_model()

    def get_model(self):
        pattern = ''.join(self.content)

        # TODO: add other models as well
        match = re.findall(r'(?:Hindmarsh|Wongwang)[a-zA-Z0-9=()\]\[\'\"\.\,\s\-\_]+', pattern, flags=re.IGNORECASE)

        if len(match) > 0:
            # get only parameters
            self.model_name = re.match('[a-zA-Z]+', match[0])[0].lower()

            self.temp_params = [x.strip(',') for x in re.findall(r'[a-zA-Z0-9]+\=[0-9\,\.\-\'\"\[\]]+', match[0])
                                if x.endswith('],')]
            self.split_params()
            self.model = Models(self.model_name, self.output_path, self.uid,
                                suffix=self.suffix, app=True, **self.params)

    def split_params(self):
        struct = {}

        for param in self.temp_params:
            k = re.match(r'[a-zA-Z0-9]+', param)[0]
            v = re.findall(r'[0-9\.]+', re.findall(r'\[[0-9\.\-]+', param)[0])[0]
            struct[k] = [float(v)]

        self.params = struct


xm = XML(suffix='50healthy', uid='delta_times')