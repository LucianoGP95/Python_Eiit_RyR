import os, sys
import pytest
sys.path.append("../src/")
from core_logic import get_name

@pytest.fixture
def temp_test_dir(tmp_path):
    # You can perform additional setup here if needed
    return tmp_path

def temp_test_dir(tmpdir):
    # You can perform additional setup here if needed
    yield str(tmpdir)

def test_get_name(temp_test_dir):
    # Create a dummy CSV file in the temporary directory
    dummy_file = os.path.join(temp_test_dir, "dummy_file.csv")
    with open(dummy_file, "w") as f:
        f.write("dummy content")

    # Call the function with the temporary directory
    tooling_name = get_name(temp_test_dir)

    # Assert that the result is a string
    assert isinstance(tooling_name, str)