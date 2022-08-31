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
import json
import os
import re

from utils import *
import lems.api as lems


# def __init__(self, model_name: [None, str, list], output, uid='default',
#              usage='app', unit='s', store_numeric=True, suffix=None, **params):


class XML:
    def __init__(self, input_path='../examples/50healthy_code.py', output_path='../example',
                 unit='s', uid='default', usage='app', store_numeric=True, suffix=None):
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

    def get_model(self):
        pattern = ''.join(self.content)
        match = re.findall(r'Hindmarsh[a-zA-Z0-9=()\]\[\'\"\.\,\s\-\_]+', pattern)

        print(match)

        if len(match) > 0:
            # get only parameters
            self.model_name = re.match('[a-zA-Z]+', match[0])[0]

            self.params = [x.strip(',') for x in re.findall(r'[a-zA-Z0-9]+\=[0-9\,\.\-\'\"\[\]]+', match[0])
                           if x.endswith('],')]
            self.split_params()

    def split_params(self):
        struct = {}

        for param in self.params:
            k = re.match(r'[a-zA-Z0-9]+', param)[0]
            v = re.findall(r'[0-9\.]+', re.findall(r'\[[0-9\.\-]+', param)[0])[0]
            struct[k] = v

        self.params = struct






xm = XML()
print(xm.get_model())


