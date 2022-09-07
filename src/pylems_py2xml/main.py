# Usage: xm = XML(suffix='50healthy', uid='delta_times', app=True)

import re
from pylems_py2xml.utils import *
from pylems_py2xml.models import *


class XML:
    """
    Main class that reads Python code, finds the model used, preprocesses parameters
    specified in the code and passes to the Models class to change the default values
    and saves XML files.

    Parameters
    ----------
    input_path :        str (default='../examples/50healthy_code.py')
        Path to the Python code that contains one of the models (HindmarshRose, WongWang, etc)

    output_path :       str (default='../examples')
        Path to a folder that will store converted XML files

    unit :              str (default='s' (seconds))
        # TODO: add description here

    uid :               str (default = 'default')
        Unique identifier that is used in lems.Component construction

    app:              bool (default=False)
        Whether the user is using this conversion through BEP034 conversion app (https://github.com/dissagaliyeva/incf).
        If True, the conversions will follow BIDS format. For that you will need to supplement "uid" and "suffix" fields.

    store_numeric :     bool (default=True)
        Whether to store only numeric values. For example, if you want to disregard
        'variables_of_interest' = ['xi', 'alpha'] in the final XML file, you should leave the default True value.

    suffix :            str (default=None)
        Suffix used in the final XML name. By default, two files get saved: model's equations (e.g., SJHM3D for
        HindmarshRose model -> model-SJHM3D_{uid}.xml) and parameters (e.g., {suffix}_param.xml).

    """

    def __init__(self, inp='../examples/50healthy_code.py', output_path='../examples',
                 unit='s', uid='default', app=False, store_numeric=True, suffix=None):
        # define passed-in parameters
        self.input_path = inp
        self.output_path = output_path
        self.unit = unit
        self.uid = uid
        self.app = app
        self.store_numeric = store_numeric
        self.suffix = suffix

        # create placeholder for to-be-supplemented variables
        self.model_name = None
        self.params = None
        self.model = None
        self.temp_params = None

        self.content = open_file(inp)  # get content from the input path
        self.models = ['hindmarshrose', 'wongwang']  # supported models

        if isinstance(inp, str):
            self.get_model()
        elif isinstance(inp, dict):
            pass

    def get_model(self):
        """
        Function that finds models and their parameters used in Python code.
        """

        # combine list to form string literal
        pattern = ''.join(self.content)

        # find models used and their parameters ignoring upper-, lower-case
        match = re.findall(r'(?:hindmarsh|wongwang)[a-zA-Z0-9=()\]\[\'\"\.\,\s\-\_]+', pattern, flags=re.IGNORECASE)

        # only if there's a match, traverse parameters and get their 'cleaned' version
        if len(match) > 0:
            # get only parameters
            self.model_name = re.match('[a-zA-Z]+', match[0])[0].lower()

            # clean further to get parameters
            self.temp_params = [x.strip(',') for x in re.findall(r'[a-zA-Z0-9]+\=[0-9\,\.\-\'\"\[\]]+', match[0])
                                if x.endswith('],')]

            # traverse cleaned parameters to get a dictionary of parameters
            self.split_params()

            # call the Models class to save XML files
            self.model = Models(self.model_name, self.output_path, self.uid,
                                suffix=self.suffix, app=True, **self.params)

    def split_params(self):
        """
        Preprocess the result of regex traversal and store parameters in a dictionary.
        These parameters need to be stored in a dictionary because the default model's
        parameters will be altered with the new values (hence, these cleaned values
        in a dictionary).

        For example, if input is: ['r=[0.006]', 'a=[1.0]', 'b=[3.0]', 'c=[1.0]'], the
        output will become: {'r': [0.006], 'a': [1.0], 'b': [3.0], 'c': [1.0]}
        """
        # create an empty dictionary that will store new values
        struct = {}

        # traverse over list of parameters
        for param in self.temp_params:
            k = re.match(r'[a-zA-Z0-9]+', param)[0]
            v = re.findall(r'[0-9\.]+', re.findall(r'\[[0-9\.\-]+', param)[0])[0]
            struct[k] = [float(v)]

        self.params = struct
