from collections import deque
from backend.edf_scheduler import generate_jobs


def run_round_robin_scheduler(product_count=8, quantum=4):
    jobs = sorted(generate_jobs(product_count), key=lambda job: job["arrival_time"])

    pending_jobs = deque(jobs)
    ready_queue = deque()
    time = 0
    completed = []
    remaining_burst = {job["job_id"]: job["burst_time"] for job in jobs}
    first_start = {}

    while pending_jobs or ready_queue:
        while pending_jobs and pending_jobs[0]["arrival_time"] <= time:
            ready_queue.append(pending_jobs.popleft())

        if not ready_queue:
            if pending_jobs:
                time = pending_jobs[0]["arrival_time"]
            continue

        current_job = ready_queue.popleft()

        if current_job["job_id"] not in first_start:
            first_start[current_job["job_id"]] = time

        execution_time = min(quantum, remaining_burst[current_job["job_id"]])
        start_time = time
        completion_time = time + execution_time

        remaining_burst[current_job["job_id"]] -= execution_time
        time = completion_time

        while pending_jobs and pending_jobs[0]["arrival_time"] <= time:
            ready_queue.append(pending_jobs.popleft())

        if remaining_burst[current_job["job_id"]] > 0:
            ready_queue.append(current_job)
        else:
            deadline_missed = completion_time > current_job["absolute_deadline"]

            completed.append({
                **current_job,
                "start_time": first_start[current_job["job_id"]],
                "completion_time": completion_time,
                "waiting_time": completion_time - current_job["arrival_time"] - current_job["burst_time"],
                "turnaround_time": completion_time - current_job["arrival_time"],
                "deadline_missed": deadline_missed
            })

    return completed


if __name__ == "__main__":
    schedule = run_round_robin_scheduler()
    for row in schedule:
        print(row)
