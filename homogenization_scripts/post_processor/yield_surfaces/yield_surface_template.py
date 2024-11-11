# System packages
from typing import Protocol
from pandas import DataFrame

# Local packages
# from .helper_functions import calculate_MSE_stress

class YieldSurfaces(Protocol):
    # To implement a new yield surface, a class should be created implementing
    # the following functions with the same name and input values.

    # Setting additionally needed coefficients can be done with the constructor:

    # Example:
    # def __init__(self, some_other_constant: float) -> None:
    #   self.some_other_constant = some_other_constant

    # Aditional functions can be implemented as well:
    # def square_some_other_constant(self) -> float:
    #   squared = self.some_other_constant**2
    # return squared

    # The MSE functions can be copied over as is. Note that the calculate_MSE_stress
    # has to be imported from the helper_functions.py script.

    mean_square_error_stress: float

    # To give some constant to the yield surface the constructor can be used:
    # This will be used as "yield_surface_name = YieldSurfaceName(some_constant)"
    # def __init__(self, some_constant: float) -> None:
    #     self.some_constant = some_constant
    #     return

    def set_coefficients_from_list(self, coefficients_list: list[float]) -> None:
        # This function will receive a list of coefficients, which have to be stored
        # with any sort of naming inside of the class instance. These coefficients are
        # used inside of evaluate().
        # The length of coefficients_list equals the output of number_optimization_coefficients()
        # Example:
        # self.a = coefficients_list[0]
        # self.power = coefficients_list[1]
        return
    
    def number_optimization_coefficients(self) -> int:
        # The number of coefficients that have to be fitted. Must match expected length 
        # in set_coefficients_from_list()
        return int()
    
    def display_name(self) -> str:
        # The name to use for outputs and plots
        return str()
    
    def unit_conversion(self) -> float:
        # The yield point data is in Pascal, this translates the stresses to another unit
        Pa_to_MPa = 1/1E6
        return Pa_to_MPa
    
    def unit_name(self) -> str:
        unit_name = "MPa"
        return unit_name
    
    def evaluate(self, stress_voight: list[float]) -> float:
        # This function takes a stress state (voight notation) and returns the value
        # of the yield surface function. Yield surface function must equal 0 for yielding. 
        # For example, in the case of Hill, notation must be:
        # evaluate() = -1/self.unit_conversion() + F*(...) + G*(...) + H*(...) + L*(...) + M*(...) + N*(...) 
        # NOTE: -1/self.unit_conversion() used for normalization of the coefficients: Needed for accurate data fitting
        return float()
    
    def penalty_sum(self) -> float:
        # Certain yield surfaces have conditions that have to be met by the coefficients.
        # Suppose that coefficient_1 should be larger then 1 and smaller then 2.
        # This function allows to set a penalty (barrier) function to adhere to these constraints which
        # is used during optimization of the coefficients (data fitting).
        # Take the following into account: 
        #   A penalty is any positive value.
        #   Penalty should be 0 when constraint is met.
        #   Barrier function should at least be quadratic of the constraint violation.
        #   Multiply penalty by large number if constraint violation numerically small (generally the case)
        # Example application:
        # penalty_smaller_then_1 = 1000*(min([1, coefficient_1] - 1))**2
        # penalty_larger_then_2 = 1000*(max([2, coefficient_1] - 2))**2
        # penalty = penalty_smaller_then_1 + penalty_larger_then_2
        # return penalty
        return float()
    
    def write_to_file(self, path:str, MSE: float | None = None) -> None:
        # Define how the fitted yield surface should be writen to a file.
        return
    
    def get_MSE(self, data_set: DataFrame) -> float:
        # Calculate the mean square error of over/under estimation of yield stresses
        mean_square_error = calculate_MSE_stress(self, data_set) # type: ignore
        return mean_square_error
    
    def set_MSE(self, mean_square_error_stress: float) -> None:
        # Store the mean square error of over/under estimation of yield stresses
        self.mean_square_error_stress = mean_square_error_stress
        return
    
    def get_and_set_MSE(self, data_set: DataFrame) -> float:
        mean_square_error_stress = self.get_MSE(data_set)
        self.set_MSE(mean_square_error_stress)
        return mean_square_error_stress
    

def calculate_MSE_stress(self, data_set) -> float: # type: ignore
    # Dummy function. See actual function in helper_functions.py.
    return float()