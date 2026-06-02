import os
import json
import pandas as pd
import matplotlib.pyplot as plt


SCHEDULER_FILES = {
    "EDF": "simulation_events/edf_schedule.json",
    "RMS": "simulation_events/rms_schedule.json",
    "FCFS": "simulation_events/fcfs_schedule.json",
    "Round Robin": "simulation_events/round_robin_schedule.json",
    "Priority": "simulation_events/priority_schedule.json"
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_metrics():
    rows = []

    for name, path in SCHEDULER_FILES.items():
        data = load_json(path)
        metrics = data["metrics"]

        rows.append({
            "algorithm": name,
            "total_jobs": metrics["total_jobs"],
            "missed_deadlines": metrics["missed_deadlines"],
            "average_waiting_time": metrics["average_waiting_time"],
            "average_turnaround_time": metrics["average_turnaround_time"]
        })

    return pd.DataFrame(rows)


def save_metric_chart(df, metric, title, ylabel, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.bar(df["algorithm"], df[metric])
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=220)
    plt.close()


def save_comparative_table(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)


def save_markdown_summary(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    best_deadline = df.sort_values("missed_deadlines").iloc[0]
    best_wait = df.sort_values("average_waiting_time").iloc[0]
    best_turnaround = df.sort_values("average_turnaround_time").iloc[0]

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("# Scheduling Comparative Analysis\n\n")
        file.write("## Algorithms Compared\n\n")
        file.write("- Earliest Deadline First\n")
        file.write("- First Come First Serve\n")
        file.write("- Round Robin\n")
        file.write("- Priority Scheduling\n")
        file.write("- Rate Monotonic Scheduling\n\n")

        file.write("## Metrics Table\n\n")
        file.write(df.to_markdown(index=False))
        file.write("\n\n")

        file.write("## Interpretation\n\n")
        file.write(
            f"- Best algorithm by missed deadlines: **{best_deadline['algorithm']}** "
            f"with **{int(best_deadline['missed_deadlines'])}** missed deadlines.\n"
        )
        file.write(
            f"- Best algorithm by average waiting time: **{best_wait['algorithm']}** "
            f"with **{best_wait['average_waiting_time']}** time units.\n"
        )
        file.write(
            f"- Best algorithm by average turnaround time: **{best_turnaround['algorithm']}** "
            f"with **{best_turnaround['average_turnaround_time']}** time units.\n\n"
        )

        file.write("## Case Study Interpretation\n\n")
        file.write(
            "In an AI-assisted visual inspection cell, deadline misses represent products "
            "reaching the actuator before the required sensing, inspection, decision, or logging "
            "tasks finish. Therefore, the most suitable algorithm is not merely the one with the "
            "lowest waiting time, but the one that protects time-critical inspection and rejection "
            "operations.\n\n"
        )

        file.write(
            "EDF is the most thematically suitable algorithm because the conveyor-based inspection "
            "cell is deadline-driven. RMS is also relevant because industrial control tasks often repeat "
            "periodically, and RMS gives higher priority to tasks with shorter periods. FCFS is simple but "
            "ignores urgency. Round Robin improves fairness but may fragment urgent work. Priority Scheduling "
            "can protect critical tasks such as sensor and actuator operations, but its effectiveness depends "
            "heavily on correct priority assignment.\n"
        )


def main():
    df = load_metrics()

    save_comparative_table(df, "visual_outputs/scheduling_comparative_metrics.csv")
    save_metric_chart(
        df,
        "missed_deadlines",
        "Missed Deadlines by Scheduling Algorithm",
        "Missed Deadlines",
        "visual_outputs/all_scheduler_deadline_comparison.png"
    )
    save_metric_chart(
        df,
        "average_waiting_time",
        "Average Waiting Time by Scheduling Algorithm",
        "Average Waiting Time",
        "visual_outputs/all_scheduler_waiting_time_comparison.png"
    )
    save_metric_chart(
        df,
        "average_turnaround_time",
        "Average Turnaround Time by Scheduling Algorithm",
        "Average Turnaround Time",
        "visual_outputs/all_scheduler_turnaround_comparison.png"
    )
    save_markdown_summary(df, "docs/SCHEDULING_COMPARATIVE_ANALYSIS.md")

    print(df)
    print("Saved comparative charts and docs/SCHEDULING_COMPARATIVE_ANALYSIS.md")


if __name__ == "__main__":
    main()
