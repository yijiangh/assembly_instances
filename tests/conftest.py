import os
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--extrusion_problem",
        action="append",
        default=[],
        help="list of extrusion problem name (no directory path included) to pass to test functions",
    )

@pytest.fixture
def extrusion_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, '..', 'extrusion'))

def enumerate_problems(extrusion_dir):
    here = os.path.dirname(os.path.abspath(__file__))
    temp_extrusion_dir = os.path.abspath(os.path.join(here, '..', 'extrusion'))

    for filename in sorted(os.listdir(temp_extrusion_dir)):
        if filename.endswith('.json'):
            yield filename

def pytest_generate_tests(metafunc):
    if "extrusion_problem" in metafunc.fixturenames and len(metafunc.config.getoption("extrusion_problem")) > 0:
        print('Testing {}'.format(metafunc.config.getoption("extrusion_problem")))
        metafunc.parametrize("extrusion_problem", metafunc.config.getoption("extrusion_problem"))
    else:
        # test all
        print('Testing all extrusion problems.')
        problems = sorted(set(enumerate_problems(extrusion_dir)))
        metafunc.parametrize("extrusion_problem", problems)