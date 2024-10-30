"""
import pre_trendy


import pre_era5
import pre_fire
import pre_fluxcom
import pre_gome_sif
import pre_tm5_is
import pre_tm5_gosat
import subprocess
import multiprocessing
import threading
"""
"""
threads = []
t1 = threading.Thread(target=pre_tm5_gosat)
threads.append(t1)
t2 = threading.Thread(target=pre_tm5_is)
threads.append(t2)
t3 = threading.Thread(target=pre_gome_sif)
threads.append(t3)

for t in threads:
    t.start()
for t in threads:
    t.join()"""