"""Shared test fixtures and configuration for FastAPI tests."""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def sample_activities():
    """
    Provide a fresh copy of activities data for each test.
    This avoids test pollution from shared state.
    """
    return deepcopy(activities)


@pytest.fixture
def client():
    """
    Provide a TestClient for making HTTP requests to the FastAPI app.
    Uses FastAPI's dependency override to inject fresh activities for each test.
    """
    # Store original activities
    original_activities = deepcopy(activities)

    # Create a fresh copy of activities for this test
    test_activities = deepcopy(activities)

    # Override the app's activities dependency
    def override_activities():
        return test_activities

    # Apply the override
    app.dependency_overrides[lambda: activities] = override_activities

    # Create the test client
    test_client = TestClient(app)

    yield test_client

    # Cleanup: restore original activities and remove overrides
    app.dependency_overrides.clear()
    activities.clear()
    activities.update(original_activities)
