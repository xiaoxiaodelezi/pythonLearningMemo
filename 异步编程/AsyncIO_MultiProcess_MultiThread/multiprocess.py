# 多进程并发，
# 适合CPU密集计算的时候
# 每个任务都有自己的内存，所以无法直接共享变量
# 需要通过队列或者共享内存之类的机制来共享
# 必须通过__main__的方式作为入口，不然会出现问题


import time
from concurrent.futures import ProcessPoolExecutor, as_completed


def do_cpu_work(task_id, iteration):
    result = 0
    for i in range(iteration):
        result += i * i
    return f"Task {task_id} completed (result: {result})"


def run_multiprocessing(tasks=5, max_works=5):
    results = []
    with ProcessPoolExecutor(max_workers=max_works) as executor:
        futures = [executor.submit(do_cpu_work, i, 1000000) for i in range(tasks)]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    return results

if __name__=="__main__":
    start_time = time.perf_counter()
    results = run_multiprocessing(tasks=5,max_works=5)
    elapsed_time = time.perf_counter() - start_time

    print("Multiprocessing Results:")
    for result in results:
        print(f" {result}")

    print(f"\nTotal time: {elapsed_time} seconds")
    print("Note: Tasks ran in parallel using using separate processes (CPU-bound tasks)")


