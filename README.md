# Homogenization for Damask

This project is an unaffiliated extension to [DAMASK](https://github.com/damask-multiphysics/damask) and aims to homogenize DAMASK results and extract useful information for engineers. In particular, the [DAMASK_grid](https://damask-multiphysics.org/support/FAQ/grid_solver.html) solver and the [Python package](https://pypi.org/project/damask/) are used to find the homogenized stress and strain state used for identifying the components of the elastic matrix, yield surface and general loading response. 

To achieve these results, this extension provides:
- Generation of DAMASK simulation files.
- Running and monitoring of DAMASK_grid simulations, including condition based termination of simulations.
- Post-processing of DAMASK simulation results extending to:
    - Homogenization of simulation domain for stress and strain
    - Fitting the results to the components of the elastic matrix
    - Finding of yield stresses for arbitrary loading directions
    - Fitting and plotting of yield surfaces
    - Plotting of stress-strain curves

## Installation

## Usage

## Context
This project has been developed by Joppe Kleinhout in the context of pursuing a Msc degree in Mechanical Engineering at the University of Twente. Specifically as an internship at the Research chair of Nonlinear Solid Mechanics.

## Acknowledgements

