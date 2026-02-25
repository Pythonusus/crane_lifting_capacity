"""This module contains project wide test fixtures."""

import json
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.api import app


@pytest.fixture
def client(monkeypatch) -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI app."""

    with TestClient(app) as c:
        yield c


@pytest.fixture
def cranes_test_data():
    """
    Load crane test data from individual JSON files in cranes_dump directory.
    Test data is assumed to be in cranes_dump/ directory
    in same dir with conftest.py.
    Each crane is stored in a separate JSON file
    with format: manufacturer_model.json
    """
    cranes_test_data_dir = Path(__file__).parent / "cranes_test_data"
    crane_data = {}

    if not cranes_test_data_dir.exists():
        raise FileNotFoundError(
            f"Cranes test data directory not found: {cranes_test_data_dir}. "
            "Please run 'make dump-cranes' first to generate test data."
        )

    # Load all JSON files from the cranes_dump directory
    for json_file in cranes_test_data_dir.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                json_data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {json_file}: {e}")

            if "name" not in json_data:
                raise ValueError(f"Missing 'name' field in {json_file}")
            crane_data[json_data["name"]] = json_data

    if not crane_data:
        raise FileNotFoundError(
            f"No crane JSON files found in {cranes_test_data_dir}. "
            "Please run 'make dump-test-cranes' first to generate test data."
        )

    return crane_data


@pytest.fixture
def calc_accuracy():
    """
    Return the required accuracy for the calculations.
    """
    return 0.01
