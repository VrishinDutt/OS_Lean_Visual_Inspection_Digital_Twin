import json
import os


def export_json(data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def schedule_to_unreal_events(schedule, mode):
    events = []

    for row in schedule:
        status = "deadline_missed" if row["deadline_missed"] else "scheduled"

        events.append({
            "time": row["start_time"],
            "product_id": row["product_id"],
            "event": f"{row['task']}_started",
            "mode": mode,
            "status": status
        })

        events.append({
            "time": row["completion_time"],
            "product_id": row["product_id"],
            "event": f"{row['task']}_completed",
            "mode": mode,
            "status": status
        })

    return events
