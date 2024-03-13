import pyb
import utime
import math

class Servo:
    def __init__(self, pin, timer, zero_angle):
        """!
        Initializes a PWM channel to controll the servo.
        @param inpin The board pin used to control the servo
        @param timer The timer for the PWM
        """
        try:
            # Initializing Pins
            # Input pin
            self.pin = pyb.Pin(pin, pyb.Pin.OUT_PP)
            self.pin.low()
            self.zero = zero_angle
            self.PWM_tim = timer.channel(1, mode=pyb.Timer.PWM, pin=self.pin)
            if zero_angle > 270:
                raise ValueError("zero_angle larger than 270")
            elif zero_angle < 0:
                raise ValueError("zero_angle must be positive")
            self.PWM_tim.pulse_width(int(zero_angle*(2500-500)/(270)+500))
            print("Servo class created, servo set to zero_angle")
        except ValueError as e:
            print('Error, Servo driver failed in initialization')
            print(e)
    
    def SetAngle(self, angle):
        """!
        Method that sets the servo to a given angle in degrees.
        @param angle An angle ranging from 0 to 270.  This is absolute position.
        """
        try:
            if angle > 270:
                raise Exception("angle larger than 270")
            elif angle < 0:
                raise Exception("angle must be positive")
            self.PWM_tim.pulse_width(int(angle*(2500-500)/(270)+500))
        except Exception as e:
            print("Error executing SetAngle")
            print(e)

    def SetDeflection(self, dangle):
        """!
        Method that sets the servo to a given angular deflection from zero in degrees.
        @param dangle An angle ranging from (270-zero_angle) to negative zero_angle
        """
        try:
            if dangle + self.zero > 270:
                raise Exception("deflection exceeds motor limits")
            elif dangle + self.zero < 0:
                raise Exception("deflection exceeds motor limits")
            self.PWM_tim.pulse_width(int((dangle + self.zero)*(2500-500)/(270)+500))
        except Exception as e:
            print("Error executing SetDeflection")
            print(e)


if __name__ == "__main__":
    servo_pin = pyb.Pin(pyb.Pin.board.PA8, pyb.Pin.OUT_PP)
    s_timer = pyb.Timer(1, prescaler=79, period=19999)
    my_servo = Servo(pin=servo_pin, timer=s_timer, zero_angle=0)
    try:
        while True:
            my_servo.SetAngle(0)
            utime.sleep(2)
            my_servo.SetAngle(90)
            utime.sleep(2)
            #my_servo.SetDeflection(0)
            #utime.sleep(2)
            #my_servo.SetDeflection(90)
            #utime.sleep(2)
            #my_servo.SetDeflection(-90)
            #utime.sleep(2)
    except KeyboardInterrupt:
        print("stopped the code")
