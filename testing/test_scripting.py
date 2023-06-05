import glob
import os
from multiprocessing import Manager


session_info = dict()
mgr = Manager()
nc_safe = list()
nc_safe_par = Manager().list()