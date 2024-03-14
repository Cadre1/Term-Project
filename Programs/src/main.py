"""!
@file main.py
    This program sets up two tasks to run two different DC motors with encoders, 4 inter-task shared variables, and a queue.
    Upon the microcontroller's reset, the program will wait for an pair of input, Kps and position setpoints.
    A pair of encoders, motor drivers, and proportional contollers are then set up and controlled as separate cotasks with these input values.
    These cotasks are run without blocking each other and the responses are printed out.
"""

import gc
import pyb
import utime
import cotask
import task_share
import motor_driver
import encoder_reader
import mlx_cam
import motor_control
import servo
from machine import Pin, I2C

      
def task1_fun(shares):
    """!
    Task that determines how long each section of the shootout will last
    @param shares A list holding the three shares, Start_Flag, Stop_Flag, and Return_Flag used by this task
    """
    # Get references to the share and queue which have been passed to this task
    Start_Flag, Stop_Flag, Return_Flag, Button_Flag = shares
    # Init Yield
    yield 0
    
    state = 0
    while True:
        if state == 0:
            print('state 0 for task 1')
            # Initializes pins and timers
            pinB0 = pyb.ADC(pyb.Pin.board.PB0)
            # Initializes Intertask Flag variables
            Start_Flag.put(0)
            Stop_Flag.put(0)
            Return_Flag.put(0)
            Button_Flag.put(0)
            state = 1
            print('state 1 for task 1')
        elif state == 1:
            # Waits for an Input from the GPIO Pin
            # EDIT: Pass this state if we choose to just use the restart as our start the match trigger
            if (pinB0.read()*3.3/4095) >= 2:
                state = 2
                Button_Flag.put(1)
                print('state 2 for task 1')
            #state = 2
        elif state == 2:
            # Waits 5 seconds for the starting phase
            time_interval = 5000 # 5 second overall run time
            start_time = utime.ticks_ms()
            end_time = utime.ticks_add(start_time,time_interval)
            curr_time = start_time
            while utime.ticks_diff(end_time,curr_time) > 0:
                curr_time = utime.ticks_ms()
                yield 0
            Start_Flag.put(1)
            state = 3
            print('state 3 for task 1')
        elif state == 3:
            # Waits 10 seconds for the shooting phase
            time_interval = 10000 # 10 second overall run time
            start_time = utime.ticks_ms()
            end_time = utime.ticks_add(start_time,time_interval)
            curr_time = start_time
            while utime.ticks_diff(end_time,curr_time) > 0:
                curr_time = utime.ticks_ms()
                yield 0
            Start_Flag.put(0)
            Stop_Flag.put(1)
            state = 4
            print('state 4 for task 1')
        elif state == 4:
            # Waits 1 second for the stopping phase
            time_interval = 1000 # 1 second overall run time
            start_time = utime.ticks_ms()
            end_time = utime.ticks_add(start_time,time_interval)
            curr_time = start_time
            while utime.ticks_diff(end_time,curr_time) > 0:
                curr_time = utime.ticks_ms()
                yield 0
            Stop_Flag.put(0)
            Return_Flag.put(1)
            state = 5
            print('state 5 for task 1')
        elif state == 5:
            # Waits 3 seconds for the returning phase
            time_interval = 3000 # 3 second overall run time
            start_time = utime.ticks_ms()
            end_time = utime.ticks_add(start_time,time_interval)
            curr_time = start_time
            while utime.ticks_diff(end_time,curr_time) > 0:
                curr_time = utime.ticks_ms()
                yield 0
            Return_Flag.put(0)
        yield 0
            
      
