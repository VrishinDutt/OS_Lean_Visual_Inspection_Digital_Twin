from rich import print

from backend.unsafe_race_model import run_unsafe_simulation
from backend.synchronized_pipeline import run_safe_simulation
from backend.edf_scheduler import run_edf_scheduler
from backend.fcfs_scheduler import run_fcfs_scheduler
from backend.round_robin_scheduler import run_round_robin_scheduler
from backend.priority_scheduler import run_priority_scheduler
from backend.rms_scheduler import run_rms_scheduler
from backend.metrics import summarize_schedule, save_gantt_chart, save_deadline_comparison
from backend.event_exporter import export_json, schedule_to_unreal_events


def export_schedule_result(mode, schedule, metrics):
    export_json(
        {
            "mode": mode,
            "schedule": schedule,
            "events": schedule_to_unreal_events(schedule, mode),
            "metrics": metrics
        },
        f"simulation_events/{mode}_schedule.json"
    )


def main():
    print("[bold cyan]Running unsafe race-condition model...[/bold cyan]")
    unsafe_result = run_unsafe_simulation()
    export_json(unsafe_result, "simulation_events/unsafe_mode_events.json")

    print("[bold cyan]Running safe synchronized model...[/bold cyan]")
    safe_result = run_safe_simulation()
    export_json(safe_result, "simulation_events/safe_mode_events.json")

    print("[bold cyan]Running EDF scheduler...[/bold cyan]")
    edf_schedule = run_edf_scheduler(product_count=8)
    edf_metrics = summarize_schedule(edf_schedule)
    export_schedule_result("edf", edf_schedule, edf_metrics)

    print("[bold cyan]Running FCFS scheduler...[/bold cyan]")
    fcfs_schedule = run_fcfs_scheduler(product_count=8)
    fcfs_metrics = summarize_schedule(fcfs_schedule)
    export_schedule_result("fcfs", fcfs_schedule, fcfs_metrics)

    print("[bold cyan]Running Round Robin scheduler...[/bold cyan]")
    rr_schedule = run_round_robin_scheduler(product_count=8, quantum=4)
    rr_metrics = summarize_schedule(rr_schedule)
    export_schedule_result("round_robin", rr_schedule, rr_metrics)

    print("[bold cyan]Running Priority scheduler...[/bold cyan]")
    priority_schedule = run_priority_scheduler(product_count=8)
    priority_metrics = summarize_schedule(priority_schedule)
    export_schedule_result("priority", priority_schedule, priority_metrics)

    print("[bold cyan]Running RMS scheduler...[/bold cyan]")
    rms_schedule = run_rms_scheduler(product_count=8)
    rms_metrics = summarize_schedule(rms_schedule)
    export_schedule_result("rms", rms_schedule, rms_metrics)

    save_gantt_chart(edf_schedule, "visual_outputs/edf_gantt_chart.png")
    save_gantt_chart(rms_schedule, "visual_outputs/rms_gantt_chart.png")
    save_deadline_comparison(
        edf_metrics,
        fcfs_metrics,
        "visual_outputs/deadline_miss_comparison.png"
    )

    print("\n[bold green]Simulation complete.[/bold green]")
    print("\n[bold]Unsafe Metrics:[/bold]", unsafe_result["metrics"])
    print("[bold]Safe Metrics:[/bold]", safe_result["metrics"])
    print("[bold]EDF Metrics:[/bold]", edf_metrics)
    print("[bold]FCFS Metrics:[/bold]", fcfs_metrics)
    print("[bold]Round Robin Metrics:[/bold]", rr_metrics)
    print("[bold]Priority Metrics:[/bold]", priority_metrics)
    print("[bold]RMS Metrics:[/bold]", rms_metrics)

    print("\n[bold yellow]Generated files:[/bold yellow]")
    print("simulation_events/unsafe_mode_events.json")
    print("simulation_events/safe_mode_events.json")
    print("simulation_events/edf_schedule.json")
    print("simulation_events/fcfs_schedule.json")
    print("simulation_events/round_robin_schedule.json")
    print("simulation_events/priority_schedule.json")
    print("simulation_events/rms_schedule.json")
    print("visual_outputs/edf_gantt_chart.png")
    print("visual_outputs/rms_gantt_chart.png")
    print("visual_outputs/deadline_miss_comparison.png")


if __name__ == "__main__":
    main()
