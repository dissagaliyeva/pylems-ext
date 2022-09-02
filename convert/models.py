import os
import shutil
import lems.api as lems


class Models:
    """
    Create an XML model using PyLEMS and supplemented Python code, change default parameters,
    and save files in the specified folder.

    Parameters
    ----------
    model_name :        str (default = 'hindmarshRose')
        Name of the model found in Python code. Supported model(s): HindmarshRose.

    output:             str (default='../examples')
        Path to the folder where conversions need to be stored.

    uid:                str (default = 'default')
        Unique identifier that is used in lems.Component construction

    app:              bool (default=False)
        Whether the user is using this conversion through BEP034 conversion app (https://github.com/dissagaliyeva/incf).
        If True, the conversions will follow BIDS format. For that you will need to supplement "uid" and "suffix" fields.

    unit:               str (default='s')
        #TODO: add description here

    store_numeric :     bool (default=True)
        Whether to store only numeric values. For example, if you want to disregard
        'variables_of_interest' = ['xi', 'alpha'] in the final XML file, you should leave the default True value.

    suffix :            str (default=None)
        Suffix used in the final XML name. By default, two files get saved: model's equations (e.g., SJHM3D for
        HindmarshRose model -> model-SJHM3D_{uid}.xml) and parameters (e.g., {suffix}_param.xml).

    **params:           dict
        Parameters derived from Python code, already preprocessed in main.py.

    """
    def __init__(self, model_name: str = 'hindmarshRose', output: str = '../examples', uid: str = 'default',
                 app: bool = False, unit: str = 's', store_numeric: bool = True, suffix: str = None, **params):
        self.model_name = model_name                    # chosen model
        self.output = output                            # path to store output results
        self.uid = uid                                  # lems.Component's id_ parameter
        self.app = app                                  # whether you're using it through the app (https://github.com/dissagaliyeva/incf)
        self.unit = unit                                # TODO: add description
        self.store_numeric = store_numeric              # whether to store only numeric fields from the model
        self.suffix = suffix                            # suffix to use in file naming
        self.params = params                            # parameters derived from supplemented Python code

        self.path = None                                # full path (with file name)
        self.model = None                               # lems model
        self.comp_type = uid                            # model name (SJHM3D, WongWang)

        self.models = {
            # define default values of HindmarhRose from TVB model's package
            # https://github.com/the-virtual-brain/tvb-root/blob/master/tvb_library/tvb/simulator/models/stefanescu_jirsa.py
            'hindmarshrose': dict(r=[0.006], a=[1.], b=[3.], c=[1.], d=[5.], s=[1.], xo=[-1.6], K11=[0.5],
                                  K12=[0.1], K21=[0.15], sigma=[0.3], mu=[3.3], x_1=[-1.6], A_ik=None, B_ik=None,
                                  C_ik=None, a_i=None, b_i=None, c_i=None, d_i=None, e_i=None, f_i=None, h_i=None,
                                  p_i=None, IE_i=None, II_i=None, m_i=None, n_i=None,
                                  variables_of_interest=['xi', 'eta', 'tau'],
                                  state_variable_range=dict(x=[-4., 4.], y=[-60., 20.], z=[-2., 18.], eta=[-25., 20.0],
                                                            alpha=[-4., 4.], beta=[-20., 20.], gamma=[2., 10.]))
        }

        # run the steps to save files
        self.execute_steps()

    def execute_steps(self):
        """
        Define the steps to verify, preprocess, and save XML files.
        """
        # change default model values with values found in Python code
        self.change_params()

        # save XML files
        if self.model is not None:
            # get LEMS model and Components
            model = self.create_params()

            # save the default
            self.save_xml(model)

            if self.app:
                self.save_xml(model, 'model')

    def change_params(self):
        """
        Iterate over newly-found parameters and change the default values.
        """

        # copy the existing model
        temp = self.models[self.model_name].copy()

        # change default values and store in a new variable
        self.model = {key: self.params.get(key, temp[key]) for key in temp.keys()}

    def create_params(self):
        """
        Create lems.Model and add the components.
        """

        # instantiate lems.Model
        model = lems.Model()

        # define model's type
        if self.model_name == 'hindmarshrose':
            self.comp_type = 'SJHM3D'
        elif self.model_name == 'wongwang':
            self.comp_type = 'WongWang'

        # store only numeric values if enabled
        if self.store_numeric:
            # remove brackets and store only numeric values
            self.model = {k: v[0] for k, v in self.model.items() if isinstance(v, list) and len(v) == 1}

        # store only those parameters that have numeric values,
        # this will be used and stored in ../output/param folder
        model.add(lems.Component(id_=self.uid, type_=self.comp_type, **self.model))

        return model

    def save_xml(self, model, ftype='default'):
        """
        Save the model to XML file.

        Parameters
        ----------
        model :
            param ftype:
        ftype :
            (Default value = 'default')

        Returns
        -------

        
        """
        # save the default model
        if ftype == 'default':
            self.path = os.path.join(self.output, f'desc-{self.suffix}_param.xml')
            model.export_to_file(self.path)
        elif ftype == 'model':
            self.merge_xml()

    def merge_xml(self):
        """:return:"""
        if os.path.exists(self.path):
            xml1 = self.path
            xml2 = os.path.join('templates', self.model_name + '.xml')
            file = os.path.join(self.output, f'model-{self.comp_type}_{self.uid}.xml')

            exists = False

            if os.path.exists(file):
                os.remove(file)

            for fname in [xml2, xml1]:
                with open(file, 'a') as outfile:
                    with open(fname) as infile:
                        for line in infile:
                            if line.startswith('<Lems') or line.startswith('<?xml'):
                                if not exists:
                                    outfile.write(line)
                            else:
                                if not exists and line.startswith('</Lems>'):
                                    continue
                                outfile.write(line)
                exists = True

            # save eq xml
            shutil.copy(xml2, os.path.join(self.output, f'desc-{self.suffix}_eq.xml'))