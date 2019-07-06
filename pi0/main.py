from DinoMain import *

if(__name__ == "__main__"):
   print("Start Dino Experiment.")
   try:
      DinoMain().run()
   except:
      DinoLog.stop()
   print("End Dino Experiment.")

