# System packages
import os
import damask # type: ignore
import numpy as np
import shutil
import yaml


# Local packages
from ...common_classes.damask_job import DamaskJob, DamaskJobTypes
from ...common_classes.problem_definition import ProblemDefinition

class PrepareFile:

    def make_sure_work_folders_are_empty(
            problem_definition: ProblemDefinition,  # type: ignore
            damask_job: DamaskJob) -> None:
        damask_files_folder_job = damask_job.runtime.damask_files
        damask_files_folder_exists = os.path.exists(damask_files_folder_job)
        if damask_files_folder_exists:
            if os.path.isdir(damask_files_folder_job):
                shutil.rmtree(damask_files_folder_job)
            else:
                os.remove(damask_files_folder_job)
        
        os.makedirs(damask_files_folder_job, exist_ok=True)
    
        
        damask_files_results_job = damask_job.runtime.results_folder
        results_folder_exists = os.path.exists(damask_files_results_job)
        if results_folder_exists:
            backup_folder = damask_job.runtime.backup_folder

            existing_result_files = os.listdir(damask_files_results_job)
            for f in existing_result_files: 
                os.makedirs(backup_folder, exist_ok=True)
                shutil.move(os.path.join(damask_files_results_job, f), os.path.join(backup_folder,f))

            shutil.rmtree(damask_files_results_job)
        os.makedirs(damask_files_results_job, exist_ok=True)

        return None

        
    def material_properties_and_orientation_file(problem_definition: ProblemDefinition, damask_job: DamaskJob) -> tuple[ProblemDefinition, DamaskJob]: # type: ignore
        ## Read Euler angles and material data from files, create damask material configuration object
        material_properties_file = problem_definition.general.path.material_properties
        # grain_orientation_file = problem_definition.general.path.grain_orientation
        
        # config_material                             = damask.ConfigMaterial()
        # config_material['homogenization']['dummy']  = {'N_constituents':1,'mechanical':{'type':'pass'}}
        # config_material['phase']['A']               = damask.ConfigMaterial.load(material_properties_file)

        # orientations                                = np.loadtxt(grain_orientation_file,delimiter=',')
        # O_A                                         = damask.Rotation.from_Euler_angles(orientations,degrees=True) # type: ignore

        # config_material: damask.ConfigMaterial                             = config_material.material_add(homogenization='dummy',phase='A',O=O_A)  # type: ignore

        # material_properties_file_fixed = os.path.join(damask_job.runtime.damask_files, "material.yaml")
        # config_material.save(material_properties_file_fixed) # type: ignore
        damask_job.runtime.set_material_properties_file(material_properties_file)

        return (problem_definition, damask_job)


    def grid_and_dimensions_file(
            problem_definition: ProblemDefinition,  # type: ignore
            damask_job: DamaskJob) -> tuple[ProblemDefinition, DamaskJob]: 
        # preparing variables

        grid_file = problem_definition.general.path.grid_file
        dimensions_file = problem_definition.general.path.dimensions_file

        _, grid_file_extension = os.path.splitext(grid_file)

        ## Read grain IDs from files created in MTEX, save grid as damask object
        if grid_file_extension == '.txt':
            grid_pth                    = grid_file
            dimensions_pth              = dimensions_file

            grid                        = np.loadtxt(grid_pth,delimiter=',').astype(int)
            grid                        = grid-1                     # required because of mismatch in MTEX and DAMASK counting convention
            grid                        = grid[..., np.newaxis]      #  M x N -> M x N x 1 dimension
            cells                       = np.array(np.shape(grid)) # type: ignore

            [xmin,xmax,ymin,ymax,dx,_] = np.loadtxt(dimensions_pth,delimiter=',')
            physical_dimensions         = 1e-3*np.array([xmax-xmin,ymax-ymin,dx]) 
            g                           = damask.GeomGrid(grid, physical_dimensions)
            
            grid_file_fixed = os.path.join(damask_job.runtime.damask_files, "GRID.vti" )

            g.save(grid_file_fixed)
        else:
            grid_file_fixed = grid_file
        
        damask_job.runtime.set_grid_file(grid_file_fixed)

        return problem_definition, damask_job


    def load_case_file(
            problem_definition: ProblemDefinition,  # type: ignore
            damask_job: DamaskJobTypes) -> tuple[ProblemDefinition, DamaskJobTypes]:

        solver = {'mechanical':problem_definition.solver.solver_type}
        
        loadsteps = [] # type: ignore
        for load_step_number in range(len(damask_job.stress_tensor)):
            loadstep    = { # type: ignore
                'boundary_conditions':{
                    'mechanical':{
                        'F':damask_job.deformation_gradient_tensor[load_step_number],
                        'P':damask_job.stress_tensor[load_step_number]
                    }
                },
                'discretization':{
                    't':problem_definition.solver.simulation_time,
                    'N':1
                },
                'f_out':1,
                'f_restart':1
            }
            loadsteps.append(loadstep) # type: ignore
            
        load_case = damask.LoadcaseGrid(solver=solver, loadstep=loadsteps) # type: ignore

        
        load_case_path = os.path.join(damask_job.runtime.damask_files, 'LOADCASE.yaml')

        load_case.save(load_case_path) # type: ignore
        damask_job.runtime.set_loadcase_file(load_case_path)

        # damask_job: DamaskJobTypes = damask_job # type: ignore

        return problem_definition, damask_job

    def numerics_file(
            problem_definition: ProblemDefinition,  # type: ignore
            damask_job: DamaskJobTypes) -> tuple[ProblemDefinition, DamaskJobTypes]:
        
        numerics_dict: dict[str, dict[str, int | dict[str, float | int]]] = dict()

        numerics_dict['grid'] = dict()
        numerics_dict['grid']['N_staggered_iter_max'] = problem_definition.solver.N_staggered_iter_max
        numerics_dict['grid']['N_cutback_max'] = problem_definition.solver.N_cutback_max

        numerics_dict['grid']['mechanical'] = dict()
        numerics_dict['grid']['mechanical']['N_iter_min'] = problem_definition.solver.N_iter_min
        numerics_dict['grid']['mechanical']['N_iter_max'] = problem_definition.solver.N_iter_max
        numerics_dict['grid']['mechanical']['eps_abs_div_P'] = problem_definition.solver.eps_abs_div_P
        numerics_dict['grid']['mechanical']['eps_rel_div_P'] = problem_definition.solver.eps_rel_div_P
        numerics_dict['grid']['mechanical']['eps_abs_P'] = problem_definition.solver.eps_abs_P
        numerics_dict['grid']['mechanical']['eps_rel_P'] = problem_definition.solver.eps_rel_P
        numerics_dict['grid']['mechanical']['eps_abs_curl_F'] = problem_definition.solver.eps_abs_curl_F
        numerics_dict['grid']['mechanical']['eps_rel_curl_F'] = problem_definition.solver.eps_rel_curl_F

        numerics_path = os.path.join(damask_job.runtime.damask_files, 'NUMERICS.yaml')

        with open(numerics_path, 'w') as file:
            yaml.dump(numerics_dict, file)

        damask_job.runtime.set_numerics_file(numerics_path)

        return problem_definition, damask_job