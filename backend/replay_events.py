import json
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table


console = Console()


def load_events(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict) and "events" in data:
        return data["events"]

    if isinstance(data, list):
        return data

    return []


def replay(file_path, speed=0.03):
    events = sorted(load_events(file_path), key=lambda event: event["time"])

    console.print(f"\n[bold cyan]Replaying:[/bold cyan] {file_path}\n")

    for event in events:
        status = event.get("status", "normal")
        style = "white"

        if status == "race":
            style = "bold red"
        elif status == "deadline_missed":
            style = "bold yellow"
        elif event["event"] == "actuator_reject":
            style = "bold magenta"
        elif event["event"] == "actuator_pass":
            style = "green"
        elif status == "scheduled":
            style = "cyan"

        table = Table(show_header=True, header_style="bold")
        table.add_column("Time")
        table.add_column("Product")
        table.add_column("Event")
        table.add_column("Mode")
        table.add_column("Status")

        table.add_row(
            str(event["time"]),
            event["product_id"],
            event["event"],
            event["mode"],
            event["status"],
            style=style
        )

        console.print(table)
        time.sleep(speed)


def main():
    files = [
        "simulation_events/unsafe_mode_events.json",
        "simulation_events/safe_mode_events.json",
        "simulation_events/edf_schedule.json",
        "simulation_events/fcfs_schedule.json",
        "simulation_events/round_robin_schedule.json",
        "simulation_events/priority_schedule.json",
        "simulation_events/rms_schedule.json",
    ]

    console.print("[bold]Available replays:[/bold]")

    for index, file in enumerate(files, start=1):
        console.print(f"{index}. {file}")

    choice = input("\nChoose file number: ").strip()

    try:
        selected = files[int(choice) - 1]
    except Exception:
        console.print("[red]Invalid choice.[/red]")
        return

    if not Path(selected).exists():
        console.print(f"[red]File not found:[/red] {selected}")
        return

    replay(selected)


if __name__ == "__main__":
    main()
