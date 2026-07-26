# with 本质是try final的语法糖
# with可以做到
# 1.异常也能保证close/flush
# 2.锁一定会释放，避免死锁
# 3.链接一定会断开/归还，避免耗尽
# 4.清理成为默认而不是记忆
# with 表达式（）as 变量：
# 变量=表达式（）.__enter__()
# with后跟的一定是一个上下文的管理器

# mgr = open("data.txt","r",encoding="utf-8")
# f = mgr.__enter__()
# try:
#     data = f.read()
# finally:
#     mgr.__exit__(None,None,None)

import time


class Time:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start
        print(f"耗时：{self.elapsed:.4f}s")
        return False  # return False的意思是万一有异常，还是会抛出的


def slow_function():
    time.sleep(5)


with Time() as t:
    slow_function()
print("耗时秒数: ", t.elapsed)

# __exit__(exc_type,exc,tb)
# exc_type 异常类型
# exc 异常对象
# tb 调用栈信息
# return True，抑制异常；return False 异常继续抛出


class SuppressZeroDivision:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc, tb):
        return exc_type is ZeroDivisionError


with SuppressZeroDivision():
    1 / 0  # 不会报错

print("程序继续运行")


# 标准库contextlib提供with解决异常的方法
from contextlib import suppress

with suppress(ZeroDivisionError):
    1 / 0

print("异常不会抛出")


# 生成器写法
from contextlib import contextmanager


# open_file返回的是一个生成器，生成器不支持with
# 需要通过@contextmanager来装饰成生成器
@contextmanager
def open_file(path):
    f = open(path, "r", encoding="utf-8")
    try:
        yield f
    finally:
        f.close()


with open_file("data.txt") as f:
    print(f.readline())


# nullcontest

# closing

# 多个上下文的管理
# enter顺序是a，b，exit顺序是b，a。栈结构。
with (
    open("a.txt", "r", encoding="utf-8") as fa,
    open("a.txt", "r", encoding="utf-8") as fb,
):
    a = fa.read()
    b = fb.read()

print(len(a), len(b))


# ExitStack，动态管理多个文件
# 进入和退出顺序都是按照栈方式的
from contextlib import ExitStack

paths = ["a.txt", "b.txt", "c.txt"]
with ExitStack() as stack:
    files = [stack.enter_context(open(p, "r", encoding="utf-8")) for p in paths]
    contents = [f.read() for f in files]
    print(contents)
# 会自动退出


# ExitStack 登记callback
def cleanup(msg):
    print("cleanup", msg)


with ExitStack() as stack:
    stack.callback(cleanup, "离开 with 了") #关闭文件，然后执行callback
    f = stack.enter_context(open("data.txt", "r", encoding="utf-8"))
    text = f.read()
    print(text)


# 一些注意点
# 处理异常
# 1.__exit__ 如果return True，会吞掉所有异常，除非很能确定自己在suppress的错误对象，不然不要轻易使用
# 2.__enter__ 返回值。想拿到管理器本身，return self；想拿到资源，return 资源
# 3.异步时的with:async with + __aenter__/__aexit__

    