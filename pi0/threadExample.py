from threading import Thread
from time import sleep

def threaded_function(arg):
   for i in range(arg):
      print("running")
      sleep(1)
   

if __name__ == "__main__":
   thread = Thread(target = threaded_function, args = (10, ))
   print("Is thread alive? " + str(thread.is_alive()))
   thread.start()
   while(thread.is_alive() == True):
      print("Is thread alive? " + str(thread.is_alive()))
      sleep(0.5)
   print("Is thread alive? " + str(thread.is_alive()))
   thread.join()
   print("thread finished...exiting")
