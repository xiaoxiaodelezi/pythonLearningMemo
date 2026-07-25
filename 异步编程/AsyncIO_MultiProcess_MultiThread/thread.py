# 多线程并发，
# 适合IO较多的时候

import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def do_work(task_id, duration):
    time.sleep(duration)
    return f"Task {task_id} completed"


def run_threading(tasks, max_works=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_works) as executor:
        futures = [executor.submit(do_work, i, 0.1) for i in range(tasks)]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    return results


if __name__ == "__main__":
    start_time = time.perf_counter()
    results = run_threading(tasks=5)
    elapsed_time = time.perf_counter() - start_time

    print("Threading Results:")
    for result in results:
        print(f" {result}")

    print(f"\nTotal time: {elapsed_time} seconds")
    print("Note: Tasks ran concurrently using threads (I/O-bound tasks)")
