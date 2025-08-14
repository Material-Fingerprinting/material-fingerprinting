"""
                           
 _|      _|      _|_|_|_|  
 _|_|  _|_|      _|        
 _|  _|  _|      _|_|_|    
 _|      _|      _|        
 _|      _|  _|  _|    _|  
                           
 Material        Fingerprinting

"""

from matplotlib import pyplot as plt
import numpy as np

class Experiment():
    """
    An object of this class is an experiment.
    The attributes of this experiment describe the loading mode, the control variables of the experiment,
    and what is measured during the experiments.
    """
    
    def __init__(self,mode="uniaxial tension - finite strain",control_min=None,control_max=None,n_steps=15):
        
        self.n_experiment = 1
        self.mode = mode
        self.control_min = control_min
        self.control_max = control_max
        self.n_steps = n_steps
        self.fingerprint_idx = [0,self.n_steps] # indices of the experiments measurements in the fingerprint
        self.set_experiment()

    def set_experiment(self):
        if self.mode == "uniaxial tension - finite strain":
            self.dim_measurement = 1
            if self.control_min is None:
                self.control_min = 1.0
            if self.control_max is None:
                self.control_max = 1.5
            self.control = np.linspace(self.control_min,self.control_max,self.n_steps)
            # self.control_str = [r"$\\lambda$"]
            self.control_str = [r"$F_{11}$"]
            self.measurement_str = [r"$P_{11}$"]
        elif self.mode == "simple shear - finite strain":
            self.dim_measurement = 1
            if self.control_min is None:
                self.control_min = 0.01
            if self.control_max is None:
                self.control_max = 0.5
            self.control = np.linspace(self.control_min,self.control_max,self.n_steps)
            # self.control_str = [r"$\\gamma$"]
            self.control_str = [r"$F_{12}$"]
            self.measurement_str = [r"$P_{12}$"]
        else:
            raise ValueError("This experiment is not defined.")
        self.measurement = np.zeros_like(self.control)
        
    def set_fingerprint_idx(self,fingerprint_idx):
        self.fingerprint_idx = fingerprint_idx

    def conduct_experiment(self,material,parameters):
        self.measurement = material.conduct_experiment(self,parameters).reshape(-1)

    def plot(self):
        plt.plot(self.control,self.measurement)
        plt.xlabel(self.control_str[0])
        plt.ylabel(self.measurement_str[0])
        plt.tight_layout()
        plt.show()








	
        
    
        
        
        