# asyncIO
# 不使用线程
# 利用带有事件循环的单线程来管理多个协程
# 处理IO任务时比多线程方法更加高效，没有管理线程的开销
# 非常适合需要爬虫，API调用和其他需要网络等待的场景
# 本质还是单线程

import asyncio
import time


async def do_async_work(task_id, duration):
    await asyncio.sleep(duration)
    return f"Task {task_id} completed"


async def run_asyncio(task=5):
    task_list = [do_async_work(i, 0.1) for i in range(task)]
    results = await asyncio.gather(*task_list)
    return results


if __name__ == "__main__":
    start_time = time.perf_counter()
    results = asyncio.run(run_asyncio(task=5))
    elapsed_time = time.perf_counter() - start_time
    
    print("Asyncio Results:")
    for result in results:
        print(f" {result}")

    print(f"\nTotal time: {elapsed_time: 2f} seconds")
    print("Note: Tasks ran concurrently using asyncio (modern I/O-bound approach)")
