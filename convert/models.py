class Models:
    def __init__(self, model_name, **params):
        self.model_name = model_name  # define the selected model
        self.params = params
        self.model = None

        self.models = {
            # define default values of HindmarhRose from TVB model's package
            # https://github.com/the-virtual-brain/tvb-root/blob/master/tvb_library/tvb/simulator/models/stefanescu_jirsa.py
            'hindmarshRose': dict(r=[0.006], a=[1.], b=[3.], c=[1.], d=[5.], s=[1.], xo=[-1.6], K11=[0.5],
                                  K12=[0.1], K21=[0.15], sigma=[0.3], mu=[3.3], A_ik=None, B_ik=None, C_ik=None,
                                  a_i=None, b_i=None, c_i=None, d_i=None, e_i=None, f_i=None, h_i=None, p_i=None,
                                  IE_i=None, II_i=None, m_i=None, n_i=None,
                                  x_1=-1.6, variables_of_interest=['xi', 'eta', 'tau'],
                                  state_variable_range=dict(x=[-4., 4.], y=[-60., 20.], z=[-2., 18.], eta=[-25., 20.0],
                                                            alpha=[-4., 4.], beta=[-20., 20.], gamma=[2., 10.]))
        }

        self.change_params()

    def change_params(self):
        temp = self.models[self.model_name].copy()
        self.model = {key: self.params.get(key, temp[key]) for key in temp.keys()}


print(Models('hindmarshRose', r=[0.006], a=[1.0], b=[3.0], c=[1.0], d=[5.0], s=[4.0], xo=[-1.6], K11=[0.5],
             K12=[0.1], K21=[0.15], sigma=[0.3], mu=[2.2], variables_of_interest=["xi", "alpha"]).model)
