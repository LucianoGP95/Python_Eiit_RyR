import script
import pytest

def test_script():
    tol = 0.015
    val = [0.3467, 0.342, 0.3475, 0.3543]
    result = script.limits_generator(tol, val)
    assert isinstance(result, list)
