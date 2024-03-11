import pyb
import utime
import math

#servo_pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
#s_timer = pyb.Timer(5, freq=1000)
#PWM_timS = s_timer.channel(1, pyb.Timer.PWM, pin=servo_pin, pulse_width=8000)

#my_servo = servo.Servo(pin_id=servo_pin,min_deg=0.0,max_deg=270,freq=50)

my_servo = pyb.Servo(A0)

try:
    while True:
        my_servo.angle(0)
        utime.sleep(2)
        my_servo.angle(90)
        utime.sleep(2)
        my_servo.angle(-90)
        utime.sleep(2)
except KeyboardInterrupt:
    print("stopped the code")
