NUM_PRODUCTS = 30

CONVEYOR_SPEED = 1.0

TASKS = {
    "sensor": {
        "burst": 2,
        "deadline": 10
    },
    "camera": {
        "burst": 4,
        "deadline": 25
    },
    "ai_inspection": {
        "burst": 12,
        "deadline": 70
    },
    "rule_inspection": {
        "burst": 5,
        "deadline": 45
    },
    "decision_fusion": {
        "burst": 3,
        "deadline": 85
    },
    "actuator": {
        "burst": 4,
        "deadline": 100
    },
    "logger": {
        "burst": 6,
        "deadline": 160
    }
}

DEFECT_PATTERN = {
    5, 11, 17, 23, 29
}
