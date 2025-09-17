"""
                           
 _|      _|      _|_|_|_|  
 _|_|  _|_|      _|        
 _|  _|  _|      _|_|_|    
 _|      _|      _|        
 _|      _|  _|  _|    _|  
                           
 Material        Fingerprinting

"""

import matplotlib.pyplot as plt
import numpy as np

from material_fingerprinting.Experiment import Experiment

class Fingerprints():
    """
    An object of this class is a database of material fingerprints for one material.
    The attributes of this database are for example the number of fingerprints, the material and the considered experiments.
    The methods describe for example rules how the fingerprints should be generated.
    """
    
    def __init__(self,experiment_list,material,parameter_min=0.1,parameter_max=10,n_fingerprints=100):
        
        if not isinstance(experiment_list, list):
            if isinstance(experiment_list, Experiment):
                experiment_list = [experiment_list]
            else:
                raise TypeError("experiment_list must be a list of Experiment objects.")

        self.experiment_list = experiment_list
        self.n_experiments = len(experiment_list)
        self.material = material
        self.parameter_min = parameter_min
        self.parameter_max = parameter_max
        self.n_fingerprints = n_fingerprints
        self.parameters = None
        self.fingerprints_list = []
        
        self.set_parameters()
        self.compute_fingerprints()

    def set_parameters(self):
        range_positive = np.linspace(self.parameter_min,self.parameter_max,self.n_fingerprints)
        range_Gent = np.linspace(1/1000,1/10,self.n_fingerprints)
        range_Ogden = np.linspace(self.parameter_min,self.parameter_max/2,int(self.n_fingerprints/2))
        # we may also set parameters on a logarithmic scale
        # self.parameters[:,1] = np.logspace(-1,1,self.n_fingerprints)

        if self.material.n_parameters == 1:
            self.n_fingerprints = 1
            self.parameters = np.array([[1.0]])
        elif self.material.n_parameters == 2:
            self.parameters = np.zeros((self.n_fingerprints,self.material.n_parameters))
            self.parameters[:,0] = np.ones(self.n_fingerprints)
            if self.material.name == "Demiray - incompressible":
                self.parameters[:,1] = range_positive
            elif self.material.name == "Gent - incompressible":
                self.parameters[:,1] = range_Gent
            elif self.material.name == "Holzapfel - incompressible":
                self.parameters[:,1] = range_positive
            elif self.material.name == "Mooney-Rivlin - incompressible":
                self.parameters[:,1] = range_positive
            elif self.material.name == "Ogden - incompressible":
                self.parameters[:,1] = np.concatenate((-range_Ogden[::-1], range_Ogden))
            elif self.material.name == "Yeoh quadratic - incompressible":
                self.parameters[:,1] = range_positive
            else:
                raise ValueError("Parameter ranges are not implemented for this material.")

    def compute_fingerprints(self):
        for exp in self.experiment_list:
            fingerprints = np.zeros((self.n_fingerprints,exp.n_steps))
            for i in range(self.n_fingerprints):
                fingerprints[i,:] = self.material.conduct_experiment(exp,parameters=self.parameters[i,:])
            self.fingerprints_list.append(fingerprints)

        # if self.experiment.n_experiment == 1:
        #     for i in range(self.n_fingerprints):
        #         self.fingerprints[i,:] = self.material.conduct_experiment(self.experiment,parameters=self.parameters[i,:])
        # elif self.experiment.n_experiment > 1:
        #     for i in range(self.n_fingerprints):
        #         self.fingerprints[i,:] = self.material.conduct_experiment_union(self.experiment,parameters=self.parameters[i,:])

    # def normalize(self):
    #     # Assumption: The fingerprints have the physical dimension of a force.
    #     # We choose the unit of the force, such that the fingerprints are normalized.
    #     fingerprint_norms = np.linalg.norm(self.fingerprints, axis=1, keepdims=True)
    #     self.parameters_normalized = self.parameters.copy()
    #     self.parameters_normalized[:,self.material.homogeneity_parameters] /= fingerprint_norms
    #     self.fingerprints_normalized = self.fingerprints / fingerprint_norms
    
    # def plot_fingerprints(self,normalized=False):

    #     if normalized:
    #         y_data = self.fingerprints_normalized
    #     else:
    #         y_data = self.fingerprints

    #     for i in range(self.n_fingerprints):
    #         plt.plot(self.experiment.control, y_data[i])
        
    #     if self.experiment.n_experiment == 1:
    #         plt.xlabel(self.experiment.control_str[0])
    #         plt.ylabel(self.experiment.measurement_str[0])
    #     else:
    #         plt.xlabel("Fingerprint Dimensions")
    #         plt.ylabel("Fingerprint Amplitudes")

    #     plt.show()
        
    def delete(self):
        for attr in list(self.__dict__):
            delattr(self, attr)
        del self








	
        
    
        
        
        