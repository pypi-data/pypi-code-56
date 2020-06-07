from bme280 import BME280
from bh1750 import BH1750
import time
import sys
from ads1115 import ADS1115
sys.path.append('./env/')


def main():
    print("===================== weather demo script ====================")

    time.sleep(1)

    bus = 0
    adc_addr = 0x48
    light_addr = 0x23
    bmp280_addr = 0x76

    a = ADS1115(bus, adc_addr)

    l = BH1750(bus, light_addr)

    b = BME280(bus, bmp280_addr)

    counter = 0

    try:
        while True:
            counter = counter + 1
            time.sleep(1)
            adc_0 = a.readAdc(0)
            adc_1 = a.readAdc(1)
            adc_2 = a.readAdc(2)
            adc_3 = a.readAdc(3)

            light = l.getLight()

            temp = b.read_temperature()
            pressure = b.read_pressure()
            humidity = b.read_humidity()

            print("adc: " + adc_0 + " " + adc_1 + " " + adc_2 + " " + adc_3 + " light: " +
                  light + " temp :" + temp + " pressure: " + pressure + " hum: " + humidity)

    except KeyboardInterrupt:
        print("Interrupt from keyboard")
        sys.exit(0)


if __name__ == "__main__":
    main()
