import numpy as np
import material_fingerprinting as mf

# experimental data
mat = mf.Material(name="Ogden - incompressible")
parameters = np.array([50.0, 4.0])
exp1 = mf.Experiment(mode="uniaxial tension - finite strain",control_min=0.7,control_max=1.3,n_steps=20)
exp2 = mf.Experiment(mode="simple shear - finite strain",control_min=0.0001,control_max=0.5,n_steps=20)

# test 1
measurement = {
    "experiment": "UTCSS", # uniaxial tension/compression and simple shear
    "F11": exp1.control,
    "P11": mat.conduct_experiment(exp1,parameters = parameters),
    "F12": np.array([0.0]),
    "P12": np.array([0.0]),
}
model_disc, parameters_disc = mf.discover(measurement)
print(model_disc)
print(parameters_disc)

# test 2
measurement = {
    "experiment": "UTCSS", # uniaxial tension/compression and simple shear
    "F11": np.array([1.0]),
    "P11": np.array([0.0]),
    "F12": exp2.control,
    "P12": mat.conduct_experiment(exp2,parameters = parameters),
}
model_disc, parameters_disc = mf.discover(measurement)
print(model_disc)
print(parameters_disc)

# test 3
measurement = {
    "experiment": "UTCSS", # uniaxial tension/compression and simple shear
    "F11": exp1.control.reshape(-1)[:5],
    "P11": mat.conduct_experiment(exp1,parameters = parameters).reshape(-1)[:5],
}
mf.discover(measurement)

# test 4
measurement = {
    "experiment": "UTCSS", # uniaxial tension/compression and simple shear
    "F12": exp2.control.reshape(-1)[5:],
    "P12": mat.conduct_experiment(exp2,parameters = parameters).reshape(-1)[5:],
}
mf.discover(measurement)
