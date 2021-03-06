#!/usr/bin/env python
import struct
import smbus
import sys
import time

class UPS():
        
        def __init__(self):
                
                # Set the bus port either 1 or 0
                self.bus = smbus.SMBus(1)
                # set low capacity alert for the battery
                self.low_capacity = 20

        def read_voltage(self):

                # This function returns the voltage as float from the UPS-Lite via SMBus object
                address = 0x36
                read = self.bus.read_word_data(address, 2)
                swapped = struct.unpack("<H", struct.pack(">H", read))[0]
                voltage = swapped * 1.25 /1000/16
                return voltage


        def read_capacity(self):
                
                # This function returns the ramaining capacitiy in int as precentage of the battery connect to the UPS-Lite
                address = 0x36
                read = self.bus.read_word_data(address, 4)
                swapped = struct.unpack("<H", struct.pack(">H", read))[0]
                capacity = swapped/256
                return int(capacity)
        
        def is_battery_full(self,capacity):
                
                # This function returns True if the battery is full, else return False
                if(capacity == 100):
                        return True
                return False
        
        def is_battery_low(self,capacity):
                
                # This function returns True if the battery capacity is low, else return False
                if(capacity <= self.low_capacity):
                        return True
                return False
             
def main():
            
        ups_lite = UPS()
        voltage = ups_lite.read_voltage()
        capacity = ups_lite.read_capacity()
        is_low = ups_lite.is_battery_low(capacity)
        is_full = ups_lite.is_battery_full(capacity)
        
        print("[-] Voltage: %s" % voltage)
        print("[-] Capacitiy: %s" % capacity)
        
main()
