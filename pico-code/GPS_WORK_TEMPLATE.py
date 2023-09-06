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

'''Ваша конкретная настройка фильтра Калмана принимает два основных параметра: process_variance и measurement_variance.

Process Variance (process_variance):

Этот параметр описывает, насколько быстро истинное состояние системы изменяется с течением времени.
Большие значения указывают, что истинное состояние может значительно изменяться между последовательными измерениями.
Меньшие значения указывают на то, что истинное состояние системы изменяется медленно.
Например, если вы отслеживаете положение автомобиля, который может резко ускоряться или тормозить, вы, возможно, захотите установить высокое значение процессной дисперсии.
Measurement Variance (measurement_variance):

Этот параметр описывает уровень шума или неточности измерений.
Большое значение указывает на высокий уровень шума в данных измерений.
Меньшее значение указывает на более точные измерения.
Например, если у вас есть датчик с низким качеством измерений или много внешних факторов, которые могут повлиять на измерение (например, GPS в плохих погодных условиях), вы можете установить высокое значение дисперсии измерений.
При настройке фильтра Калмана для вашей конкретной задачи важно экспериментировать с различными значениями process_variance и measurement_variance, чтобы определить оптимальные настройки. Эти параметры могут сильно влиять на работу фильтра, и правильная настройка может существенно улучшить результаты фильтрации.

В целом:

Если вы доверяете своим измерениям больше, чем прогнозам на основе прошлых данных, установите measurement_variance ниже, чем process_variance.
Если вы доверяете своим прогнозам на основе прошлых данных больше, чем текущим измерениям, установите process_variance ниже, чем measurement_variance.
Таким образом, фильтр Калмана будет корректировать свои прогнозы в зависимости от того, какой источник информации считается более надежным.'''