def task2_fun(shares):
    """!
    Task that controls the targetting, panning, and firing of the nerf gun turret
    @param shares A list holding the three shares, Start_Flag, Stop_Flag, and Return_Flag used by this task
    """
    # Get references to the share and queue which have been passed to this task
    Start_Flag, Stop_Flag, Return_Flag, Button_Flag = shares
    # Init Yield
    yield 0
    
    state = 0
    while True:
        if state == 0:
            print('state 0 for task 2')
            # Initializes pins, timers, and I2C for the Panning Motor and Encoder, Flywheel GPIO Pin, IR Sensor, and Servo 

            # Initializes the GPIO Pin for the flywheel motor MOSFET
            PC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
            PC1.low()

            # Initializes the I2C for the IR Sensor
            i2c_bus = I2C(1)

            # Selects MLX90640 camera I2C address, normally 0x33, and check the bus
            i2c_address = 0x33
            scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
            print(f"I2C Scan: {scanhex}")

            # Creates the camera object and set it up in default mode
            camera = mlx_cam.MLX_Cam(i2c_bus)
            print(f"Current refresh rate: {camera._camera.refresh_rate}")
            camera._camera.refresh_rate = 10.0
            print(f"Refresh rate is now:  {camera._camera.refresh_rate}")
    
            # Initializes the Motor Pins and Timers
            a_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
            in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
            in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
            a_timer = pyb.Timer(3, freq=1000)

            # Creates the Motor Driver Object
            moe = motor_driver.MotorDriver(a_pin, in1pin, in2pin, a_timer)
            moe.enable()

            # Initializes the Encoder Counter and Pins
            timer_C = pyb.Timer(8, period=65535, prescaler=0)
            pinC6 = pyb.Pin(pyb.Pin.board.PC6)
            pinC7 = pyb.Pin(pyb.Pin.board.PC7)
            
            # Creates the Encoder Object
            enc = encoder_reader.Encoder(pinC6, pinC7, timer_C)
            
            # Motor Controller setup
            # Initializes Kp and setpoint
            des_pos = 0
            Kp = 0
            Ki = 0
            Kd = 0
            setpoint = 0
            
            # Creates the Motor Controller Object
            moe_con = motor_control.MotorControl(setpoint, Kp, Ki, Kd)
            
            # Initializes the Servo Pins and Timers
            servo_pin = pyb.Pin(pyb.Pin.board.PA8, pyb.Pin.OUT_PP)
            s_timer = pyb.Timer(1, prescaler=79, period=19999)
            my_servo = servo.Servo(pin=servo_pin, timer=s_timer, zero_angle=80)
            
            shoot = 1
            refire = 0 # EDIT: Adjust for the number of ADDITIONAL shots
            state = 1
            print('state 1 for task 2')
        elif state == 1:
            # Waits for the start of the shooting phase
            if Start_Flag.get():
                state = 2
                print('state 2 for task 2')
            
            # Can remove this else and the following while loop if we don't want to move during initial 5 seconds
            elif Button_Flag.get():  
                # Sets the setpoint and Kp
                des_pos = 80000
                setpoint = des_pos
                Kp = 0.25
                Ki = 0
                Kd = 0
                moe_con.set_gain(Kp, Ki, Kd)
                moe_con.set_setpoint(setpoint)
                    
                time_interval = 1000 # 1 second (1000ms) stay-within-range time
                range_interval = 1000 # 1000 count stay-within-range
                first_time = 1
                
                while True:
                    if Start_Flag.get():
                        state = 2
                        print('state 2 for task 2')
                        break
                    else:
                        curr_time = utime.ticks_ms()
                        pos = enc.read_position()
                        PWM = moe_con.run(pos, 7)
                        moe.set_duty_cycle(PWM)
                        # Checks if we are within the range interval of our desired position and starts the stay-within-range timer
                        if pos >= (des_pos-range_interval) and pos <= (des_pos+range_interval):
                            if first_time:
                                start_time = utime.ticks_ms()
                                end_time = utime.ticks_add(start_time,time_interval)
                                curr_time = start_time
                                first_time = 0
                            elif utime.ticks_diff(end_time,curr_time) < 0:
                                first_time = 1
                                moe.set_duty_cycle(0)
                                Button_Flag.put(0)
                                break
                        else:
                            first_time = 1
                    yield 0
        elif state == 2:
            # Determines the position that the turret needs to be at to be centered on the target
            if Stop_Flag.get():
                state = 5
                print('state 5 for task 2')
            else:
                Button_Flag.put(0)
                # Turns on the flywheel
                PC1.high()
                # Keeps trying to get an image until it collects one
                image = None
                while not image:
                    if Stop_Flag.get():
                        state = 5
                        print('state 5 for task 2')
                        break
                    image = camera.get_image_nonblocking()
                    yield 0
                
                # Processes image to get the centroid of the hottest region, ignoring temperatures less than 90% of the max
                ignore = [91, 100] # EDIT: Adjust until we get an appropriate/accurate shot (See camera outputs)
                centered = True
                x_bar_centroid, y_bar_centroid = camera.get_centroid(image, ignore, centered)
                x_bar_hotspot, y_bar_hotspot = camera.get_hotspot(image, centered)
                
                
                # Calculates the encoder position off of the horizontal position
                count_per_180 = 80000
                count_per_degree = count_per_180/180
                weight_dist = [70/100, 30/100] # EDIT: Adjust to make the effect of centroid or hotspot more impactful
                horz_angle_centroid = 55/32*x_bar_centroid
                horz_angle_hotspot = 55/32*x_bar_hotspot
                horz_angle = (horz_angle_centroid*weight_dist[0]+horz_angle_hotspot*weight_dist[1])/2
                print(f'Centroid X: {horz_angle_centroid}')
                print(f'Hotspot X: {horz_angle_hotspot}')
                print(f'Average X: {horz_angle}')
                
                dcount = horz_angle*count_per_degree
                des_pos = count_per_180 + dcount
                state = 3
                print('state 3 for task 2')
        elif state == 3:
            # Rotates the turret to the calculated encoder position
            if Stop_Flag.get():
                state = 5
                print('state 5 for task 2')
            else:
                # Turns on the flywheel
                PC1.high()
                
                # Sets the setpoint and Kp
                setpoint = des_pos
                Kp = 0.2 # EDIT: Adjust Kp if there is a lot of slip(?)
                Ki = 0 # EDIT: You shouldn't need to touch Ki or Kd. 
                Kd = 0 # TTS isn't that bad and slip is worse
                moe_con.set_gain(Kp, Ki, Kd)
                moe_con.set_setpoint(setpoint)
                
                time_interval = 100 # 0.75 second stay-within-range time
                range_interval = 2000 # 2000 count stay-within-range
                first_time = 1
                
                while True:
                    if Stop_Flag.get():
                        state = 5
                        print('state 5 for task 2')
                        break
                    else:
                        curr_time = utime.ticks_ms()
                        pos = enc.read_position()
                        PWM = moe_con.run(pos, 7)
                        moe.set_duty_cycle(PWM)
                        # Checks if we are within the range interval of our desired position and starts the stay-within-range timer
                        if pos >= (des_pos-range_interval) and pos <= (des_pos+range_interval):
                            if first_time:
                                start_time = utime.ticks_ms()
                                end_time = utime.ticks_add(start_time,time_interval)
                                curr_time = start_time
                                first_time = 0
                            elif utime.ticks_diff(end_time,curr_time) < 0:
                                first_time = 1
                                moe.set_duty_cycle(0)
                                state = 4
                                print('state 4 for task 2')
                                break
                        else:
                            first_time = 1
                    yield 0
        elif state == 4:
            # Uses the servo motor to pull the trigger
            if Stop_Flag.get():
                state = 5
                print('state 5 for task 2')
            else:
                if shoot:
                    # Move Servo to firing angle of 45 degrees.
                    my_servo.SetAngle(45)
                    refire -= 1
                    # Waits 0.1 second for the stopping phase
                    time_interval = 200
                    # 0.2 second overall run time (Changed from 0.1 to 0.2 to match Servo testing results
                    start_time = utime.ticks_ms()
                    end_time = utime.ticks_add(start_time,time_interval)
                    curr_time = start_time
                    while utime.ticks_diff(end_time,curr_time) > 0:
                        if Stop_Flag.get():
                            state = 5
                            break
                        curr_time = utime.ticks_ms()
                        yield 0
                    shoot = 0
                else:
                    my_servo.SetAngle(80)
                    PC1.low()
                    if refire >= 0:
                        shoot = 1
                        state = 2
        elif state == 5:
            # Stops all motor motion and resets servo
            PC1.low()
            moe.set_duty_cycle(0)
            my_servo.SetAngle(80)
            if Return_Flag.get():
                des_pos = 0
                state = 6
                print('state 6 for task 2')
        elif state == 6:
            # Returns to initial motor position, then disables the motor and waits
            # Sets the setpoint and Kp
            setpoint = des_pos
            Kp = 0.25
            Ki = 0
            Kd = 0
            moe_con.set_gain(Kp, Ki, Kd)
            moe_con.set_setpoint(setpoint)
                
            time_interval = 1000 # 1 second stay-within-range time
            range_interval = 2500 # 2500 count stay-within-range
            first_time = 1
                
            while True:
                pos = enc.read_position()
                PWM = moe_con.run(pos, 7)
                moe.set_duty_cycle(PWM)
                # Checks if we are within the range interval of our desired position and starts the stay-within-range timer
                if pos >= (des_pos-range_interval) and pos <= (des_pos+range_interval):
                    if first_time:
                        start_time = utime.ticks_ms()
                        end_time = utime.ticks_add(start_time,time_interval)
                        curr_time = start_time
                        first_time = 0
                    elif utime.ticks_diff(end_time,curr_time) > 0:
                        first_time = 1
                        moe.set_duty_cycle(0)
                        state = 4
                        break
                else:
                    first_time = 1
            moe.set_duty_cycle(0)
            moe.disable()
            while True:
                yield 0
        yield 0
        

# This code creates 4 shares, a queue, and 2 tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":

    # Create a share and a queue to test function and diagnostic printouts
    Start_Flag = task_share.Share('h', thread_protect=False, name="Start Flag")
    Stop_Flag = task_share.Share('h', thread_protect=False, name="Stop Flag")
    Return_Flag = task_share.Share('h', thread_protect=False, name="Return Flag")
    Button_Flag = task_share.Share('h', thread_protect=False, name="Button Flag")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=2, period=20,
                        profile=True, trace=False, shares=(Start_Flag, Stop_Flag, Return_Flag, Button_Flag))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=1, period=7,
                        profile=True, trace=False, shares=(Start_Flag, Stop_Flag, Return_Flag, Button_Flag))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

