# System packages
from typing import Union

# Local packages
from ...common_classes.problem_definition import ProblemDefinition

def compare_yield_point_settings(
        problem_definition: ProblemDefinition, 
        existing_results: dict[str, dict[str, Union[str, bool, float]]]):
    
    differences_detected = False
    reasons: list[str] = []

    existing_settings = existing_results['yield_point']
    if not existing_settings['N_increments'] == problem_definition.solver.N_increments:
        differences_detected = True
        reasons.append(" number of increments (N_increments) changed")

    if not existing_settings['yield_condition'] == problem_definition.yielding_condition.yield_condition:
        differences_detected = True
        reasons.append(" condition for yield detection changed")
    else:
        match problem_definition.yielding_condition.yield_condition:
            case 'modulus_degradation':
                yield_condition_value = problem_definition.yielding_condition.modulus_degradation_percentage
            case 'stress_strain_curve':
                yield_condition_value = problem_definition.yielding_condition.plastic_strain_yield
            case _:
                raise Exception(f"Comparison of the yield value for the {problem_definition.yielding_condition.yield_condition} yield condition is not yet implemented!")

        if not existing_settings['yield_condition_value'] == yield_condition_value:
            differences_detected = True
            reasons.append(" value at which plasticity is defined is changed")
    
    if not existing_settings['estimated_tensile_yield'] == problem_definition.yielding_condition.estimated_tensile_yield:
        differences_detected = True
        reasons.append(" estimated estimated tensile yield strength changed")

    if not existing_settings['estimated_shear_yield'] == problem_definition.yielding_condition.estimated_shear_yield:
        differences_detected = True
        reasons.append(" estimated estimated shear yield strength changed")

    return (differences_detected, reasons)