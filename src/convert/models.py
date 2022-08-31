import glob
import os
from xml.etree import ElementTree

import lems.api as lems


class Models:
    def __init__(self, model_name: [None, str, list], output, uid='default',
                 usage='app', unit='s', store_numeric=True, suffix=None, **params):
        self.model_name = model_name  # define the selected model
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
            'hindmarshRose': dict(r=[0.006], a=[1.], b=[3.], c=[1.], d=[5.], s=[1.], xo=[-1.6], K11=[0.5],
                                  K12=[0.1], K21=[0.15], sigma=[0.3], mu=[3.3], x_1=[-1.6], A_ik=None, B_ik=None,
                                  C_ik=None, a_i=None, b_i=None, c_i=None, d_i=None, e_i=None, f_i=None, h_i=None,
                                  p_i=None, IE_i=None, II_i=None, m_i=None, n_i=None,
                                  variables_of_interest=['xi', 'eta', 'tau'],
                                  state_variable_range=dict(x=[-4., 4.], y=[-60., 20.], z=[-2., 18.], eta=[-25., 20.0],
                                                            alpha=[-4., 4.], beta=[-20., 20.], gamma=[2., 10.]))
        }

        self.execute_steps()

    def execute_steps(self):
        # 1. change default values if supplemented
        self.change_params()

        if self.model is not None:
            model = self.create_params()
            if self.usage == 'app':
                self.save_xml(model)
                self.save_xml(model, 'model')

    def change_params(self):
        temp = self.models[self.model_name].copy()
        self.model = {key: self.params.get(key, temp[key]) for key in temp.keys()}

    def create_params(self):
        model = lems.Model()

        if self.model_name == 'hindmarshRose':
            self.comp_type = 'SJHM3D'
        elif self.model_name == 'wong-wang':
            self.comp_type = 'WongWang'

        if self.store_numeric:
            # remove brackets and store only numeric values
            self.model = {k: v[0] for k, v in self.model.items() if isinstance(v, list) and len(v) == 1}

        # store only those parameters that have numeric values,
        # this will be used and stored in ../output/param folder
        model.add(lems.Component(id_=self.uid, type_=self.comp_type, **self.model))

        return model

    def save_xml(self, model, ftype='default'):
        # save the default model
        if ftype == 'default':
            self.path = os.path.join(self.output, f'{self.suffix}_param.xml')
            model.export_to_file(self.path)
        elif ftype == 'model':
            # model.add(model.import_from_file(f'templates/{self.model_name}.xml'))
            # print(model)
            # model.import_from_file(f'templates/{self.model_name}.xml')
            # print(model.merge_component_types(lems.Model().import_from_file(f'templates/{self.model_name}.xml'), model))
            self.merge_xml()
        #  model.export_to_file(os.path.join(self.output, 'params.xml'))
        pass

    def merge_xml(self):
        if os.path.exists(self.path):
            model = None

            xml1 = self.path
            xml2 = os.path.join('templates', self.model_name + '.xml')

            for xml in [xml1, xml2]:
                tree = ElementTree.parse(xml)
                root = tree.getroot()

                if model is None:
                    model = root
                else:
                    print(dir(root))
                    print(root.items())
                    print(root.text)
                    # elements = root.find('Lems')
                    # print(type(elements))
                    # print(type(model))
                    # for element in elements._children:
                    #     model[1].append(element)
        # print(model)


print(Models('hindmarshRose', '../../examples', suffix='50healthy', uid='delta_series',
             r=[0.006], a=[1.0], b=[3.0], c=[1.0], d=[5.0], s=[4.0], xo=[-1.6], K11=[0.5],
             K12=[0.1], K21=[0.15], sigma=[0.3], mu=[2.2], variables_of_interest=["xi", "alpha"]).model)

# def __init__(self, model_name: [None, str, list], output, uid='default',
#              usage='app', unit='s', store_numeric=True, suffix=None, **params):