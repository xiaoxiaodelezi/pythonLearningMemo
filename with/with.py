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
    
    def __exit__(self,exc_type,exc,tb):
        return exc_type is ZeroDivisionError
    
with SuppressZeroDivision():
    1/0 #不会报错
    
print("程序继续运行")
