import os
import pytest
import numpy as np
from pyconmech import StiffnessChecker

@pytest.fixture
def stiffness_tol():
    trans_tol = 0.0015
    rot_tol = 5 * np.pi / 180
    return trans_tol, rot_tol

@pytest.fixture
def known_failure():
    return ['klein_bottle_trail.json', 'rotated_dented_cube.json']

def create_stiffness_checker(extrusion_path, trans_tol=0.0015, rot_tol=5*np.pi/180, verbose=False):
    # TODO: the stiffness checker likely has a memory leak
    if not os.path.exists(extrusion_path):
        raise FileNotFoundError(extrusion_path)
    checker = StiffnessChecker(json_file_path=extrusion_path, verbose=verbose)
    checker.set_self_weight_load(True)
    checker.set_nodal_displacement_tol(trans_tol=trans_tol, rot_tol=rot_tol)
    return checker

def test_extrusion_stiffness(extrusion_dir, extrusion_problem, stiffness_tol, known_failure):
    p = os.path.join(extrusion_dir, extrusion_problem)

    checker = create_stiffness_checker(p, trans_tol=stiffness_tol[0], rot_tol=stiffness_tol[1], verbose=False)

    is_stiff = checker.solve()
    success, nodal_displacement, fixities_reaction, element_reaction = checker.get_solved_results()
    
    assert is_stiff == success 

    trans_tol, rot_tol = checker.get_nodal_deformation_tol()
    max_trans, max_rot, max_trans_vid, max_rot_vid = checker.get_max_nodal_deformation()
    compliance = checker.get_compliance()
    assert compliance > 0, 'Compliance must be bigger than zero! (no matter how small the value is), its likely have something wrong with the material / cross sectional properties. Does it have cross section area, Jx, Ix, Iy, Iz value? (compared to radius)'

    if not success:
        print('\n' + '='*6)
        print('Test stiffness on problem: {}'.format(p))
        # The inverse of stiffness is flexibility or compliance
        print('Stiff: {} | Compliance: {}'.format(is_stiff, compliance))
        print('Max translation deformation: {0:.5f} / {1:.5} = {2:.5}, at node #{3}'.format(
            max_trans, trans_tol, max_trans / trans_tol, max_trans_vid))
        print('Max rotation deformation: {0:.5f} / {1:.5} = {2:.5}, at node #{3}'.format(
            max_rot, rot_tol, max_rot / rot_tol, max_rot_vid))
    if extrusion_problem not in known_failure:
        assert success