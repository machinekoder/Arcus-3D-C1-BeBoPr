#!/usr/bin/env python

import sys
import os
import subprocess
import time
from machinekit import launcher
from machinekit import config


launcher.register_exit_handler()
#launcher.set_debug_level(5)
os.chdir(os.path.dirname(os.path.realpath(__file__)))
launcher.set_machinekit_ini(config.MACHINEKIT_INI)

try:
    launcher.check_installation()
    launcher.cleanup_session()
    launcher.register_exit_handler()  # needs to executed after HAL files
    launcher.load_bbio_file('bebopr_cape.bbio')

    nc_path = os.path.expanduser('~/nc_files')
    if not os.path.exists(nc_path):
        os.mkdir(nc_path)

    launcher.ensure_mklauncher()  # ensure mklauncher is started

    launcher.start_process("configserver -n 'Arcus-3D-C1 ~/Machineface")
    launcher.start_process('machinekit arcus-3d-c1.ini')
    while True:
        launcher.check_processes()
        time.sleep(1)
except subprocess.CalledProcessError:
    launcher.end_session()
    sys.exit(1)

sys.exit(0)
