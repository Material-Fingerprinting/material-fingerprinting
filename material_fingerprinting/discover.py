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
import warnings

from material_fingerprinting.Database import Database
from material_fingerprinting.Experiment import Experiment
from material_fingerprinting.Material import Material

def discover(measurement,verbose=True,first=True,plot=True):

    if verbose and first:
        print("\n=== Material Fingerprinting ===")
        print("Contact moritz.flaschel@fau.de for help and bug reports.\n")

    match measurement["experiment"]:

        case "UTC" | "UT" | "UC":
            # check data availability
            if ("F11" not in measurement) or ("P11" not in measurement):
                raise ValueError("This experimental setup requires numpy arrays F11 and P11. Either F11 or P11 is missing.")
            F11 = measurement["F11"].reshape(-1)
            P11 = measurement["P11"].reshape(-1)
            if len(F11) == 0 or (len(F11) == 1 and np.isclose(F11[0],1.0)):
                raise ValueError("This experimental setup requires numpy arrays F11 and P11. F11 and P11 do not contain enough data.")

            if verbose: print("Experiment: uniaxial tension/compression")

            # database
            db = Database().load("DB_UTCSS.npz")
            if verbose:
                print("Database:")
                print("    number of fingerprints = " + str(db.db_fingerprints.shape[0]))
                print("    smallest stretch = " + str(db.experiment_controls[0].min()))
                print("    greatest stretch = " + str(db.experiment_controls[0].max()))

            # preprocessing
            if len(F11) != len(P11):
                raise ValueError("F11 and P11 must have the same dimension.")
            if 1.0 not in F11:
                F11 = np.append(F11, 1.0)
                P11 = np.append(P11, 0.0)
            sort = np.argsort(F11)
            F11 = F11[sort]
            P11 = P11[sort]
            f1 = np.interp(db.experiment_controls[0], F11, P11, left=0.0, right=0.0)
            f2 = np.zeros_like(db.experiment_controls[1])
            f = np.concatenate([f1,f2])

            # Material Fingerprinting
            print("\nMaterial Fingerprinting:")
            id, model_disc, parameters_disc = db.discover(f,verbose=True)

            # plot
            if plot:
                mat = Material(name=model_disc)
                r = 0.05
                exp1 = Experiment(mode="uniaxial tension - finite strain",control_min=F11.min()-r*np.abs(F11).max(),control_max=F11.max()+r*np.abs(F11).max())
                P11_disc = mat.conduct_experiment(exp1,parameters = parameters_disc).squeeze()

                fig, ax = plt.subplots(1,1,figsize=(6,5))
                fig.suptitle("Discovered model: " + model_disc + " \n$W=$" + mat.get_formula(parameters_disc))
                s = 15
                ax.scatter(F11, P11, color="black", s=s, label='Data')
                ax.plot(exp1.control, P11_disc, color="red", linewidth=2, label='Discovered')
                ax.set_title("Uniaxial Tension")
                ax.set_xlabel(exp1.control_str[0])
                ax.set_ylabel(exp1.measurement_str[0])
                ax.legend()
                ax.grid(True)
                ax.minorticks_on() 
                ax.grid(True, which='minor', linestyle='--', color='lightgray', linewidth=0.5)
                fig.tight_layout()
                plt.show()

        case "SS":
            # check data availability
            if ("F12" not in measurement) or ("P12" not in measurement):
                raise ValueError("This experimental setup requires numpy arrays F12 and P12. Either F12 or P12 is missing.")
            F12 = measurement["F12"].reshape(-1)
            P12 = measurement["P12"].reshape(-1)
            if len(F12) == 0 or (len(F12) == 1 and np.isclose(F12[0],0.0)):
                raise ValueError("This experimental setup requires numpy arrays F12 and P12. F12 and P12 do not contain enough data.")
            
            if verbose: print("Experiment: simple shear")

            # database
            db = Database().load("DB_UTCSS.npz")
            if verbose:
                print("Database:")
                print("    number of fingerprints = " + str(db.db_fingerprints.shape[0]))
                print("    smallest shear = " + str(db.experiment_controls[1].min()))
                print("    greatest shear = " + str(db.experiment_controls[1].max()))

            # preprocessing
            if len(F12) != len(P12):
                raise ValueError("F12 and P12 must have the same dimension.")
            if 0.0 not in F12:
                F12 = np.append(F12, 0.0)
                P12 = np.append(P12, 0.0)
            sort = np.argsort(F12)
            F12 = F12[sort]
            P12 = P12[sort]
            f1 = np.zeros_like(db.experiment_controls[0])
            f2 = np.interp(db.experiment_controls[1], F12, P12, left=0.0, right=0.0)
            f = np.concatenate([f1,f2])

            # Material Fingerprinting
            print("\nMaterial Fingerprinting:")
            id, model_disc, parameters_disc = db.discover(f,verbose=True)

            # plot
            if plot:
                mat = Material(name=model_disc)
                r = 0.05
                exp2 = Experiment(mode="simple shear - finite strain",control_min=F12.min()-r*np.abs(F12).max(),control_max=F12.max()+r*np.abs(F12).max())
                P12_disc = mat.conduct_experiment(exp2,parameters = parameters_disc).squeeze()

                fig, ax = plt.subplots(1,1,figsize=(6,5))
                fig.suptitle("Discovered model: " + model_disc + " \n$W=$" + mat.get_formula(parameters_disc))
                s = 15
                ax.scatter(F12, P12, color="black", s=s, label='Data')
                ax.plot(exp2.control, P12_disc, color="red", linewidth=2, label='Discovered')
                ax.set_title("Simple Shear")
                ax.set_xlabel(exp2.control_str[0])
                ax.set_ylabel(exp2.measurement_str[0])
                ax.legend()
                ax.grid(True)
                ax.minorticks_on() 
                ax.grid(True, which='minor', linestyle='--', color='lightgray', linewidth=0.5)
                fig.tight_layout()
                plt.show()

        case "UTCSS":
            # check data availability
            if ("F11" not in measurement) or ("P11" not in measurement):
                warnings.warn("This experimental setup requires numpy arrays F11, P11, F12, P12. Either F11 or P11 is missing. Trying to discover model with only F12, P12.")
                measurement["experiment"] = "SS"
                return discover(measurement,verbose=verbose,first=False,plot=plot)
            F11 = measurement["F11"].reshape(-1)
            P11 = measurement["P11"].reshape(-1)
            if len(F11) == 0 or (len(F11) == 1 and np.isclose(F11[0],1.0)):
                warnings.warn("This experimental setup requires numpy arrays F11, P11, F12, P12. F11 and P11 do not contain enough data. Trying to discover model with only F12, P12.")
                measurement["experiment"] = "SS"
                return discover(measurement,verbose=verbose,first=False,plot=plot)
            if ("F12" not in measurement) or ("P12" not in measurement):
                warnings.warn("This experimental setup requires numpy arrays F11, P11, F12, P12. Either F12 or P12 is missing. Trying to discover model with only F11, P11.")
                measurement["experiment"] = "UTC"
                return discover(measurement,verbose=verbose,first=False,plot=plot)
            F12 = measurement["F12"].reshape(-1)
            P12 = measurement["P12"].reshape(-1)
            if len(F12) == 0 or (len(F12) == 1 and np.isclose(F12[0],0.0)):
                warnings.warn("This experimental setup requires numpy arrays F11, P11, F12, P12. F12 and P12 do not contain enough data. Trying to discover model with only F11, P11.")
                measurement["experiment"] = "UTC"
                return discover(measurement,verbose=verbose,first=False,plot=plot)
            
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
            if len(F11) != len(P11):
                raise ValueError("F11 and P11 must have the same dimension.")
            if 1.0 not in F11:
                F11 = np.append(F11, 1.0)
                P11 = np.append(P11, 0.0)
            sort = np.argsort(F11)
            F11 = F11[sort]
            P11 = P11[sort]
            if len(F12) != len(P12):
                raise ValueError("F12 and P12 must have the same dimension.")
            if 0.0 not in F12:
                F12 = np.append(F12, 0.0)
                P12 = np.append(P12, 0.0)
            sort = np.argsort(F12)
            F12 = F12[sort]
            P12 = P12[sort]
            f1 = np.interp(db.experiment_controls[0], F11, P11, left=0.0, right=0.0)
            f2 = np.interp(db.experiment_controls[1], F12, P12, left=0.0, right=0.0)
            f = np.concatenate([f1,f2])

            # Material Fingerprinting
            print("\nMaterial Fingerprinting:")
            id, model_disc, parameters_disc = db.discover(f,verbose=True)

            # plot
            if plot:
                mat = Material(name=model_disc)
                r = 0.05
                exp1 = Experiment(mode="uniaxial tension - finite strain",control_min=F11.min()-r*np.abs(F11).max(),control_max=F11.max()+r*np.abs(F11).max())
                exp2 = Experiment(mode="simple shear - finite strain",control_min=F12.min()-r*np.abs(F12).max(),control_max=F12.max()+r*np.abs(F12).max())
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
            
        case _:
            raise NotImplementedError("This experimental setup is not implemented.")
        
    return model_disc, parameters_disc
