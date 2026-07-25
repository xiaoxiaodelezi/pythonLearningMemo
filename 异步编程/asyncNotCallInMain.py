import asyncio
from datetime import datetime

startTime = datetime.now()

async def background_task():
    print("后台任务开始 时间戳：", (datetime.now() - startTime).seconds)
    await asyncio.sleep(10)
    print("后台任务完成 时间戳：", (datetime.now() - startTime).seconds)
    return "后台有数据"

async def main():
    print("主程序开始   时间戳：", (datetime.now() - startTime).seconds)
    task = asyncio.create_task(background_task())
    print("主程序继续1  时间戳：", (datetime.now() - startTime).seconds)
    await asyncio.sleep(5)
    print("主程序继续2  时间戳：", (datetime.now() - startTime).seconds)
    # 不调用 await task
    res = await task
    print(
        "接收到task返回的数据", res, "  时间戳：", (datetime.now() - startTime).seconds
    )
    print("主线完成 时间戳：", (datetime.now() - startTime).seconds)


asyncio.run(main())