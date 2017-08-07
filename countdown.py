# from sense_emu import SenseHat, ACTION_PRESSED
from sense_hat import SenseHat, ACTION_PRESSED
import time
# from datetime import datetime

sense_hat = SenseHat()
# s.low_light = True

green = (0, 255, 0)
red = (255, 0, 0)
LEDs = 64
steps_per_LED = 256
total_LED_steps = LEDs * steps_per_LED
COLOR_MAX = 255
duration = 60 * 1000

push_callback = None


def millis():
    # return int((datetime.datetime.utcnow() -
    # datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
    return int(round(time.time() * 1000))


start_time = millis()
countdown_zero = start_time


def init(pushedAt, _duration):
    global countdown_zero, duration
    duration = _duration if _duration else duration
    countdown_zero = pushedAt + duration


def tick():
    for event in sense_hat.stick.get_events():
        if event.action == ACTION_PRESSED:
            pushedAt = millis()
            init(pushedAt, duration)
            if push_callback:
                push_callback(pushedAt, duration)
    time_left = max(countdown_zero - millis(), 0)
    percentage = time_left / duration
    current_LED_step = round(total_LED_steps * percentage, 0)
    sense_hat.set_pixels([pixel(i, current_LED_step) for i in range(LEDs)])
    return 0.01 if time_left else 0.5


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
