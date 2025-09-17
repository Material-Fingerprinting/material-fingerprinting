"""
                           
 _|      _|      _|_|_|_|  
 _|_|  _|_|      _|        
 _|  _|  _|      _|_|_|    
 _|      _|      _|        
 _|      _|  _|  _|    _|  
                           
 Material        Fingerprinting

"""

import numpy as np
import material_fingerprinting as mf

"""
experiments
"""
exp1 = mf.Experiment("uniaxial tension/compression",control_min=0.1,control_max=10.0,n_steps=1000)
exp2 = mf.Experiment("simple shear",control_min=0.0001,control_max=10.0,n_steps=1000)
exp3 = mf.Experiment("pure shear",control_min=0.1,control_max=10.0,n_steps=1000)
exp4 = mf.Experiment("equibiaxial tension/compression",control_min=0.1,control_max=10.0,n_steps=1000)
experiment_list = [exp1,exp2,exp3,exp4]

"""
models
"""
model_name_list = [
    "Blatz-Ko - incompressible",
    "Demiray - incompressible",
    "Gent - incompressible",
    "Holzapfel - incompressible",
    "Mooney-Rivlin - incompressible",
    "Neo-Hooke - incompressible",
    "Ogden - incompressible",
]

"""
database
"""
db = mf.Database()
for m in model_name_list:
    fp = mf.Fingerprints(
        experiment_list,
        mf.Material(name=m),
        parameter_min=0.1,
        parameter_max=50,
        n_fingerprints=500,
        )
    db.append(fp)
    fp.delete()

# db.save_npz("HEI") # hyperelastic incompressible
db.save_pkl("HEI") # hyperelastic incompressible

db_loaded = mf.Database().load_pkl("HEI")
