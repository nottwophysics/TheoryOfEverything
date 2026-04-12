"""Shared fixtures for Theory of Everything test suite."""

import numpy as np
import pytest

from brahman.consciousness import Brahman


@pytest.fixture(autouse=True)
def reset_brahman():
    """Reset the Brahman singleton before each test."""
    Brahman.reset()
    yield
    Brahman.reset()


@pytest.fixture
def brahman():
    """A fresh Brahman instance."""
    return Brahman(resolution=64)


@pytest.fixture
def rng():
    """Seeded random state for reproducible tests."""
    return np.random.RandomState(42)
