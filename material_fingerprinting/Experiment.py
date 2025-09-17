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
    
    def __init__(self,name="uniaxial tension/compression",control_min=None,control_max=None,n_steps=100):
        
        self.n_experiment = 1
        self.name = name
        self.control_min = control_min
        self.control_max = control_max
        self.n_steps = n_steps
        self.fingerprint_idx = [0,self.n_steps] # indices of the experiments measurements in the fingerprint
        self.control = None
        self.measurement = None
        self.dim_measurement = None
        self.control_str = None
        self.measurement_str = None
        
        self.set_experiment()

    def set_experiment(self):

        match self.name:
            case "uniaxial tension/compression":
                self.dim_measurement = 1
                if self.control_min is None:
                    self.control_min = 0.5
                if self.control_max is None:
                    self.control_max = 2.0
                if self.control_min <= 0.0 or self.control_max <= 0.0:
                    raise ValueError("The control must be greater than zero for " + self.name + ".")
                self.control = np.linspace(self.control_min,self.control_max,self.n_steps)
                # self.control_str = [r"$\\lambda$"]
                self.control_str = [r"$F_{11}$"]
                self.measurement_str = [r"$P_{11}$"]
            case "simple shear":
                self.dim_measurement = 1
                if self.control_min is None:
                    self.control_min = 0.0
                if self.control_max is None:
                    self.control_max = 1.0
                self.control = np.linspace(self.control_min,self.control_max,self.n_steps)
                # self.control_str = [r"$\\gamma$"]
                self.control_str = [r"$F_{12}$"]
                self.measurement_str = [r"$P_{12}$"]
            case "pure shear":
                self.dim_measurement = 1
                if self.control_min is None:
                    self.control_min = 0.5
                if self.control_max is None:
                    self.control_max = 2.0
                if self.control_min <= 0.0 or self.control_max <= 0.0:
                    raise ValueError("The control must be greater than zero for " + self.name + ".")
                self.control = np.linspace(self.control_min,self.control_max,self.n_steps)
                # self.control_str = [r"$\\lambda$"]
                self.control_str = [r"$F_{11}$"]
                self.measurement_str = [r"$P_{11}$"]
            case "equibiaxial tension/compression":
                self.dim_measurement = 1
                if self.control_min is None:
                    self.control_min = 0.5
                if self.control_max is None:
                    self.control_max = 2.0
                if self.control_min <= 0.0 or self.control_max <= 0.0:
                    raise ValueError("The control must be greater than zero for " + self.name + ".")
                self.control = np.linspace(self.control_min,self.control_max,self.n_steps)
                # self.control_str = [r"$\\lambda$"]
                self.control_str = [r"$F_{11}=F_{22}$"]
                self.measurement_str = [r"$P_{11}=P_{22}$"]
            case _:
                raise NotImplementedError(
                    "This experimental setup is not implemented."
                    "\nAvailable experimental setups: "
                    "\n    uniaxial tension/compression"
                    "\n    simple shear"
                    "\n    pure shear"
                    "\n    equibiaxial tension/compression"
                )
        self.measurement = np.zeros_like(self.control)

    def set_control(self,control):
        self.control_min = np.min(control)
        self.control_max = np.max(control)
        self.control = control
        self.n_steps = len(control)
        self.fingerprint_idx = [0,self.n_steps]
        
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








	
        
    
        
        
        