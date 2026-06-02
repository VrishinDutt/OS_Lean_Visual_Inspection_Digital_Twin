from backend.edf_scheduler import generate_jobs


def run_fcfs_scheduler(product_count=8):
    jobs = sorted(generate_jobs(product_count), key=lambda job: job["arrival_time"])

    time = 0
    completed = []

    for job in jobs:
        if time < job["arrival_time"]:
            time = job["arrival_time"]

        start_time = time
        completion_time = start_time + job["burst_time"]
        deadline_missed = completion_time > job["absolute_deadline"]

        completed.append({
            **job,
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": start_time - job["arrival_time"],
            "turnaround_time": completion_time - job["arrival_time"],
            "deadline_missed": deadline_missed
        })

        time = completion_time

    return completed


if __name__ == "__main__":
    schedule = run_fcfs_scheduler()
    for row in schedule:
        print(row)
