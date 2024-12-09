# System packages
import damask  # type: ignore
import numpy as np
from numpy.typing import NDArray

# Local packages
from ...common_functions import damask_helper
from ...common_classes.problem_definition import StressTensors, StrainTensors

def interpolate_values_float(
        fraction: float, 
        values_1: float, 
        values_2: float) -> float: 
    input_shape_match = np.shape(values_1) == np.shape(values_2)
    if not input_shape_match:
        raise ValueError(f"Shape of field 1 ({np.shape(values_1)}) does not match shape field 2 ({np.shape(values_2)})! (interpolation)")
    
    interpolated: float = (values_2 - values_1) * fraction + values_1
    return interpolated

def interpolate_values_tensor(
        fraction: float, 
        values_1: NDArray[np.float64], 
        values_2: NDArray[np.float64]) -> NDArray[np.float64]: 
    input_shape_match = np.shape(values_1) == np.shape(values_2)
    if not input_shape_match:
        raise ValueError(f"Shape of field 1 ({np.shape(values_1)}) does not match shape field 2 ({np.shape(values_2)})! (interpolation)")
    
    interpolated: NDArray[np.float64] = (values_2 - values_1) * fraction + values_1
    return interpolated

class InterpolatedResults:
    interpolation_fraction: float
    iteration_1: int
    iteration_2: int
    stress: NDArray[np.float64]
    strain: NDArray[np.float64]
    stress_linear: NDArray[np.float64]
    strain_linear: NDArray[np.float64]
    strain_norm: float
    strain_norm_first_iteration: float
    deformation_energy: float
    damage_value: float
    deformation_energy_linear: float

    def __init__(self,
            interpolation_fraction: float, damask_results: damask.Result,
            iteration_1: int, iteration_2: int,
            stress_tensor_type: StressTensors, strain_tensor_type: StrainTensors) -> None:

        self.interpolation_fraction = interpolation_fraction
        self.iteration_1 = iteration_1
        self.iteration_2 = iteration_2

        damask_results = damask_results.view(increments=[0, 1])


        (damask_results, stress_averaged_per_increment) = damask_helper.get_averaged_stress_per_increment(damask_results, stress_tensor_type)
        (damask_results, strain_averaged_per_increment) = damask_helper.get_averaged_strain_per_increment(damask_results, strain_tensor_type)

        self.stress_linear = stress_averaged_per_increment[1]
        self.strain_linear = strain_averaged_per_increment[1]

        damask_results = damask_results.view(increments=[iteration_1, iteration_2])

        (damask_results, stress_averaged_per_increment) = damask_helper.get_averaged_stress_per_increment(damask_results,stress_tensor_type)
        (damask_results, strain_averaged_per_increment) = damask_helper.get_averaged_strain_per_increment(damask_results,strain_tensor_type)

        stress_1: np.float64 = stress_averaged_per_increment[0]
        strain_1: np.float64 = strain_averaged_per_increment[0]

        stress_2: np.float64 = stress_averaged_per_increment[1]
        strain_2: np.float64 = strain_averaged_per_increment[1]

        stress_interpolated: NDArray[np.float64] = interpolate_values_tensor(interpolation_fraction, stress_1, stress_2)  # type: ignore
        strain_interpolated: NDArray[np.float64] = interpolate_values_tensor(interpolation_fraction, strain_1, strain_2) # type: ignore

        self.stress: NDArray[np.float64] = stress_interpolated
        self.strain: NDArray[np.float64] = strain_interpolated

        self.strain_norm = float(np.linalg.norm(self.strain))
        self.strain_norm_first_iteration = float(np.linalg.norm(self.strain_linear))

        self.strain_norm = float(np.linalg.norm(self.strain))
        self.strain_norm_first_iteration = float(np.linalg.norm(self.strain_linear))

        self.deformation_energy_undamaged_secant = damask_helper.calculate_linear_deformatation_energy_undamaged_secant_stiffness(self.stress_linear, self.strain_linear, self.strain)
    
        self.damage_value = damask_helper.calculate_damage_value(self.stress_linear, self.strain_linear, self.stress, self.strain)
        self.deformation_energy = damask_helper.calculate_linear_deformatation_energy(self.stress, self.strain)




