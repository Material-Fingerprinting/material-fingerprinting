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
from material_fingerprinting.Measurement import Measurement

# colors extracted from the tab20 colormap
tab20blue = [31/255, 119/255, 180/255]
tab20red = [214/255, 39/255, 40/255]

def discover(measurement_list, database="HEI", verbose=True, verbose_best_models=False, plot=True):
    if verbose:
        print("\n=== Material Fingerprinting ===")
        print("Contact moritz.flaschel@fau.de for help and bug reports.\n")

    # Check data
    if not isinstance(measurement_list, list):
        if isinstance(measurement_list, Measurement):
            measurement_list = [measurement_list]
        else:
            raise TypeError("measurement_list must be a list of Measurement objects.")
    for m in measurement_list:
        if not isinstance(m, Measurement):
            raise TypeError("measurement_list must be a list of Measurement objects.")

    db = Database().load_pkl(database,verbose=verbose)
    measurement_experiment_name_list = [m.experiment_name for m in measurement_list]

    if not all(name in db.experiment_name_list for name in measurement_experiment_name_list):
        raise ValueError(f"The database does not contain fingerprints for the given measurements.")
        
    # Print database information if requested
    if verbose:
        print("Database Information:")
        print("    models in the database: ")
        for name in db.model_name_list:
            print("        " + name)
        print("    number of fingerprints = " + str(db.fingerprints_list[0].shape[0]))
        if "uniaxial tension/compression" in measurement_experiment_name_list:
            i = db.experiment_name_list.index("uniaxial tension/compression")
            print("    uniaxial tension: stretch ranges from " + str(np.min(db.experiment_control_list[i])) + " to " + str(np.max(db.experiment_control_list[i])) + " in the database")
        if "simple shear" in measurement_experiment_name_list:
            i = db.experiment_name_list.index("simple shear")
            print("    simple shear: shear stretch ranges from " + str(np.min(db.experiment_control_list[i])) + " to " + str(np.max(db.experiment_control_list[i])) + " in the database")
        if "pure shear" in measurement_experiment_name_list:
            i = db.experiment_name_list.index("pure shear")
            print("    pure shear: stretch ranges from " + str(np.min(db.experiment_control_list[i])) + " to " + str(np.max(db.experiment_control_list[i])) + " in the database")
        if "equibiaxial tension/compression" in measurement_experiment_name_list:
            i = db.experiment_name_list.index("equibiaxial tension/compression")
            print("    equibiaxial tension: stretch ranges from " + str(np.min(db.experiment_control_list[i])) + " to " + str(np.max(db.experiment_control_list[i])) + " in the database")
    
    # Assemble fingerprint of the measurement
    f = np.array([])
    for i, experiment_name in enumerate(db.experiment_name_list):
        if experiment_name in measurement_experiment_name_list:
            j = measurement_experiment_name_list.index(experiment_name)
            f_interp = np.interp(db.experiment_control_list[i], measurement_list[j].control, measurement_list[j].measurement, left=0.0, right=0.0)
            f = np.append(f,f_interp)
        else:
            f = np.append(f,np.zeros(db.fingerprints_list[i].shape[1]))

    # Material Fingerprinting
    id, model_disc, parameters_disc, correlations = db.discover(f)

    # Compute R² values
    r2_results = compute_r2(measurement_list, model_disc, parameters_disc)

    # Print results if requested
    if verbose:
        mat = Material(name=model_disc)
        print("\nMaterial Fingerprinting Results:")
        print(f"    discovered model: {model_disc}")
        print("    identified parameters: " + str(parameters_disc))
        print(f"    formula: {mat.get_formula(parameters_disc)}")
        print("    R² values per experiment:")
        for exp_name, r2 in r2_results["R2_per_experiment"].items():
            print(f"        {exp_name}: {r2:.4f}")
        print(f"    R² average over all experiments: {r2_results['R2_average']:.4f}")

    # Print best models if requested
    if verbose and verbose_best_models:
        sorted_indices = np.argsort(correlations)[::-1]
        unique_models = []
        unique_parameters = []
        unique_correlations = []
        for idx in sorted_indices:
            model_name = db.model_name_list[db.model_indices[idx]]
            if model_name not in unique_models:
                unique_models.append(model_name)
                unique_parameters.append(parameters_disc)
                unique_correlations.append(correlations[idx])

        print("\n    best models in the database:")
        for i, (model_name, corr) in enumerate(zip(unique_models, unique_correlations)):
            print(f"        {i+1}. model: {model_name}, cosine similarity: {corr:.4f}")


    # Plot if requested
    if plot:
        discover_plot(measurement_list, model_disc, parameters_disc, r2_results)

    return model_disc, parameters_disc, r2_results

def discover_plot(measurement_list,model_disc,parameters_disc,r2_results=None):
    mat = Material(name=model_disc)
    if r2_results is None: r2_results = compute_r2(measurement_list, model_disc, parameters_disc)
    n_exp = len(measurement_list)
    fig, axes = plt.subplots(1, n_exp, figsize=(5*n_exp, 5), squeeze=False)
    fig.suptitle("Discovered model: " + model_disc + "\n$W=$" + mat.get_formula(parameters_disc))
    for i, m in enumerate(measurement_list):
        r = np.abs(np.max(m.control) - np.min(m.control)) / 20
        s = 15
        exp = Experiment(name=m.experiment_name, control_min=np.min(m.control)-r, control_max=np.max(m.control)+r)
        prediction = mat.conduct_experiment(exp, parameters=parameters_disc).squeeze()
        ax = axes[0, i]
        ax.scatter(m.control, m.measurement, color=tab20blue, s=s, label="Data")
        ax.plot(exp.control, prediction, color=tab20red, linewidth=2, label="Discovered")
        ax.set_title(m.experiment_name + "\n$R^2$=" + str(round(r2_results["R2_per_experiment"][m.experiment_name], 4)))
        ax.set_xlabel(exp.control_str[0])
        ax.set_ylabel(exp.measurement_str[0])
        ax.legend()
        ax.grid(True)
        ax.minorticks_on()
        ax.grid(True, which="minor", linestyle="--", color="lightgray", linewidth=0.5)
    fig.tight_layout()
    plt.show()
    return

def compute_r2(measurement_list, model_disc, parameters_disc):
    """
    Computes R² values for each experiment and the average R² for a discovered model.
    """
    mat = Material(name=model_disc)
    r2_per_experiment = {}

    for m in measurement_list:
        # Define experiment with the same control as the measurement
        exp = Experiment(name=m.experiment_name)
        exp.set_control(m.control)

        # Compute predicted measurements
        prediction = mat.conduct_experiment(exp, parameters=parameters_disc).squeeze()
        
        # Compute R² manually
        ss_res = np.sum((m.measurement - prediction) ** 2)
        ss_tot = np.sum((m.measurement - np.mean(m.measurement)) ** 2)
        r2 = 1 - ss_res / ss_tot
        r2_per_experiment[m.experiment_name] = r2

    r2_average = np.mean(list(r2_per_experiment.values()))
    return {"R2_per_experiment": r2_per_experiment, "R2_average": r2_average}
