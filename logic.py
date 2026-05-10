def is_valid_budget(budget):
    return budget >= 0


def is_valid_priority(priority):
    return priority in ["Low", "Medium", "High"]


def is_valid_status(status):
    return status in ["Planned", "Visited"]


def calculate_total_budget(destinations):
    total = 0

    for destination in destinations:
        total += destination["budget"]

    return total


def count_visited_destinations(destinations):
    count = 0

    for destination in destinations:
        if destination["status"] == "Visited":
            count += 1

    return count
