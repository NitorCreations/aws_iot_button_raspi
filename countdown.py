from sense_hat import SenseHat
import time
# from datetime import datetime

s = SenseHat()
# s.low_light = True

green = (0, 255, 0)
red = (255, 0, 0)
LEDs = 64
steps_per_LED = 256
total_LED_steps = LEDs * steps_per_LED
COLOR_MAX = 255
duration = 10*1000


def millis():
    # return int((datetime.datetime.utcnow() -
    # datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
    return int(round(time.time() * 1000))


start_time = millis()
countdown_zero = start_time


def init():
    # print "init!"
    global countdown_zero
    countdown_zero = millis() + duration


init()


def tick(time_left):
    percentage = time_left / duration
    current_LED_step = round(total_LED_steps * percentage, 0)
    pixels = [pixel(i, current_LED_step) for i in range(64)]
    s.set_pixels(pixels)


def pixel(i, current_step):
    my_min_step = steps_per_LED * i
    my_max_step = steps_per_LED * i + steps_per_LED - 1
    if my_min_step <= current_step and my_max_step >= current_step:
        my_percentage = (current_step - my_min_step) / steps_per_LED
        if my_percentage >= 0.5:
            my_red = min(2 * int(round(COLOR_MAX - (COLOR_MAX * my_percentage),
                                       0)), 255)
            my_green = 255
        else:
            my_red = 255
            my_green = min(2 * int(round(COLOR_MAX * my_percentage, 0)), 255)
        return (my_red, my_green, 0)
    elif my_max_step < current_step:
        return green
    else:
        return red


while True:
    if s.stick.get_events():
        init()
    time_left = max(countdown_zero - millis(), 0)
    if not time_left:
        tick(time_left)
        time.sleep(1)
    else:
        tick(time_left)
        time.sleep(.01)
