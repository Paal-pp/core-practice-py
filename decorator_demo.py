from functools import wraps
import random
import time
"""
装饰器的练手代码
基于规定正确错误值的重试
基于异常的重试
计算时间的的重试
"""
def retry(func):
    @wraps(func) #(func)这个是一定要传入的这个不能忘！
    def wrapper(*args,**kwargs):
        print(f"{func.__name__}开始运行")
        result = func(*args,**kwargs)
        if result == False:
            retry_num = 1
            print(f"{func.__name__}运行失败，开启三次重试")
            while retry_num<3:
                print(f"重试第{retry_num}次")
                result = func(*args,**kwargs)
                if result == True:
                    break
                else:
                    retry_num =retry_num+1
        return result
    return wrapper

def retry_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                print(f"第{i+1}次执行")
                return func(*args, **kwargs)
            except Exception as e:
                print(f"执行失败: {e}")
                if i == 2:
                    print("三次都失败了，抛出异常")
                    raise
    return wrapper


def retry_num(max_retries = 3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print(f"{func.__name__} 开始运行")

            for attempt in range(max_retries + 1):
                result = func(*args, **kwargs)

                if result:
                    if attempt > 0:
                        print(f"{func.__name__} 在第 {attempt} 次重试后成功")
                    return result

                if attempt < max_retries:
                    print(f"{func.__name__} 运行失败，准备第 {attempt + 1} 次重试")
                else:
                    print(f"{func.__name__} 重试 {max_retries} 次后仍然失败")

            return False

        return wrapper

    return decorator

def time_calculation():
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            start = time.perf_counter()
            print(f"{func.__name}开始运行")
            result = func(*args,**kwargs)
            end = time.perf_counter()
            runtime = end - start
            print(f"{func.__name}运行结束,运行时间{runtime}")
            return result
        return wrapper
    return decorator


@retry
def randomnum1():
    num = random.randint(1, 2)
    if num == 1:
        return False
    else:
        return True
    
@retry_num(max_retry_num=4)
def randomnum2():
    num = random.randint(1, 2)
    if num == 1:
        return False
    else:
        return True


@time_calculation()
@retry_exception
def randomnum3():
    num = random.randint(1, 2)
    if num == 1:
        raise ValueError("随机失败一次")
    return "成功"


