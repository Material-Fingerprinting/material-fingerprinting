"""
                           
 _|      _|      _|_|_|_|  
 _|_|  _|_|      _|        
 _|  _|  _|      _|_|_|    
 _|      _|      _|        
 _|      _|  _|  _|    _|  
                           
 Material        Fingerprinting

"""

from matplotlib import pyplot as plt
import numpy as np

class Measurement():
    """
    
    """

    def __init__(self,experiment_name,control,measurement):
        self.experiment_name = experiment_name

        match experiment_name:
            case "uniaxial tension/compression":
                control = control.reshape(-1)
                measurement = measurement.reshape(-1)
                if len(control) != len(measurement):
                    raise ValueError("The control variable F11 and the measurement P11 must have the same dimension.")
                if len(control) == 0 or (len(control) == 1 and np.isclose(control[0],1.0)):
                    raise ValueError("The control variable F11 does not contain enough data.")
                if 1.0 not in control:
                    control = np.append(control, 1.0)
                    measurement = np.append(measurement, 0.0)
                sort = np.argsort(control)
                control = control[sort]
                measurement = measurement[sort]
                
            case "simple shear":
                control = control.reshape(-1)
                measurement = measurement.reshape(-1)
                if len(control) != len(measurement):
                    raise ValueError("The control variable F12 and the measurement P12 must have the same dimension.")
                if len(control) == 0 or (len(control) == 1 and np.isclose(control[0],0.0)):
                    raise ValueError("The control variable F12 does not contain enough data.")
                if 0.0 not in control:
                    control = np.append(control, 0.0)
                    measurement = np.append(measurement, 0.0)
                sort = np.argsort(control)
                control = control[sort]
                measurement = measurement[sort]

            case "pure shear":
                control = control.reshape(-1)
                measurement = measurement.reshape(-1)
                if len(control) != len(measurement):
                    raise ValueError("The control variable F11 and the measurement P11 must have the same dimension.")
                if len(control) == 0 or (len(control) == 1 and np.isclose(control[0],1.0)):
                    raise ValueError("The control variable F11 does not contain enough data.")
                if 1.0 not in control:
                    control = np.append(control, 1.0)
                    measurement = np.append(measurement, 0.0)
                sort = np.argsort(control)
                control = control[sort]
                measurement = measurement[sort]

            case "equibiaxial tension/compression":
                control = control.reshape(-1)
                measurement = measurement.reshape(-1)
                if len(control) != len(measurement):
                    raise ValueError("The control variable F11 and the measurement P11 must have the same dimension.")
                if len(control) == 0 or (len(control) == 1 and np.isclose(control[0],1.0)):
                    raise ValueError("The control variable F11 does not contain enough data.")
                if 1.0 not in control:
                    control = np.append(control, 1.0)
                    measurement = np.append(measurement, 0.0)
                sort = np.argsort(control)
                control = control[sort]
                measurement = measurement[sort]
                
            case _:
                raise NotImplementedError(
                    "This experimental setup is not implemented."
                    "\nAvailable experimental setups: "
                    "\n    uniaxial tension/compression"
                    "\n    simple shear"
                    "\n    pure shear"
                    "\n    equibiaxial tension/compression"
                )

        self.control = control
        self.measurement = measurement

