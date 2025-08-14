"""
                           
 _|      _|      _|_|_|_|  
 _|_|  _|_|      _|        
 _|  _|  _|      _|_|_|    
 _|      _|      _|        
 _|      _|  _|  _|    _|  
                           
 Material        Fingerprinting

"""

import importlib.resources
import matplotlib.pyplot as plt
import numpy as np

from material_fingerprinting.Material import Material

class Database():
    """
    An object of this class is a database of material fingerprints for multiple different materials.
    The attributes of this material are for example its parameters and their dimensions.
    The methods describe how the material responds in different experiments.
    """
    
    def __init__(self,experiment_name=None,experiment_controls=None):
        
        self.experiment_name = experiment_name
        self.experiment_controls = experiment_controls

        self.db_model_names = []
        self.db_model_ids = []
        self.db_parameters = None
        self.db_homogeneity_parameters = None
        self.db_fingerprints = None
        self.n_parameters_max = 0

    def append(self,fb):

        if fb.material.n_parameters > self.n_parameters_max:
            self.n_parameters_max = fb.material.n_parameters

        if len(self.db_model_names) == 0:
            id = 0
            self.db_parameters = np.zeros((0,self.n_parameters_max))
            self.db_homogeneity_parameters = np.zeros((0,self.n_parameters_max), dtype=bool)
            self.db_fingerprints = np.zeros((0,fb.fingerprints_normalized.shape[1]))
        else:
            id = self.db_model_ids[-1] + 1
        
        if fb.fingerprints_normalized.shape[1] != self.db_fingerprints.shape[1]:
            raise ValueError("Invalid number of data points in fingerprint.")

        self.db_model_names += [fb.material.name]
        self.db_model_ids += [id] * fb.n_fingerprints

        new_homogeneity_parameters = np.tile(fb.material.homogeneity_parameters, (fb.parameters_normalized.shape[0], 1))
        if fb.parameters_normalized.shape[1] == self.db_parameters.shape[1]:
            self.db_parameters = np.concatenate((self.db_parameters,fb.parameters_normalized),axis=0)
            self.db_homogeneity_parameters = np.concatenate((self.db_homogeneity_parameters,new_homogeneity_parameters),axis=0)
        else:
            db_parameters_pad = self.pad_array(self.db_parameters)
            parameters_normalized_pad = self.pad_array(fb.parameters_normalized)
            self.db_parameters = np.concatenate((db_parameters_pad,parameters_normalized_pad),axis=0)
            db_homogeneity_parameters_pad = self.pad_array(self.db_homogeneity_parameters)
            homogeneity_parameters_pad = self.pad_array(new_homogeneity_parameters)
            self.db_homogeneity_parameters = np.concatenate((db_homogeneity_parameters_pad,homogeneity_parameters_pad),axis=0)

        self.db_fingerprints = np.concatenate((self.db_fingerprints,fb.fingerprints_normalized),axis=0)

    def pad_array(self,array):
        if array.shape[1] < self.n_parameters_max:
            if array.dtype == bool:
                pad = np.full((array.shape[0], self.n_parameters_max - array.shape[1]), False)
            else:
                pad = np.full((array.shape[0], self.n_parameters_max - array.shape[1]), np.nan)
            return np.hstack([array, pad])
        else:
            return array

    def discover(self,measurement,verbose=True):
        mask = ~np.isclose(measurement, 0)
        measurement = measurement[mask]
        measurement_norm = np.linalg.norm(measurement)
        measurement_normalized = measurement / measurement_norm
        fingerprints = self.db_fingerprints[:,mask]
        fingerprints_norms = np.linalg.norm(fingerprints, axis=1, keepdims=True)
        fingerprints_normalized = fingerprints / fingerprints_norms
        paramters_normalized = self.db_parameters.copy()
        temp = self.db_parameters.copy() / fingerprints_norms
        paramters_normalized[self.db_homogeneity_parameters] = temp[self.db_homogeneity_parameters]
        correlations = fingerprints_normalized @ measurement_normalized
        id = np.argmax(correlations)
        material = Material(self.db_model_names[self.db_model_ids[id]])
        parameters = paramters_normalized[id][~np.isnan(paramters_normalized[id])]
        parameters = material.scale_parameters(parameters,measurement_norm)
        if verbose:
            print("    discovered model: " + self.db_model_names[self.db_model_ids[id]])
            print("    identified parameters: " + str(parameters))
            print("    formula: " + material.get_formula(parameters))
        return id, self.db_model_names[self.db_model_ids[id]], parameters
    
    def save(self,path=None):
        if path is None: path = "material_fingerprinting/databases/DB_" + self.experiment_name + ".npz"
        np.savez(
            path,
            experiment_name = self.experiment_name,
            experiment_controls = self.experiment_controls,
            model_names = self.db_model_names,
            model_ids = self.db_model_ids,
            parameters = self.db_parameters,
            homogeneity_parameters = self.db_homogeneity_parameters,
            fingerprints = self.db_fingerprints,
            )
    
    def load(self,name):
        data_path = importlib.resources.files("material_fingerprinting.databases").joinpath(name)
        with data_path.open('rb') as f:
            database = np.load(f)
            self.experiment_name = database["experiment_name"]
            self.experiment_controls = database["experiment_controls"]
            self.db_model_names = database["model_names"]
            self.db_model_ids = database["model_ids"]
            self.db_parameters = database["parameters"]
            self.db_homogeneity_parameters = database["homogeneity_parameters"]
            self.db_fingerprints = database["fingerprints"]
            self.n_parameters_max = database["parameters"].shape[1]
        return self

    def plot_fingerprints(self):
        for i in range(self.db_fingerprints.shape[0]):
            plt.plot(np.arange(self.db_fingerprints.shape[1]) + 1, self.db_fingerprints[i,:])
        plt.xlabel("Fingerprint Dimensions")
        plt.ylabel("Fingerprint Amplitudes")
        plt.show()

    





	
        
    
        
        
        