from time     import *   # Time library for delays

from DinoLog  import *   # DinoLog class for test


folder = "test_logs"

log1 = DinoLog(folder, "file1")
log2 = DinoLog(folder, "file2")

log1.log("message 1 on log 1")
sleep(1)
log2.log("message 1 on log 2")
sleep(1)
log2.log("message 2 on log 2")
log1.closeLog()
log1.log("message 2 on log 1")
