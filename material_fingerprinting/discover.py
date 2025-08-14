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

from material_fingerprinting.Database import Database
from material_fingerprinting.Experiment import Experiment
from material_fingerprinting.Material import Material

def discover(measurement,verbose=True,plot=True):

    if verbose:
        print("Material Fingerprinting (Beta)")
        print("Contact moritz.flaschel@fau.de for help and error reports.\n")

    if measurement["experiment"] == "UTCSS":

        if verbose: print("Experiment: uniaxial tension/compression and simple shear")

        # database
        db = Database().load("DB_UTCSS.npz")

        if verbose:
            print("Database:")
            print("    number of fingerprints = " + str(db.db_fingerprints.shape[0]))
            print("    smallest stretch = " + str(db.experiment_controls[0].min()))
            print("    greatest stretch = " + str(db.experiment_controls[0].max()))
            print("    smallest shear = " + str(db.experiment_controls[1].min()))
            print("    greatest shear = " + str(db.experiment_controls[1].max()))

        # preprocessing
        if ("F11" not in measurement) or ("P11" not in measurement) or ("F12" not in measurement) or ("P12" not in measurement):
            raise ValueError("This experimental setup requires np arrays F11, P11, F12, and P12.")
        F11 = measurement["F11"].squeeze()
        P11 = measurement["P11"].squeeze()
        F12 = measurement["F12"].squeeze()
        P12 = measurement["P12"].squeeze()
        if len(F11) != len(P11):
            raise ValueError("F11 and P11 must have the same dimension.")
        if len(F12) != len(P12):
            raise ValueError("F12 and P12 must have the same dimension.")
        f1 = np.interp(db.experiment_controls[0], F11, P11, left=0.0, right=0.0)
        f2 = np.interp(db.experiment_controls[1], F12, P12, left=0.0, right=0.0)
        f = np.concatenate([f1,f2])

        # Material Fingerprinting
        print("\nMaterial Fingerprinting:")
        id, model_disc, parameters_disc = db.discover(f,verbose=True)

        # plot
        if plot:
            mat = Material(name=model_disc)
            exp1 = Experiment(mode="uniaxial tension - finite strain",control_min=F11.min(),control_max=F11.max())
            exp2 = Experiment(mode="simple shear - finite strain",control_min=F12.min(),control_max=F12.max())
            P11_disc = mat.conduct_experiment(exp1,parameters = parameters_disc).squeeze()
            P12_disc = mat.conduct_experiment(exp2,parameters = parameters_disc).squeeze()

            fig, ax = plt.subplots(1,2,figsize=(10,5))
            fig.suptitle("Discovered model: " + model_disc + " \n$W=$" + mat.get_formula(parameters_disc))
            s = 15
            ax[0].scatter(F11, P11, color="black", s=s, label='Data')
            ax[0].plot(exp1.control, P11_disc, color="red", linewidth=2, label='Discovered')
            ax[0].set_title("Uniaxial Tension")
            ax[0].set_xlabel(exp1.control_str[0])
            ax[0].set_ylabel(exp1.measurement_str[0])
            ax[0].legend()
            ax[1].scatter(F12, P12, color="black", s=s, label='Data')
            ax[1].plot(exp2.control, P12_disc, color="red", linewidth=2, label='Discovered')
            ax[1].set_title("Simple Shear")
            ax[1].set_xlabel(exp2.control_str[0])
            ax[1].set_ylabel(exp2.measurement_str[0])
            for a in ax:
                a.grid(True)
                a.minorticks_on() 
                a.grid(True, which='minor', linestyle='--', color='lightgray', linewidth=0.5)
            fig.tight_layout()
            plt.show()

    else:
        raise NotImplementedError("This experimental setup is not yet implemented.")
