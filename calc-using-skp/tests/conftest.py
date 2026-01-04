"""Pytest configuration and shared fixtures."""

import pytest
from decimal import Decimal
from sys import path as sys_path
from pathlib import Path

# Add src directory to path for imports
project_root = Path(__file__).parent.parent
sys_path.insert(0, str(project_root / "src"))


@pytest.fixture
def decimal_zero():
    """Fixture for zero as Decimal."""
    return Decimal('0')


@pytest.fixture
def decimal_one():
    """Fixture for one as Decimal."""
    return Decimal('1')


@pytest.fixture
def decimal_pi():
    """Fixture for pi approximation as Decimal."""
    return Decimal('3.14159265')


@pytest.fixture
def sample_decimals():
    """Fixture for common decimal test values."""
    return {
        'half': Decimal('0.5'),
        'tenth': Decimal('0.1'),
        'third': Decimal('0.333333333'),
        'pi': Decimal('3.14159265'),
        'large': Decimal('999999999999'),
    }
