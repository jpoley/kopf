import glob
import os.path
import pathlib
import subprocess

import pytest

from kopf._core.intents.registries import SmartOperatorRegistry

root_dir = os.path.relpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
examples = sorted(glob.glob(os.path.join(root_dir, 'examples/*/')))
assert examples  # if empty, it is just the detection failed
examples = [path for path in examples if not glob.glob((os.path.join(path, 'test*.py')))]


@pytest.fixture
def registry_factory():
    # Authentication is needed for the real e2e tests.
    return SmartOperatorRegistry


@pytest.fixture(params=examples, ids=[os.path.basename(path.rstrip('/')) for path in examples])
def exampledir(request):
    return pathlib.Path(request.param)


@pytest.fixture()
def with_crd():
    # Our best guess on which Kubernetes version we are running on.
    subprocess.run(f"kubectl apply -f examples/crd.yaml",
                   shell=True, check=True, timeout=10, capture_output=True)


@pytest.fixture()
def with_peering():
    subprocess.run(f"kubectl apply -f peering.yaml",
                   shell=True, check=True, timeout=10, capture_output=True)


@pytest.fixture()
def no_crd():
    subprocess.run("kubectl delete customresourcedefinition kopfexamples.kopf.dev",
                   shell=True, check=True, timeout=10, capture_output=True)


@pytest.fixture()
def no_peering():
    subprocess.run("kubectl delete customresourcedefinition kopfpeerings.kopf.dev",
                   shell=True, check=True, timeout=10, capture_output=True)
