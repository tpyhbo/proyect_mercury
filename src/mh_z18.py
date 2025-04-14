from machine import UART
import time

class MHZ18:
    def __init__(self, uart,tx, rx):
        self.uart = UART(2, baudrate=9600, tx=tx, rx=rx)

    def read_co2(self):
        cmd = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'
        self.uart.write(cmd)
        time.sleep(0.1)
        if self.uart.any():
            res = self.uart.read(9)
            if res and len(res) == 9 and res[0] == 0xFF and res[1] == 0x86:
                return res[2]*256 + res[3]
        return -1  # Error

    def read_co2_continuous(self,uart):
        while True:
            co2 = self.read_co2()
            print("CO2:", co2, "ppm")
            time.sleep(2)

    def set_detection_range(self, range_val):
        if range_val == 2000:
            cmd = b'\xFF\x01\x99\x00\x00\x07\xD0\x00\x2C'  # 0x07D0 = 2000
        elif range_val == 5000:
            cmd = b'\xFF\x01\x99\x00\x00\x13\x88\x00\xCB'  # 0x1388 = 5000
        else:
            return  # Not supported
        self.uart.write(cmd)
        time.sleep(0.1)
