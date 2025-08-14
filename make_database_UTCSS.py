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
experiment
"""
exp1 = mf.Experiment(mode="uniaxial tension - finite strain",control_min=0.5,control_max=1.9,n_steps=1000)
exp2 = mf.Experiment(mode="simple shear - finite strain",control_min=0.01,control_max=1.0,n_steps=1000)
exp_union = mf.ExperimentUnion([exp1,exp2])

"""
compute fingerprints
"""
model_names = [
    "Blatz-Ko - incompressible",
    "Demiray - incompressible",
    "Gent - incompressible",
    "Holzapfel - incompressible",
    "Mooney-Rivlin - incompressible",
    "Neo-Hooke - incompressible",
    "Ogden - incompressible",
]

db = mf.Database(experiment_name="UTCSS",experiment_controls=[exp1.control,exp2.control])
for m in model_names:
    fp = mf.Fingerprints(
        mf.Material(name=m),
        exp_union,
        parameter_min=0.01,
        parameter_max=100,
        n_fingerprints=1000,
        )
    db.append(fp)

db.save()


