#!/usr/bin/env python
#Author: Darryl Beckham

import collections
import contextlib
import errno
import functools
import os
import signal
import subprocess
import sys
import time
import traceback
import pwd
import termios
from pprint import pprint

proc_fs = '/proc'
processes = []

class Process:
    #from /proc/<pid>/loginuid
    uid = None

    #from /proc/<pid>/stat
    pid = None
    cmd = None
    state = None
    parent_id = None
    pgrp_id = None
    session = None
    tty = None
    tpgid = None
    flags = None
    min_faults = None
    child_min_faults = None
    maj_fault = None
    child_maj_faults = None
    user_time = None
    kernel_time = None
    child_user_time = None
    child_kernel_time = None
    priority = None
    nice = None
    num_threads = None
    itrealvalue = None
    start_time = None
    vsize = None
    rss = None
    rsslim = None
    startcode = None
    endcode = None
    startstack = None
    stack_pointer = None
    instruction_pointer = None
    pending_signals = None
    blocked_signals = None
    sigignore = None
    sigcatch = None
    wchan = None
    nswap = None
    cnswap = None
    exit_signal = None
    processor = None
    rt_priority = None
    policy = None
    delayacct_blkio_ticks = None
    guest_time = None
    child_guest_time = None
    start_data = None
    end_data = None
    start_brk = None
    arg_start = None
    arg_end = None
    env_start = None
    env_end = None
    exit_code = None

    def getProcessInfo(self,pid):
        loginuid = os.path.join(proc_fs,pid,"loginuid")
        stat = os.path.join(proc_fs,pid,"stat")
        if os.path.exists(loginuid):
            with open(loginuid) as f:
                self.uid = int(f.readline().rstrip('\n'))
            f.close()
        if os.path.exists(stat):
            #change to account for large files
            with open(stat) as f:
                contents = f.read().split()
                self.pid = contents[0]
                self.cmd = contents[1]
                self.state = contents[2]
                self.parent_id = contents[3]
                self.pgrp_id = contents[4]
                self.session = contents[5]
                self.tty = contents[6]
                self.tpgid = contents[7]
                self.flags = contents[8]
                self.min_faults = contents[9]
                self.child_min_faults = contents[10]
                self.maj_fault = contents[11]
                self.child_maj_faults = contents[12]
                self.user_time = contents[13]
                self.kernel_time = contents[14]
                self.child_user_time = contents[15]
                self.child_kernel_time = contents[16]
                self.priority = contents[17]
                self.nice = contents[18]
                self.num_threads = contents[19]
                self.itrealvalue = contents[20]
                self.start_time = contents[21]
                self.vsize = contents[22]
                self.rss = contents[23]
                self.rsslim = contents[24]
                self.startcode = contents[25]
                self.endcode = contents[26]
                self.startstack = contents[27]
                self.stack_pointer = contents[28]
                self.instruction_pointer = contents[29]
                self.pending_signals = contents[30]
                self.blocked_signals = contents[31]
                self.sigignore = contents[32]
                self.sigcatch = contents[33]
                self.wchan = contents[34]
                self.nswap = contents[35]
                self.cnswap = contents[36]
                self.exit_signal = contents[37]
                self.processor = contents[38]
                self.rt_priority = contents[39]
                self.policy = contents[40]
                self.delayacct_blkio_ticks = contents[41]
                self.guest_time = contents[42]
                self.child_guest_time = contents[43]
                self.start_data = contents[44]
                self.end_data = contents[45]
                self.start_brk = contents[46]
                self.arg_start = contents[47]
                self.arg_end = contents[48]
                self.env_start = contents[49]
                self.env_end = contents[50]
                self.exit_code = contents[51]
            f.close()

for root, dirs, files in os.walk(proc_fs):
    for pid in dirs:
        if(pid.isdigit()):
            p = Process()
            p.getProcessInfo(pid)
            processes.append(p)

def ps():
    for process in processes:
        #print(process.uid, os.getuid())
        if process.uid == os.geteuid():
            print(pwd.getpwuid(process.uid)[0], process.pid, process.tty, process.start_time, process.cmd)

ps()