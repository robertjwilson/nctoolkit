import glob
import os
import multiprocessing

import nctoolkit

session_info = dict()
if __name__ == "__main__":

    with multiprocessing.Manager() as manager:
        nc_safe_par = manager.list()
nc_safe = list()