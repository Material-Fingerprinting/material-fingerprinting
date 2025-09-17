"""
                           
 _|      _|      _|_|_|_|  
 _|_|  _|_|      _|        
 _|  _|  _|      _|_|_|    
 _|      _|      _|        
 _|      _|  _|  _|    _|  
                           
 Material        Fingerprinting

"""

import numpy as np

from material_fingerprinting.Kinematics import *

CLIP_EXP = 20

class Material():
    """
    An object of this class is a material.
    The attributes of this material are for example its parameters and their physical dimensions.
    The methods describe how the material responds in different experiments.
    """
    
    def __init__(self,name="Mooney-Rivlin - incompressible"):
        
        self.name = name
        self.set_material()

    def set_material(self):
        # sorted in alphabetical order
        if self.name == "Blatz-Ko - incompressible":
            self.n_parameters = 1
            self.homogeneity_parameters = np.array([True], dtype=bool)
            self.dim_parameters = ["force/area"]
        elif self.name == "Demiray - incompressible":
            self.n_parameters = 2
            self.homogeneity_parameters = np.array([True, False], dtype=bool)
            self.dim_parameters = ["force/area", "dimensionless"]
        elif self.name == "Gent - incompressible":
            self.n_parameters = 2
            self.homogeneity_parameters = np.array([True, False], dtype=bool)
            self.dim_parameters = ["force/area", "dimensionless"]
        elif self.name == "Holzapfel - incompressible":
            self.n_parameters = 2
            self.homogeneity_parameters = np.array([True, False], dtype=bool)
            self.dim_parameters = ["force/area", "dimensionless"]
        elif self.name == "Mooney-Rivlin - incompressible":
            self.n_parameters = 2
            self.homogeneity_parameters = np.array([True] * self.n_parameters, dtype=bool)
            self.dim_parameters = ["force/area"] * self.n_parameters
        elif self.name == "Neo-Hooke - incompressible":
            self.n_parameters = 1
            self.homogeneity_parameters = np.array([True], dtype=bool)
            self.dim_parameters = ["force/area"]
        elif self.name == "Ogden - incompressible":
            self.n_parameters = 2
            self.homogeneity_parameters = np.array([True, False], dtype=bool)
            self.dim_parameters = ["force/area", "dimensionless"]
        elif self.name == "Yeoh quadratic - incompressible":
            self.n_parameters = 2
            self.homogeneity_parameters = np.array([True] * self.n_parameters, dtype=bool)
            self.dim_parameters = ["force/area"] * self.n_parameters
        
        else:
            raise ValueError("This material is not defined.")
        
    def scale_parameters(self,parameters,factor):
        parameters = parameters.copy()
        parameters[self.homogeneity_parameters] *= factor
        return parameters
    
    def get_strain_energy_density_incompressible_I1I2(self,parameters,I1,I2):

        if len(parameters) != self.n_parameters:
            raise ValueError("Inconsistent number of parameters.")
        
        # sorted in alphabetical order
        if self.name == "Blatz-Ko - incompressible":
            W = parameters[0] * (I2 - 3)
        
        elif self.name == "Demiray - incompressible":
            W = parameters[0] * (np.exp(parameters[1] * (I1 - 3)) - 1)

        elif self.name == "Gent - incompressible":
            # the Gent model is a simple and accurate approximation of the Arruda–Boyce model
            # the Gent model has a singularity at 1 = parameters[1] * (I1-3)
            W = - parameters[0] * (np.ln(1 - (I1-3) * parameters[1]))

        elif self.name == "Holzapfel - incompressible":
            W = parameters[0] * (np.exp(parameters[1] * (I1 - 3)**2) - 1)

        elif self.name == "Mooney-Rivlin - incompressible":
            W = parameters[0] * (I1 - 3) + parameters[1] * (I2 - 3)

        elif self.name == "Neo-Hooke - incompressible":
            W = parameters[0] * (I1 - 3)

        elif self.name == "Ogden - incompressible":
            raise NotImplementedError("The strain energy density of the Ogden model does not depend on I1 and I2.")

        elif self.name == "Yeoh quadratic - incompressible":
            W = parameters[0] * (I1 - 3) + parameters[1] * (I1 - 3)**2

        return W
    
    def get_strain_energy_density_incompressible_lam(self,parameters,lam1,lam2):
        lam3 = 1.0 / (lam1 * lam2)
        I1 = lam1**2 + lam2**2 + lam3**2
        I2 = lam1**2 * lam2**2 + lam2**2 * lam3**2 + lam1**2 * lam3**2

        if len(parameters) != self.n_parameters:
            raise ValueError("Inconsistent number of parameters.")

        if self.name == "Ogden - incompressible":
            W = parameters[0] * (lam1**parameters[1] + lam2**parameters[1] + lam3**parameters[1] - 3)
        else:
            W = self.get_strain_energy_density_incompressible_I1I2(parameters,I1,I2)

        return W
        
    def conduct_experiment(self,experiment,parameters):
        if len(parameters) != self.n_parameters:
            raise ValueError("Inconsistent number of parameters.")
        if experiment.n_experiment != 1:
            raise ValueError("This method is only implemented for a single experiment and not for a union of experiments.")
        
        measurement = np.zeros((experiment.dim_measurement,experiment.n_steps))

        # sorted in alphabetical order
        if self.name == "Blatz-Ko - incompressible":
            # W = parameters[0] * (I2 - 3)
            I2 = compute_I2(experiment.control,format=experiment.name)
            dI2 = compute_I2_derivative(experiment.control,format=experiment.name)
            dW_dI2 = parameters[0]
            measurement[:] = dW_dI2 * dI2
        
        elif self.name == "Demiray - incompressible":
            # W = parameters[0] * (exp(parameters[1] * (I1 - 3)) - 1)
            I1 = compute_I1(experiment.control,format=experiment.name)
            dI1 = dI1 = compute_I1_derivative(experiment.control,format=experiment.name)
            # to avoid numerical overflow, we clip the argument of the exponential function
            argument = np.clip(parameters[1] * (I1 - 3.0), -CLIP_EXP, CLIP_EXP)
            mask = ~((argument > -CLIP_EXP) & (argument < CLIP_EXP))
            dW_dI1 = parameters[0] * parameters[1] * np.exp(argument)
            result = dW_dI1 * dI1
            if np.any(mask): result[mask] = np.sign(result[mask])*np.max(np.abs(result))
            measurement[:] = result

        elif self.name == "Gent - incompressible":
            # the Gent model is a simple and accurate approximation of the Arruda–Boyce model
            # the Gent model has a singularity at 1 = parameters[1] * (I1-3)
            # W = - parameters[0] * (ln(1 - (I1-3) * parameters[1]))
            I1 = compute_I1(experiment.control,format=experiment.name)
            dI1 = compute_I1_derivative(experiment.control,format=experiment.name)
            dW_dI1 = (parameters[0] * parameters[1]) / (1 - (I1-3) * parameters[1])
            measurement[:] = dW_dI1 * dI1

        elif self.name == "Holzapfel - incompressible":
            # W = parameters[0] * (exp(parameters[1] * (I1 - 3)**2) - 1)
            I1 = compute_I1(experiment.control,format=experiment.name)
            dI1 = dI1 = compute_I1_derivative(experiment.control,format=experiment.name)
            # to avoid numerical overflow, we clip the argument of the exponential function
            argument = np.clip(parameters[1] * (I1 - 3.0)**2, -CLIP_EXP, CLIP_EXP)
            mask = ~((argument > -CLIP_EXP) & (argument < CLIP_EXP))
            dW_dI1 = 2 * parameters[0] * parameters[1] * (I1 - 3.0) * np.exp(argument)
            result = dW_dI1 * dI1
            if np.any(mask): result[mask] = np.sign(result[mask])*np.max(np.abs(result))
            measurement[:] = result

        elif self.name == "Mooney-Rivlin - incompressible":
            # W = parameters[0] * (I1 - 3) + parameters[1] * (I2 - 3)
            I1 = compute_I1(experiment.control,format=experiment.name)
            dI1 = compute_I1_derivative(experiment.control,format=experiment.name)
            I2 = compute_I2(experiment.control,format=experiment.name)
            dI2 = compute_I2_derivative(experiment.control,format=experiment.name)
            dW_dI1 = parameters[0]
            dW_dI2 = parameters[1]
            measurement[:] = dW_dI1 * dI1 + dW_dI2 * dI2

        elif self.name == "Neo-Hooke - incompressible":
            # W = parameters[0] * (I1 - 3)
            I1 = compute_I1(experiment.control,format=experiment.name)
            dI1 = compute_I1_derivative(experiment.control,format=experiment.name)
            dW_dI1 = parameters[0]
            measurement[:] = dW_dI1 * dI1

        elif self.name == "Ogden - incompressible" and experiment.name == "uniaxial tension/compression":
            # W = parameters[0] * (lam1**parameters[1] + lam2**parameters[1] + lam3**parameters[1] - 3)
            dQ_dlamda = parameters[1] * np.power(experiment.control,parameters[1]-1.0) - parameters[1] * np.power(experiment.control,-parameters[1]/2.0-1.0)
            measurement[:] = parameters[0] * dQ_dlamda
        elif self.name == "Ogden - incompressible" and experiment.name == "simple shear":
            # C_bar = 1 + 1.0/2.0 * experiment.control**2.0
            # C_aux = np.sqrt(C_bar**2.0 - 1.0)
            mask = ~np.isclose(experiment.control, 0.0)
            dQ_dC1 = np.zeros_like(experiment.control)
            dQ_dC2 = np.zeros_like(experiment.control)
            C_bar = 1 + 1.0/2.0 * experiment.control[mask]**2.0
            C_aux = np.sqrt(C_bar**2.0 - 1.0)
            # dQ_dC1 = parameters[1]/2.0 * np.power(C_bar - C_aux,parameters[1]/2.0-1.0) * (1.0 - C_bar/C_aux) # own derivation
            # dQ_dC2 = parameters[1]/2.0 * np.power(C_bar + C_aux,parameters[1]/2.0-1.0) * (1.0 + C_bar/C_aux) # own derivation
            dQ_dC1[mask] = - parameters[1]*np.power(C_bar - C_aux,parameters[1]/2.0) / (2.0*C_aux) # Wolfram
            dQ_dC2[mask] = parameters[1]*np.power(C_bar + C_aux,parameters[1]/2.0) / (2.0*C_aux) # Wolfram
            measurement[:] = parameters[0] * experiment.control * (dQ_dC1 + dQ_dC2)
        elif self.name == "Ogden - incompressible" and experiment.name == "pure shear":
            dQ_dlamda = parameters[1] * np.power(experiment.control,parameters[1]-1.0) - parameters[1] * np.power(experiment.control,-parameters[1]-1.0)
            measurement[:] = parameters[0] * dQ_dlamda
        elif self.name == "Ogden - incompressible" and experiment.name == "equibiaxial tension/compression":
            dQ_dlamda = parameters[1] * np.power(experiment.control,parameters[1]-1.0) - parameters[1] * np.power(experiment.control,-2.0*parameters[1]-1.0)
            measurement[:] = parameters[0] * dQ_dlamda

        elif self.name == "Yeoh quadratic - incompressible":
            # W = parameters[0] * (I1 - 3) + parameters[1] * (I1 - 3)**2
            I1 = compute_I1(experiment.control,format=experiment.name)
            dI1 = compute_I1_derivative(experiment.control,format=experiment.name)
            dW_dI1 = parameters[0] + 2.0 * parameters[1] * (I1 - 3.0)
            measurement[:] = dW_dI1 * dI1

        else:
            raise ValueError("This combination of experiment and material is not implemented.")
        
        return measurement
    
    def conduct_experiment_union(self,experiment_union,parameters):
        measurement = np.zeros((1,experiment_union.n_steps))
        for exp in experiment_union.experiment_list:
            measurement[0,exp.fingerprint_idx[0]:exp.fingerprint_idx[1]] = self.conduct_experiment(exp,parameters)
        return measurement
    
    def get_formula(self,parameters,format="latex"):
        if len(parameters) != self.n_parameters:
            raise ValueError("Inconsistent number of parameters.")
        
        if format == "latex":
            # sorted in alphabetical order
            if self.name == "Blatz-Ko - incompressible":
                W = f"${parameters[0]:.4f} [I_2 - 3] - p [J-1]$"
            elif self.name == "Demiray - incompressible":
                W = f"${parameters[0]:.4f} \\left[\\exp({parameters[1]:.4f} [I_1 - 3]) - 1\\right] - p [J-1]$"
            elif self.name == "Gent - incompressible":
                W = f"$- {parameters[0]:.4f} \\left[\\ln(1 - {parameters[1]:.4f} [I_1 - 3])\\right] - p [J-1]$"
            elif self.name == "Holzapfel - incompressible":
                W = f"${parameters[0]:.4f} \\left[\\exp({parameters[1]:.4f} [I_1 - 3]^2) - 1\\right] - p [J-1]$"
            elif self.name == "Mooney-Rivlin - incompressible":
                W = f"${parameters[0]:.4f} [I_1 - 3] + {parameters[1]:.4f} [I_2 - 3] - p [J-1]$"
            elif self.name == "Neo-Hooke - incompressible":
                W = f"${parameters[0]:.4f} [I_1 - 3] - p [J-1]$"
            elif self.name == "Ogden - incompressible":
                W = f"${parameters[0]:.4f} [\\lambda_1^" + "{" + f"{parameters[1]:.4f}" + "}" + f" + \\lambda_2^" + "{" + f"{parameters[1]:.4f}" + "}" + f" + \\lambda_3^" + "{" + f"{parameters[1]:.4f}" + "}" + f" - 3] - p [J-1]$"
            else:
                raise ValueError("The formula for this material is not implemented.")
        return W

