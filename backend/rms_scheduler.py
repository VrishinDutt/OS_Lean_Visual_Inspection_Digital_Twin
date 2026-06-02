from backend.edf_scheduler import generate_jobs


TASK_PERIOD = {
    "sensor": 20,
    "camera": 40,
    "rule_inspection": 60,
    "ai_inspection": 100,
    "decision_fusion": 120,
    "actuator": 150,
    "logger": 300
}


def run_rms_scheduler(product_count=8):
    jobs = generate_jobs(product_count)
    time = 0
    completed = []
    ready_queue = []
    pending_jobs = sorted(jobs, key=lambda job: job["arrival_time"])

    while pending_jobs or ready_queue:
        while pending_jobs and pending_jobs[0]["arrival_time"] <= time:
            ready_queue.append(pending_jobs.pop(0))

        if not ready_queue:
            time = pending_jobs[0]["arrival_time"]
            continue

        ready_queue.sort(
            key=lambda job: (
                TASK_PERIOD.get(job["task"], 999),
                job["absolute_deadline"],
                job["arrival_time"]
            )
        )

        current_job = ready_queue.pop(0)

        start_time = time
        completion_time = start_time + current_job["burst_time"]
        deadline_missed = completion_time > current_job["absolute_deadline"]

        completed.append({
            **current_job,
            "period": TASK_PERIOD.get(current_job["task"], 999),
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": start_time - current_job["arrival_time"],
            "turnaround_time": completion_time - current_job["arrival_time"],
            "deadline_missed": deadline_missed
        })

        time = completion_time

    return completed


if __name__ == "__main__":
    schedule = run_rms_scheduler()
    for row in schedule:
        print(row)
