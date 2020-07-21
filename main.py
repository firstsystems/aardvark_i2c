#!/usr/bin/env python3

# ==========================================================================
# IMPORTS
# ==========================================================================
from aai2c_eeprom import _writeMemory, _readMemory
from aardvark_py import *
from aai2c_eeprom import *

# ==========================================================================
# CONSTANTS
# ==========================================================================
BUS_TIMEOUT = 150  # ms

# ==========================================================================
# MAIN PROGRAM
# ==========================================================================

print("Reading PMIC")

if (len(sys.argv) < 7):
    print("usage: aai2c_eeprom PORT BITRATE read  SLAVE_ADDR OFFSET LENGTH")
    print("usage: aai2c_eeprom PORT BITRATE write SLAVE_ADDR OFFSET LENGTH")
    print("usage: aai2c_eeprom PORT BITRATE zero  SLAVE_ADDR OFFSET LENGTH")
    sys.exit()

port = int(sys.argv[1])
bitrate = int(sys.argv[2])
command = sys.argv[3]
device = int(sys.argv[4], 0)
addr = int(sys.argv[5], 0)
length = int(sys.argv[6])

handle = aa_open(port)
if (handle <= 0):
    print("Unable to open Aardvark device on port %d" % port)
    print("Error code = %d" % handle)
    sys.exit()

# Ensure that the I2C subsystem is enabled
aa_configure(handle, AA_CONFIG_SPI_I2C)

# Enable the I2C bus pullup resistors (2.2k resistors).
# This command is only effective on v2.0 hardware or greater.
# The pullup resistors on the v1.02 hardware are enabled by default.
aa_i2c_pullup(handle, AA_I2C_PULLUP_BOTH)

# Power the EEPROM using the Aardvark adapter's power supply.
# This command is only effective on v2.0 hardware or greater.
# The power pins on the v1.02 hardware are not enabled by default.
aa_target_power(handle, AA_TARGET_POWER_BOTH)

# Set the bitrate
bitrate = aa_i2c_bitrate(handle, bitrate)
print("Bitrate set to %d kHz" % bitrate)

# Set the bus lock timeout
bus_timeout = aa_i2c_bus_timeout(handle, BUS_TIMEOUT)
print("Bus lock timeout set to %d ms" % bus_timeout)

# Perform the operation
if (command == "write"):
    _writeMemory(handle, device, addr, length, 0)
    print("Wrote to EEPROM")

elif (command == "read"):
    _readMemory(handle, device, addr, length)

elif (command == "zero"):
    _writeMemory(handle, device, addr, length, 1)
    print("Zeroed EEPROM")

else:
    print("unknown command: %s" % command)

# Close the device
aa_close(handle)
