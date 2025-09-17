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
    if format == "uniaxial tension/compression":
        I1 = np.power(control,2.0) + 2.0/control
    elif format == "simple shear":
        I1 = np.power(control,2.0) + 3.0
    elif format == "pure shear":
        I1 = np.power(control,2.0) + np.power(control,-2.0) + 1.0
    elif format == "equibiaxial tension/compression":
        I1 = 2.0*np.power(control,2.0) + np.power(control,-4.0)
    else:
        raise ValueError("Not implemented.")
    return I1

def compute_I1_derivative(control,format="F"):
    # note that this is not dI1/d(control)
    # instead, it is dI1/d(F11) - dI1/d(F33) F33/F11 to account for incompressibility
    if format == "uniaxial tension/compression":
        dI1 = 2.0*control - 2.0*np.power(control,-2.0)
    elif format == "simple shear":
        dI1 = 2.0*control
    elif format == "pure shear":
        dI1 = 2.0*control - 2.0*np.power(control,-3.0)
    elif format == "equibiaxial tension/compression":
        dI1 = 2.0*control - 2.0*np.power(control,-5.0)
    else:
        raise ValueError("Not implemented.")
    return dI1

def compute_I1_derivative_triaxial_incompressible(F11,F22,F33):
    # dI1/d(F11) - dI1/d(F33) F33/F11
    return 2*(F11 - np.power(F33,2.0)/F11)

def compute_I2(control,format="F"):
    if format == "uniaxial tension/compression":
        I2 = 2*control + 1/np.power(control,2.0)
    elif format == "simple shear":
        I2 = np.power(control, 2.0) + 3.0
    elif format == "pure shear":
        I2 = np.power(control,2.0) + np.power(control,-2.0) + 1.0
    elif format == "equibiaxial tension/compression":
        I2 = np.power(control,4.0) + 2.0*np.power(control,-2.0)
    else:
        raise ValueError("Not implemented.")
    return I2

def compute_I2_derivative(control,format="F"):
    # note that this is not dI2/d(control)
    # instead, it is dI2/d(F11) - dI2/d(F33) F33/F11 to account for incompressibility
    if format == "uniaxial tension/compression":
        dI2 = 2.0 - 2.0*np.power(control,-3.0)
    elif format == "simple shear":
        dI2 = 2.0*control
    elif format == "pure shear":
        dI2 = 2.0*control - 2.0*np.power(control,-3.0)
    elif format == "equibiaxial tension/compression":
        dI2 = 2.0*np.power(control,3.0) - 2.0*np.power(control,-3.0)
    else:
        raise ValueError("Not implemented.")
    return dI2
    
def compute_I2_derivative_triaxial_incompressible(F11,F22,F33):
    # dI2/d(F11) - dI2/d(F33) F33/F11
    return 2*(F11*np.power(F22,2.0) - np.power(F11,-3))

    
    






















