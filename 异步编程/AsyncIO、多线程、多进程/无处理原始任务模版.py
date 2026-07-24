import time


def do_work(task_id, duration):
    time.sleep(duration)
    return f"Task {task_id} completed"


def run_sync(tasks=5):
    results = []
    for i in range(tasks):
        result = do_work(i, duration=0.1)
        results.append(result)
    return results


start_time = time.perf_counter()
results = run_sync(tasks=5)
elapsed_time = time.perf_counter() - start_time

print("Synchronous Results:")
for result in results:
    print(f" {result}")

print(f"\nTotal time: {elapsed_time} seconds")
print("Note: Task s ran one after another (synchronous execution)")


