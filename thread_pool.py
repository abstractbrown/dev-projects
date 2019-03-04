from concurrent.futures import ThreadPoolExecutor
import threading
import random





def task(n):
 print("Processing {}".format(n))

def main():
 print("Starting ThreadPoolExecutor")
 with ThreadPoolExecutor(max_workers=3) as executor:
   future = executor.submit(task, (2))
   future = executor.submit(task, (3))
   future = executor.submit(task, (4))
 print("All tasks complete")

if __name__ == '__main__':
 main()








# def task():
#     print("Executing our Task")
#     result = 0
#     i = 0
#     for i in range(10):
#         result = result + i
#     print("I: {}".format(result))
#     print("Task Executed {}".format(threading.current_thread()))
#
# def main():
#     executor = ThreadPoolExecutor(max_workers=3)
#     task1 = executor.submit(task)
#     task2 = executor.submit(task)
#
# if __name__ == '__main__':
#     main()