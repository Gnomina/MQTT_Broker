# More details can be found in TechToTinker.blogspot.com
# George Bantique | tech.to.tinker@gmail.com
# https://github.com/inmcm/micropyGPS/tree/master "lib repo"

from machine import Pin, UART
from micropyGPS import MicropyGPS


class KalmanFilter:
    def __init__(self, process_variance, measurement_variance, initial_value=0, initial_estimate_error=1):
        # Исходные значения
        self.estimate = initial_value  # Оценка
        self.estimate_error = initial_estimate_error  # Ошибка оценки
        # Дисперсия процесса (как быстро наше истинное значение изменяется во времени)
        self.process_variance = process_variance
        # Дисперсия измерения (как точны наши измерения)
        self.measurement_variance = measurement_variance

    def update(self, measurement):
        # Прогноз
        prediction = self.estimate
        prediction_error = self.estimate_error + self.process_variance

        # Коррекция
        kalman_gain = prediction_error / \
            (prediction_error + self.measurement_variance)
        self.estimate = prediction + kalman_gain * (measurement - prediction)
        self.estimate_error = (1 - kalman_gain) * prediction_error

        return self.estimate


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

        kf = KalmanFilter(process_variance=1, measurement_variance=2)

        speed_measurement = gps.speed[2]
        estimate = kf.update(speed_measurement)
        print(
            f"Measurement: {speed_measurement:.2f}, Estimate: {estimate:.2f}")


# def startGPSthread():
#     _thread.start_new_thread(main, ())

if __name__ == "__main__":
    print('...running main, GPS testing')
    main()
