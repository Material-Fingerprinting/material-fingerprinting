import numpy as np
import material_fingerprinting as mf

"""
experimental data - this can be replaced by the user
"""
# mat = mf.Material(name="Blatz-Ko - incompressible")
# parameters = np.array([50.0])

# mat = mf.Material(name="Gent - incompressible")
# parameters = np.array([50.0, 0.3])

mat = mf.Material(name="Ogden - incompressible")
parameters = np.array([50.0, 4.0])

exp1 = mf.Experiment(mode="uniaxial tension - finite strain",control_min=0.7,control_max=1.3,n_steps=20)
exp2 = mf.Experiment(mode="simple shear - finite strain",control_min=0.0001,control_max=0.5,n_steps=20)

# print(', '.join(map(str, exp1.control)))

"""
prepare data for discovery
"""
measurement = {
    "experiment": "UTCSS", # uniaxial tension/compression and simple shear
    "F11": exp1.control,
    "P11": mat.conduct_experiment(exp1,parameters = parameters).squeeze(),
    "F12": exp2.control,
    "P12": mat.conduct_experiment(exp2,parameters = parameters).squeeze(),
}

"""
discover model with Material Fingerprinting
"""
mf.discover(measurement)
