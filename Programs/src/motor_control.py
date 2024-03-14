"""! @file motor_control.py
This program creates the class "MotorControl" which initializes the required values for a proportional controller.
This class also contains the methods to calculate the required effort off of an input position, to set the setpoint and proportional controller gain, and to print out the step response data.
"""
import utime

class MotorControl:
    """! 
    This class creates a Proportional Gain Controller
    to be used with a motor-encoder system
    """
    def __init__(self, setpoint, Kp, Ki, Kd):
        """! 
        Creates a proportional controller by initializing the desired output
        and time lists as well as controller properties 
        @param setpoint The desired output  
        @param Kp The proportional controller gain
        """
        self.setpoint = setpoint
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        self.prev_error = 0
        self.integral_error = 0
        self.prev_time = 0
        self.first_time = 1
    
    
    def run(self, measured_output, delta_t):
        """! 
        This method takes in the measured output of the plant and returns
        the effort out of the controller
        @param measured_output The current measured output of the plant
        @returns The output effort of the proportional controller
        """
        curr_time = utime.ticks_ms()
        error = self.setpoint - measured_output
        if self.first_time:
            derror = 0
            self.first_time = 0
        else:
            derror = (error-self.prev_error)/(delta_t/1000)
            self.integral_error += error*(delta_t/1000)
            #derror = (error-self.prev_error)/(curr_time-self.prev_time)
            #self.integral_error += error*(curr_time-self.prev_time)
        self.prev_time = curr_time
        self.prev_error = error
        
        prop_output = error*self.Kp
        int_output = self.integral_error*self.Ki
        der_output = derror*self.Kd
        output = prop_output+int_output+der_output
        return output
    
    
    def set_setpoint(self, setpoint):
        """! 
        This method takes in the desired output and sets it
        @param setpoint The desired output of the plant  
        """
        self.setpoint = setpoint
        
        
    def set_gain(self, Kp, Ki, Kd):
        """! 
        This method takes in the proportional controller gain and sets it
        @param Kp The proportional controller gain  
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

if __name__ == "__main__":
    
    des_pos = 10
    curr_pos = 0
    con = MotorControl(0, 0, 0, 0)
    con.set_setpoint(des_pos)
    con.set_gain(0.25,0,0)
    while True:
        try:
            output = con.run(curr_pos, 10)
            curr_pos += output*0.01
            print(curr_pos)
            utime.sleep_ms(10)
        except:
            break