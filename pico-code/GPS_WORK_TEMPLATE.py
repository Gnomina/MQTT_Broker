# More details can be found in TechToTinker.blogspot.com
# George Bantique | tech.to.tinker@gmail.com
# https://github.com/inmcm/micropyGPS/tree/master "lib repo"

from machine import Pin, UART
from micropyGPS import MicropyGPS


def main():
    uart = UART(0, baudrate=9600, bits=8, parity=None,
                stop=1, timeout=5000, rxbuf=1024)
    gps = MicropyGPS()

    while True:
        buf = uart.readline()

        for char in buf:
            # Note the conversion to to chr, UART outputs ints normally
            gps.update(chr(char))

        print('UTC Timestamp:', gps.timestamp)
        print('Date:', gps.date_string('long'))
        print('Satellites:', gps.satellites_in_use)
        print('Altitude:', gps.altitude)
        print('Latitude:', gps.latitude)
        print('Longitude:', gps.longitude_string())
        print('Horizontal Dilution of Precision:', gps.hdop)
        print('Speed km/h', round(gps.speed[2], 2))
        print()


# def startGPSthread():
#     _thread.start_new_thread(main, ())

if __name__ == "__main__":
    print('...running main, GPS testing')
    main()
