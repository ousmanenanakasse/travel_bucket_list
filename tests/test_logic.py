import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic import (
    is_valid_budget,
    is_valid_priority,
    is_valid_status,
    calculate_total_budget,
    count_visited_destinations
)


def test_valid_budget():
    assert is_valid_budget(100) == True
    assert is_valid_budget(0) == True
    assert is_valid_budget(-50) == False


def test_valid_priority():
    assert is_valid_priority("Low") == True
    assert is_valid_priority("Medium") == True
    assert is_valid_priority("High") == True
    assert is_valid_priority("Urgent") == False


def test_valid_status():
    assert is_valid_status("Planned") == True
    assert is_valid_status("Visited") == True
    assert is_valid_status("Cancelled") == False


def test_total_budget():
    destinations = [
        {"budget": 500},
        {"budget": 300},
        {"budget": 200}
    ]

    assert calculate_total_budget(destinations) == 1000


def test_count_visited_destinations():
    destinations = [
        {"status": "Visited"},
        {"status": "Planned"},
        {"status": "Visited"}
    ]

    assert count_visited_destinations(destinations) == 2