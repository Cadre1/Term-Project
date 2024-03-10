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
    def __init__(self, setpoint, Kp):
        """! 
        Creates a proportional controller by initializing the desired output
        and time lists as well as controller properties 
        @param setpoint The desired output  
        @param Kp The proportional controller gain
        """
        self.times = []
        self.positions = []
        self.setpoint = setpoint
        self.Kp = Kp
    
    
    def run(self, measured_output):
        """! 
        This method takes in the measured output of the plant and returns
        the effort out of the controller
        @param measured_output The current measured output of the plant
        @returns The output effort of the proportional controller
        """
        time = utime.ticks_ms()
        self.times.append(time)
        self.positions.append(measured_output)
        
        error = self.setpoint - measured_output
        output = self.Kp*error
        return output
    
    
    def set_setpoint(self, setpoint):
        """! 
        This method takes in the desired output and sets it
        @param setpoint The desired output of the plant  
        """
        self.setpoint = setpoint
        
        
    def set_Kp(self, Kp):
        """! 
        This method takes in the proportional controller gain and sets it
        @param Kp The proportional controller gain  
        """
        self.Kp = Kp
        
        
    def print_step_response(self, start_time):
        """! 
        This method takes in the start time of the system and prints out the
        measured positions with their respective time relative to the start time
        @param start_time The starting time of the step response
        """
        # Prints out "time, position" in CSV format
        for i in range(len(self.times)):
            print(f"{self.times[i]-start_time}, {self.positions[i]}")
    
        