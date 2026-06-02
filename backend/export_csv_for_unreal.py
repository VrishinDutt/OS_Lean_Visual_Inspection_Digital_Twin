import json
import csv
from pathlib import Path


FILES = [
    "unsafe_mode_events.json",
    "safe_mode_events.json",
    "edf_schedule.json",
    "fcfs_schedule.json",
    "round_robin_schedule.json",
    "priority_schedule.json",
    "rms_schedule.json",
]


def extract_events(data):
    if isinstance(data, dict) and "events" in data:
        return data["events"]

    if isinstance(data, list):
        return data

    return []


def convert_file(json_path, csv_path):
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    events = extract_events(data)

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["time", "product_id", "event", "mode", "status"]
        )
        writer.writeheader()

        for event in events:
            writer.writerow({
                "time": event["time"],
                "product_id": event["product_id"],
                "event": event["event"],
                "mode": event["mode"],
                "status": event["status"]
            })


def main():
    source_dir = Path("simulation_events")
    output_dir = Path("unreal_project/event_tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    for filename in FILES:
        json_path = source_dir / filename
        csv_path = output_dir / filename.replace(".json", ".csv")

        if json_path.exists():
            convert_file(json_path, csv_path)
            print(f"Exported {csv_path}")
        else:
            print(f"Missing {json_path}")


if __name__ == "__main__":
    main()
