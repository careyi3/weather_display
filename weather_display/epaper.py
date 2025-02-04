import time
from micropython import const
from machine import SPI, Pin

# Display resolution
EPD_WIDTH = const(176)
EPD_HEIGHT = const(264)

# Display commands
SW_RESET = const(0x12)
SET_RAM_Y_ADDRESS = const(0x45)
SET_RAM_Y_ADDRESS_COUNTER = const(0x4F)
DATA_ENTRY_MODE = const(0x11)
WRITE_RAM = const(0x24)
DISPLAY_UPDATE_CONTROL = const(0x22)
ACTIVATE_DISPLAY_UPDATE = const(0x20)
SLEEP = const(0x10)

BUSY = const(1)  # 1=busy, 0=idle


class EPaper:
    class NotConfiguredException(Exception):
        "Device not configured: call config()"
        pass

    def __init__(self):
        print("Setting up epaper...")
        self.spi = SPI(2, baudrate=2000000)  # sck=18, mosi=23, miso=19
        self.cs = Pin(26, mode=Pin.OUT, value=1)
        self.dc = Pin(22, mode=Pin.OUT, value=0)
        self.rst = Pin(21, mode=Pin.OUT, value=0)
        self.bsy = Pin(17, mode=Pin.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.configured = False

    def __send_command(self, command):
        try:
            self.cs(0)
            self.dc(0)
            self.spi.write(bytearray([command]))
        finally:
            self.cs(1)

    def __send_data(self, data):
        try:
            self.cs(0)
            self.dc(1)
            self.spi.write(data)
        finally:
            self.cs(1)

    def __wait_until_idle(self):
        print("Waiting...")
        while self.bsy.value() == BUSY:
            time.sleep_ms(100)

    def __reset(self):
        print("Resetting...")
        self.rst(1)
        time.sleep_ms(200)
        self.rst(0)
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(200)

    def __refresh_display(self):
        if not self.configured:
            raise NotConfiguredException

        print("Refreshing Display...")
        self.__send_command(DISPLAY_UPDATE_CONTROL)
        self.__send_data(b"\xF7")
        self.__send_command(ACTIVATE_DISPLAY_UPDATE)
        self.__wait_until_idle()

    def config(self):
        print("Configuring epaper...")
        self.__reset()
        print("Reset waiting...")
        self.__wait_until_idle()

        print("Software reset...")
        self.__send_command(SW_RESET)
        print("Reset waiting...")
        self.__wait_until_idle()

        print("RAM Command...")
        self.__send_command(SET_RAM_Y_ADDRESS)
        print("RAM Data...")
        self.__send_data(b"\x00\x00\x07\x01")

        print("RAM Command...")
        self.__send_command(SET_RAM_Y_ADDRESS_COUNTER)
        print("RAM Data...")
        self.__send_data(b"\x00\x00")

        print("Data Mode Command...")
        self.__send_command(DATA_ENTRY_MODE)
        print("Data Mode Data...")
        self.__send_data(b"\x03")

        time.sleep_ms(2)

        print("Configured")

        self.configured = True

    def sleep(self):
        if not self.configured:
            raise NotConfiguredException

        print("Sleeping...")
        self.__send_command(SLEEP)
        self.__send_data(b"\x01")
        self.configured = False

    def display_frame(self, frame_buffer):
        if not self.configured:
            raise NotConfiguredException

        print("Writing Frame To Memory...")
        if frame_buffer != None:
            self.__send_command(WRITE_RAM)
            time.sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self.__send_data(bytearray([~int(frame_buffer[i])]))

            self.__refresh_display()
