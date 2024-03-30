# test_example.py

def add(x, y):
    return x + y

def test_addition():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def subtract(x, y):
    return x - y

def test_subtraction():
    assert subtract(5, 2) == 3
    assert subtract(10, 7) == 3
    assert subtract(0, 0) == 0

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
