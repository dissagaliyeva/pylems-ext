import lems.api as lems


class Models:
    def __init__(self, model_name, output, unit='s', **params):
        self.model_name = model_name  # define the selected model
        self.output = output
        self.unit = unit
        self.params = params
        self.model = None

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

        self.change_params()

    def change_params(self):
        temp = self.models[self.model_name].copy()
        self.model = {key: self.params.get(key, temp[key]) for key in temp.keys()}
        self.save_lems()

    def save_lems(self):
        model = lems.Model()

        # remove brackets and store only numeric values
        self.model = {k: v[0] for k, v in self.model.items() if isinstance(v, list) and len(v) == 1}

        # append values
        model.add(lems.Component(id_='1', type_='SJHM3D', **self.model))

        model.export_to_file('model.xml')


print(Models('hindmarshRose', '../examples',
             r=[0.006], a=[1.0], b=[3.0], c=[1.0], d=[5.0], s=[4.0], xo=[-1.6], K11=[0.5],
             K12=[0.1], K21=[0.15], sigma=[0.3], mu=[2.2], variables_of_interest=["xi", "alpha"]).model)
