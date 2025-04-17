import time
import binascii

import board
import busio
from digitalio import DigitalInOut

from adafruit_pn532.spi import PN532_SPI
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B


class NFCReader():
    key = b"\xFF\xFF\xFF\xFF\xFF\xFF"
    last_scan = 0
    scan_cd = 1 # seconds to wait between successful scans

    def __init__(self):
        # SPI connection:
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        cs_pin = DigitalInOut(board.D25)
        self.pn532 = PN532_SPI(spi, cs_pin, debug=False)

        ic, ver, rev, support = self.pn532.firmware_version
        print(f"Found PN532 with firmware version: {ver}.{rev} IC: {ic}")

        # Configure PN532 to communicate with MiFare cards
        self.pn532.SAM_configuration()
        self.pn532.listen_for_passive_target()

    def auth_card_for_reading(self, uid):
        authenticated = self.pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, self.key)
        if not authenticated:
            raise Exception("Authentication failed!")

    def get_data_from_card(self):
        # Must have called <auth_card_for_reading> before this step
        full_message = []
        for i in range(4, 6):
            for data in self.pn532.mifare_classic_read_block(i):
                hex_val = f"{data:02x}"

                # Remove cruft from beginning of the message
                if len(full_message) == 8 and full_message[5:] == ['54', '02', '65']:
                    full_message = []
                    continue

                # Stop recording when we reach the end of the message
                if hex_val in ['fe', '0']:
                    break

                full_message.append(hex_val)

        bytes_object = binascii.unhexlify(''.join(full_message))
        decoded = bytes_object.decode('ascii')
        return self._strip_non_ascii(decoded)
    
    def _strip_non_ascii(self, text):
        return "".join(
            char for char
            in text
            if 31 < ord(char) < 127
        )
    
    def scan_for_card(self):
        now = time.monotonic()
        data = None
        if self.last_scan + self.scan_cd > now:
            return data

        # Check if a card is available to read
        uid = self.pn532.read_passive_target(timeout=0.1)
        # Try again if no card is available.
        if uid is not None:
            self.last_scan = now
            try:
                self.auth_card_for_reading(uid)
                data = self.get_data_from_card()
            except Exception as e:
                print(f'NFC Error: {str(e)}')

        return data

    
    def scan_for_card_passive(self):
        now = time.monotonic()
        data = None
        if self.last_scan + self.scan_cd > now:
            return data
        
        uid = self.pn532.get_passive_target(timeout=0.01)
        if uid is not None:
            self.last_scan = now
            try:
                self.auth_card_for_reading(uid)
                data = self.get_data_from_card()
            except Exception as e:
                print(f'NFC Error: {str(e)}')

        return data

nfc = NFCReader()

loop_counter = 0
while True:
    now = time.monotonic()
    if data := nfc.scan_for_card_passive():
        print(data)

    loop_time = time.monotonic()
    loop_counter = (loop_counter + 1) % 100
    if loop_counter == 0:
        print(loop_time - now)