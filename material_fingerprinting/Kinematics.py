"""
                           
 _|      _|      _|_|_|_|  
 _|_|  _|_|      _|        
 _|  _|  _|      _|_|_|    
 _|      _|      _|        
 _|      _|  _|  _|    _|  
                           
 Material        Fingerprinting

"""

import numpy as np

def compute_I1(control,format="F"):
    if format == "uniaxial tension - finite strain":
        I1 = np.pow(control,2.0) + 2.0/control
    elif format == "simple shear - finite strain":
        I1 = np.pow(control,2.0) + 3.0
    else:
        raise ValueError("Not implemented.")
    return I1

def compute_I1_derivative(control,format="F"):
    if format == "uniaxial tension - finite strain":
        dI1 = 2.0*control - 2.0*np.pow(control,-2.0)
    elif format == "simple shear - finite strain":
        dI1 = 2.0*control
    else:
        raise ValueError("Not implemented.")
    return dI1

def compute_I2(control,format="F"):
    if format == "uniaxial tension - finite strain":
        I2 = 2*control + 1/np.pow(control,2.0)
    elif format == "simple shear - finite strain":
        I2 = np.pow(control, 2.0) + 3.0
    else:
        raise ValueError("Not implemented.")
    return I2

def compute_I2_derivative(control,format="F"):
    if format == "uniaxial tension - finite strain":
        dI2 = 2.0 - 2.0/np.pow(control,3.0)
    elif format == "simple shear - finite strain":
        dI2 = 2.0*control
    else:
        raise ValueError("Not implemented.")
    return dI2
    

    
    






















