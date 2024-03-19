"""! @file servo.py
This program creates the class "Servo" which initializes the GPIO pins as PWM outputs for a servo motor.
This class also contains the ability to set the absolute and relative servo position.
"""
import pyb
import utime
import math

class Servo:
    """! 
    This class sets up a servo motor with angle control. 
    """
    def __init__(self, pin, timer, zero_angle):
        """! 
        Creates a servo motor by initializing GPIO pins as PWM outputs and turning off the motor for safety. 
        @param inpin The PWM pin used to control the servo position
        @param timer The corresponding timer for the PWM pin
        @param zero_angle The initial angle in which we want to base our relative positions from
        """
        try:
            # Initializing pins and timers
            self.pin = pyb.Pin(pin, pyb.Pin.OUT_PP)
            self.pin.low()
            self.zero = zero_angle
            self.PWM_tim = timer.channel(1, mode=pyb.Timer.PWM, pin=self.pin)
            if zero_angle > 270:
                raise ValueError("zero_angle larger than 270")
            elif zero_angle < 0:
                raise ValueError("zero_angle must be positive")
            # Setting the pulse width of the servo to the desired angle using datasheet specified values
            self.PWM_tim.pulse_width(int(zero_angle*(2500-500)/(270)+500))
            print("Servo class created, servo set to zero_angle")
        except ValueError as e:
            print('Error, Servo driver failed in initialization')
            print(e)
    
    
    def SetAngle(self, angle):
        """!
        This method sets the servo to a given angle in degrees.
        @param angle An angle ranging from 0 to 270 for absolute position.
        """
        try:
            if angle > 270:
                raise Exception("angle larger than 270")
            elif angle < 0:
                raise Exception("angle must be positive")
            # Setting the pulse width of the servo to the desired angle using datasheet specified values
            self.PWM_tim.pulse_width(int(angle*(2500-500)/(270)+500))
        except Exception as e:
            print("Error executing SetAngle")
            print(e)


    def SetDeflection(self, dangle):
        """!
        This method sets the servo to a given angular deflection from zero in degrees.
        @param dangle An angle ranging from (270-zero_angle) to negative zero_angle
        """
        try:
            if dangle + self.zero > 270:
                raise Exception("deflection exceeds motor limits")
            elif dangle + self.zero < 0:
                raise Exception("deflection exceeds motor limits")
            # Setting the pulse width of the servo to the desired angle using datasheet specified values
            self.PWM_tim.pulse_width(int((dangle + self.zero)*(2500-500)/(270)+500))
        except Exception as e:
            print("Error executing SetDeflection")
            print(e)


# Test Code
if __name__ == "__main__":
    servo_pin = pyb.Pin(pyb.Pin.board.PA8, pyb.Pin.OUT_PP)
    s_timer = pyb.Timer(1, prescaler=79, period=19999)
    my_servo = Servo(pin=servo_pin, timer=s_timer, zero_angle=80)
    try:
        my_servo.SetAngle(80)
        utime.sleep(2)
        my_servo.SetAngle(45)
        utime.sleep_ms(200)
        my_servo.SetAngle(80)
    except KeyboardInterrupt:
        print("stopped the code")
