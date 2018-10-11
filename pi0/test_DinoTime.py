from time     import *   # Time library for delays

from DinoTime  import *  # Class for test

# Initialize DinoTime class
DinoTime()

met1 = DinoTime.getMET()
sleep(1)
met2 = DinoTime.getMET()
DinoTime()
sleep(2)
met3 = DinoTime.getMET()

print("MET #1 = " + str(met1))
print("MET #2 = " + str(met2))
print("MET #3 = " + str(met3))

