import os
import shutil
import lems.api as lems


class Models:
    """



    """
    def __init__(self, model_name: str = 'hindmarshRose', output: str = '../examples', uid: str = 'default',
                 usage: str = 'app', unit: str = 's', store_numeric: bool = True, suffix: str = None, **params):
        self.model_name = model_name                    # define the selected model
        self.output = output
        self.uid = uid
        self.usage = usage
        self.unit = unit
        self.store_numeric = store_numeric
        self.suffix = suffix
        self.params = params

        self.path = None
        self.model = None
        self.comp_type = uid

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

        self.execute_steps()

    def execute_steps(self):
        """:return:"""
        # 1. change default values if supplemented
        self.change_params()

        if self.model is not None:
            model = self.create_params()
            if self.usage == 'app':
                self.save_xml(model)
                self.save_xml(model, 'model')

    def change_params(self):
        """:return:"""
        temp = self.models[self.model_name].copy()
        self.model = {key: self.params.get(key, temp[key]) for key in temp.keys()}

    def create_params(self):
        """:return:"""
        model = lems.Model()

        if self.model_name == 'hindmarshrose':
            self.comp_type = 'SJHM3D'
        elif self.model_name == 'wongwang':
            self.comp_type = 'WongWang'

        if self.store_numeric:
            # remove brackets and store only numeric values
            self.model = {k: v[0] for k, v in self.model.items() if isinstance(v, list) and len(v) == 1}

        # store only those parameters that have numeric values,
        # this will be used and stored in ../output/param folder
        model.add(lems.Component(id_=self.uid, type_=self.comp_type, **self.model))

        return model

    def save_xml(self, model, ftype='default'):
        """

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
        pass

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