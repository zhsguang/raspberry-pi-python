from __future__ import print_function

import sys

import qwiic_scmd

myMotor = qwiic_scmd.QwiicScmd()
myMotor.disable()
sys.exit(0)
