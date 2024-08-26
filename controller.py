import pyfirmata

comport = "COM17"

board = pyfirmata.Arduino(comport)


led1 = board.get_pin("d:3:o")
led2 = board.get_pin("d:4:o")
led3 = board.get_pin("d:5:o")
led4 = board.get_pin("d:6:o")
led5 = board.get_pin("d:7:o")


def led(fingerUp):
    if fingerUp == [0, 0, 0, 0, 0]:
        led1.write(0)
        led2.write(0)
        led3.write(0)
        led4.write(0)
        led5.write(0)

    elif fingerUp == [0, 1, 0, 0, 0]:
        led1.write(1)
        led2.write(0)
        led3.write(0)
        led4.write(0)
        led5.write(0)
    elif fingerUp == [0, 1, 1, 0, 0]:
        led1.write(1)
        led2.write(1)
        led3.write(0)
        led4.write(0)
        led5.write(0)
    elif fingerUp == [0, 1, 1, 1, 0]:
        led1.write(1)
        led2.write(1)
        led3.write(1)
        led4.write(0)
        led5.write(0)
    elif fingerUp == [0, 1, 1, 1, 1]:
        led1.write(1)
        led2.write(1)
        led3.write(1)
        led4.write(1)
        led5.write(0)
    elif fingerUp == [1, 1, 1, 1, 1]:
        led1.write(1)
        led2.write(1)
        led3.write(1)
        led4.write(1)
        led5.write(1)
