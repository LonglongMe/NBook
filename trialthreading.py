import threading  
import time  
  
# 定义一个线程类  
class MyThread(threading.Thread):  
    def __init__(self, name):  
        threading.Thread.__init__(self)  
        self.name = name  
  
    # 重写 run 方法  
    def run(self):  
        print(f"开始线程： {self.name}")  
        for i in range(5):  
            time.sleep(1)  
            print(f"线程 {self.name} 正在运行... {i}")  
        print(f"退出线程： {self.name}")  
  
# 创建线程实例  
thread1 = MyThread("Thread-1")  
thread2 = MyThread("Thread-2")  
  
# 启动线程  
thread1.start()  
thread2.start()  
  
# 等待所有线程完成  
thread1.join()  
thread2.join()  
  
print("所有线程执行完毕")