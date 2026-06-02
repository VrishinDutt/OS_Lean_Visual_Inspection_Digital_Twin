import json
from pathlib import Path
from rich import print


REQUIRED_EVENT_KEYS = {"time", "product_id", "event", "mode", "status"}


def extract_events(data):
    if isinstance(data, dict) and "events" in data:
        return data["events"]

    if isinstance(data, list):
        return data

    return []


def validate_event(event, file_path, index):
    missing = REQUIRED_EVENT_KEYS - set(event.keys())

    if missing:
        return f"{file_path} event #{index} missing keys: {sorted(missing)}"

    if not isinstance(event["time"], (int, float)):
        return f"{file_path} event #{index} has invalid time"

    if not isinstance(event["product_id"], str):
        return f"{file_path} event #{index} has invalid product_id"

    if not isinstance(event["event"], str):
        return f"{file_path} event #{index} has invalid event"

    if not isinstance(event["mode"], str):
        return f"{file_path} event #{index} has invalid mode"

    if not isinstance(event["status"], str):
        return f"{file_path} event #{index} has invalid status"

    return None


def validate_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    events = extract_events(data)

    if not events:
        return [f"{file_path} has no events"]

    errors = []

    for index, event in enumerate(events):
        error = validate_event(event, file_path, index)
        if error:
            errors.append(error)

    return errors


def main():
    event_dir = Path("simulation_events")
    files = sorted(event_dir.glob("*.json"))

    if not files:
        print("[red]No JSON files found in simulation_events/[/red]")
        return

    all_errors = []

    for file_path in files:
        errors = validate_file(file_path)

        if errors:
            all_errors.extend(errors)
            print(f"[red]FAILED[/red] {file_path}")
        else:
            print(f"[green]VALID[/green] {file_path}")

    if all_errors:
        print("\n[bold red]Validation errors:[/bold red]")
        for error in all_errors:
            print(f"- {error}")
    else:
        print("\n[bold green]All event files are Unreal-ready.[/bold green]")


if __name__ == "__main__":
    main()
