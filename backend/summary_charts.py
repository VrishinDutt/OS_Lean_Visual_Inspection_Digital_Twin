import os
import json
import matplotlib.pyplot as plt


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_race_condition_comparison(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    unsafe = load_json("simulation_events/unsafe_mode_events.json")
    safe = load_json("simulation_events/safe_mode_events.json")

    modes = ["Unsafe Shared State", "Safe Synchronized Pipeline"]
    race_counts = [
        unsafe["metrics"]["race_conditions"],
        safe["metrics"]["race_conditions"]
    ]

    plt.figure(figsize=(9, 5))
    plt.bar(modes, race_counts)
    plt.ylabel("Race Condition Count")
    plt.title("Race Condition Comparison")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def save_quality_decision_summary(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    unsafe = load_json("simulation_events/unsafe_mode_events.json")
    safe = load_json("simulation_events/safe_mode_events.json")

    def count_decisions(data):
        products = data["products"]
        reject_count = sum(1 for product in products if product["final_decision"] == "reject")
        pass_count = sum(1 for product in products if product["final_decision"] == "pass")
        return pass_count, reject_count

    unsafe_pass, unsafe_reject = count_decisions(unsafe)
    safe_pass, safe_reject = count_decisions(safe)

    labels = ["Unsafe Pass", "Unsafe Reject", "Safe Pass", "Safe Reject"]
    values = [unsafe_pass, unsafe_reject, safe_pass, safe_reject]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.ylabel("Product Count")
    plt.title("Inspection Decision Summary")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def main():
    save_race_condition_comparison("visual_outputs/race_condition_comparison.png")
    save_quality_decision_summary("visual_outputs/quality_decision_summary.png")

    print("Saved visual_outputs/race_condition_comparison.png")
    print("Saved visual_outputs/quality_decision_summary.png")


if __name__ == "__main__":
    main()
