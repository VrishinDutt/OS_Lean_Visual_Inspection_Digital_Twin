import os
import pandas as pd
import matplotlib.pyplot as plt


def summarize_schedule(schedule):
    df = pd.DataFrame(schedule)

    return {
        "total_jobs": len(df),
        "missed_deadlines": int(df["deadline_missed"].sum()),
        "average_waiting_time": round(float(df["waiting_time"].mean()), 2),
        "average_turnaround_time": round(float(df["turnaround_time"].mean()), 2)
    }


def save_gantt_chart(schedule, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.DataFrame(schedule)

    plt.figure(figsize=(12, 7))

    for index, row in df.iterrows():
        plt.barh(
            y=row["job_id"],
            width=row["burst_time"],
            left=row["start_time"]
        )

    plt.xlabel("Time Units")
    plt.ylabel("Jobs")
    plt.title("EDF Scheduling Gantt Chart")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def save_deadline_comparison(edf_metrics, fcfs_metrics, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    labels = ["EDF", "FCFS"]
    missed = [
        edf_metrics["missed_deadlines"],
        fcfs_metrics["missed_deadlines"]
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, missed)
    plt.ylabel("Missed Deadlines")
    plt.title("Deadline Miss Comparison")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
