from backend.config import TASKS


def generate_jobs(product_count=8):
    jobs = []
    arrival_gap = 8

    for product_index in range(1, product_count + 1):
        base_arrival = product_index * arrival_gap
        product_id = f"P{product_index:03d}"

        for task_name, task_data in TASKS.items():
            jobs.append({
                "job_id": f"{product_id}_{task_name}",
                "product_id": product_id,
                "task": task_name,
                "arrival_time": base_arrival,
                "burst_time": task_data["burst"],
                "absolute_deadline": base_arrival + task_data["deadline"]
            })

    return jobs


def run_edf_scheduler(product_count=8):
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

        ready_queue.sort(key=lambda job: job["absolute_deadline"])
        current_job = ready_queue.pop(0)

        start_time = time
        completion_time = start_time + current_job["burst_time"]
        deadline_missed = completion_time > current_job["absolute_deadline"]

        completed.append({
            **current_job,
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": start_time - current_job["arrival_time"],
            "turnaround_time": completion_time - current_job["arrival_time"],
            "deadline_missed": deadline_missed
        })

        time = completion_time

    return completed


if __name__ == "__main__":
    schedule = run_edf_scheduler()
    for row in schedule:
        print(row)
