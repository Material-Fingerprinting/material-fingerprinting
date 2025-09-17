"""
                           
 _|      _|      _|_|_|_|  
 _|_|  _|_|      _|        
 _|  _|  _|      _|_|_|    
 _|      _|      _|        
 _|      _|  _|  _|    _|  
                           
 Material        Fingerprinting

"""

import numpy as np

class ExperimentUnion():
    """
    An object of this class is a union of multiple experiments, such as for example the combination
    of uniaxial tension/compression and simple shear.
    """
    
    def __init__(self,experiment_list):
        
        self.n_experiment = len(experiment_list)
        if self.n_experiment <= 1:
            raise ValueError("A union of experiments must contain more than one experiment.")
        self.experiment_list = experiment_list

        self.n_steps_list = []
        fingerprint_idx = [0]
        for experiment in self.experiment_list:
            self.n_steps_list.append(experiment.n_steps)
            fingerprint_idx.append(fingerprint_idx[-1] + experiment.n_steps)
            experiment.set_fingerprint_idx([fingerprint_idx[-2],fingerprint_idx[-1]])
        self.n_steps = sum(self.n_steps_list)

        self.control = np.arange(self.n_steps) + 1
        self.measurement = np.zeros_like(self.control)

    def conduct_experiment(self,material,parameters):

        for experiment in self.experiment_list:
            experiment.conduct_experiment(material,parameters)
        self.measurement = material.conduct_experiment(self,parameters)









	
        
    
        
        
        