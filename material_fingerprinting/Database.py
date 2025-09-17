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
import os
import pickle

from material_fingerprinting.Fingerprints import Fingerprints
from material_fingerprinting.Material import Material

class Database():
    """
    An object of this class is a database of material fingerprints for multiple different materials.
    The attributes of this material are for example its parameters and their dimensions.
    The methods describe how the material responds in different experiments.
    """
    
    def __init__(self):
        
        self.experiment_list = None
        self.experiment_name_list = []
        self.experiment_control_list = []
        self.n_experiments = 0
        self.model_name_list = []
        self.model_indices = []
        self.parameters = None
        self.homogeneity_parameters = None
        self.n_parameters_max = 0
        self.fingerprints_list = []

    def append(self,fb):

        if self.experiment_list is None:
            self.experiment_list = fb.experiment_list
            self.experiment_name_list = [exp.name for exp in fb.experiment_list]
            self.experiment_control_list = [exp.control for exp in fb.experiment_list]
            self.n_experiments = len(self.experiment_list)
        elif self.experiment_list != fb.experiment_list:
            raise ValueError("The experiments in the database do not match the fingerprints to be added.")

        if fb.material.n_parameters > self.n_parameters_max:
            self.n_parameters_max = fb.material.n_parameters

        if len(self.model_name_list) == 0:
            id = 0
            self.parameters = np.zeros((0,self.n_parameters_max))
            self.homogeneity_parameters = np.zeros((0,self.n_parameters_max), dtype=bool)
            self.fingerprints_list = [np.zeros((0,fb.fingerprints_list[i].shape[1])) for i in range(self.n_experiments)]
        else:
            id = self.model_indices[-1] + 1
        
        self.model_name_list += [fb.material.name]
        self.model_indices += [id] * fb.n_fingerprints

        new_homogeneity_parameters = np.tile(fb.material.homogeneity_parameters, (fb.parameters.shape[0], 1))
        if fb.parameters.shape[1] == self.parameters.shape[1]:
            self.parameters = np.concatenate((self.parameters,fb.parameters),axis=0)
            self.homogeneity_parameters = np.concatenate((self.homogeneity_parameters,new_homogeneity_parameters),axis=0)
        else:
            self.parameters = np.concatenate((self.pad_array(self.parameters),self.pad_array(fb.parameters)),axis=0)
            self.homogeneity_parameters = np.concatenate((self.pad_array(self.homogeneity_parameters),self.pad_array(new_homogeneity_parameters)),axis=0)

        self.fingerprints_list = [
            np.concatenate((f, g), axis=0)
            for f, g in zip(self.fingerprints_list, fb.fingerprints_list)
        ]
        
    def pad_array(self,array):
        if array.shape[1] < self.n_parameters_max:
            if array.dtype == bool:
                pad = np.full((array.shape[0], self.n_parameters_max - array.shape[1]), False)
            else:
                pad = np.full((array.shape[0], self.n_parameters_max - array.shape[1]), np.nan)
            return np.hstack([array, pad])
        else:
            return array

    def discover(self,measurement):
        mask = ~np.isclose(measurement, 0.0)
        measurement = measurement[mask]
        measurement_norm = np.linalg.norm(measurement)
        measurement_normalized = measurement / measurement_norm
        fingerprints = np.concatenate(self.fingerprints_list, axis=1)[:,mask]
        fingerprints_norms = np.linalg.norm(fingerprints, axis=1, keepdims=True)
        fingerprints_normalized = fingerprints / fingerprints_norms
        paramters_normalized = self.parameters.copy()
        temp = self.parameters.copy() / fingerprints_norms
        paramters_normalized[self.homogeneity_parameters] = temp[self.homogeneity_parameters]
        correlations = fingerprints_normalized @ measurement_normalized
        id = np.argmax(correlations)
        material = Material(self.model_name_list[self.model_indices[id]])
        parameters = paramters_normalized[id][~np.isnan(paramters_normalized[id])]
        parameters = material.scale_parameters(parameters,measurement_norm)
        return id, self.model_name_list[self.model_indices[id]], parameters
    
    def save_npz(self,name,path=None):
        # Save the database to a .npz file.
        if path is None: path = "material_fingerprinting/databases/DB_" + name + ".npz"
        else: path += "DB_" + name + ".npz"
        os.makedirs(os.path.dirname(path), exist_ok=True) # make sure the directory exists
        np.savez(
            path,
            experiment_name_list = self.experiment_name_list,
            experiment_control_list = self.experiment_control_list,
            model_name_list = self.model_name_list,
            model_indices = self.model_indices,
            parameters = self.parameters,
            homogeneity_parameters = self.homogeneity_parameters,
            n_parameters_max = self.n_parameters_max,
            fingerprints_list = self.fingerprints_list,
            )
    
    def load_npz(self,name,verbose=True):
        try:
            with np.load(f"material_fingerprinting/databases/DB_" + name + ".npz") as database:
                self.experiment_name_list = [str(x) for x in database["experiment_name_list"]]
                self.experiment_control_list = list(database["experiment_control_list"])
                self.model_name_list = [str(x) for x in database["model_name_list"]]
                self.model_indices = database["model_indices"]
                self.parameters = database["parameters"]
                self.homogeneity_parameters = database["homogeneity_parameters"]
                self.fingerprints_list = list(database["fingerprints_list"])
                self.n_parameters_max = database["n_parameters_max"]
            if verbose: print("The numpy database is loaded from the local path.")
        except FileNotFoundError:
            data_path = importlib.resources.files("material_fingerprinting.databases").joinpath("DB_" + name + ".npz")
            with data_path.open("rb") as f:
                database = np.load(f)
                self.experiment_name_list = [str(x) for x in database["experiment_name_list"]]
                self.experiment_control_list = list(database["experiment_control_list"])
                self.model_name_list = [str(x) for x in database["model_name_list"]]
                self.model_indices = database["model_indices"]
                self.parameters = database["parameters"]
                self.homogeneity_parameters = database["homogeneity_parameters"]
                self.fingerprints_list = list(database["fingerprints_list"])
                self.n_parameters_max = database["n_parameters_max"]
            if verbose: print("The numpy database is loaded from the package resources.")
        return self
    
    def save_pkl(self,name,path=None):
        # Save the database to a .pkl file.
        if path is None: path = "material_fingerprinting/databases/DB_" + name + ".pkl"
        else: path += "DB_" + name + ".pkl"
        os.makedirs(os.path.dirname(path), exist_ok=True) # make sure the directory exists
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def load_pkl(self,name,verbose=True):
        try:
            with open("material_fingerprinting/databases/DB_" + name + ".pkl", "rb") as f:
                self = pickle.load(f)
            if verbose: print("The pickle database is loaded from the local path.")
        except FileNotFoundError:
            data_path = importlib.resources.files("material_fingerprinting.databases").joinpath("DB_" + name + ".pkl")
            with data_path.open("rb") as f:
                self = pickle.load(f)
            if verbose: print("The pickle database is loaded from the package resources.")
        return self

    # def plot_fingerprints(self):
    #     for i in range(self.db_fingerprints.shape[0]):
    #         plt.plot(np.arange(self.db_fingerprints.shape[1]) + 1, self.db_fingerprints[i,:])
    #     plt.xlabel("Fingerprint Dimensions")
    #     plt.ylabel("Fingerprint Amplitudes")
    #     plt.show()

    





	
        
    
        
        
        