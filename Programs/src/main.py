"""!
@file main.py
    This program manages and allows two cotasks, task1_fun (Timing) and task2_fun (Shooting), to be run without blocking each other upon the microcontroller's reset.
    * Each of these tasks' finite state machines can be found in the README on Github.
    The Timing task initializes a pin to take an input from a button in which it then begins to track each of the required timers for the shootout.
    Each section of the shootout will have its corresponding flag set when each timer ends.
    The Shooting task initializes the pin controlling the MOSFET output to the Nerf gun flywheel, the I2C channel for the thermal camera, the pins and timers for the panning motor and encoder, and the pin, timer, and PID controller for the servo motor.
    This task will then manage the motor control for initial rotation using the motor driver, encoder, and PID controller, the centroid/hotspot detection using the thermal camera, the aiming at the determined centroid/hotspot, firing using the pin-to-flywheel circuit and servo motor, and rotation back to its starting point.
    During each of the shootout's sections, the states will be watching for changes in the timer's flag changes and change modes correspondingly. 
    * Tuning of controller gains, thermal readings, and timings may be adjusted per the requirements of operation by searching for "EDIT:" comments.
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
    Timing task that determines how long each section of the shootout will last
    @param shares A list holding the four shares, Start_Flag, Stop_Flag, Return_Flag, and Button_Flag set by this task
    """
    # Gets references to the shares which have been passed to this task
    Start_Flag, Stop_Flag, Return_Flag, Button_Flag = shares
    # Init yield
    yield 0
    
    # Timing task's state management
    state = 0
    while True:
        if state == 0:
            """!
            S0: Init
            Initializes the required pins and flags used in the Timing task
            """
            print('state 0 for task 1')
            # Initializes input pin for the starting button
            pinB0 = pyb.ADC(pyb.Pin.board.PB0)
            # Initializes intertask flag variables
            Start_Flag.put(0)
            Stop_Flag.put(0)
            Return_Flag.put(0)
            Button_Flag.put(0)
            state = 1
            print('state 1 for task 1')
        elif state == 1:
            """!
            S1: Wait For Input
            Waits for an input from the initialized GPIO pin wired to the starting button
            """
            # Checks if the starting button pin reads a voltage greater than 2V (should be around 3.3V minus voltage drops across wires and resistors)
            # Then changes state and sets the Button_Flag
            if (pinB0.read()*3.3/4095) >= 2:
                state = 2
                Button_Flag.put(1)
                print('state 2 for task 1')
        elif state == 2:
            """!
            S2: Wait For Start
            Waits 5 seconds for the starting phase, in which the target can move around, to end
            """
            # Sets up a 5 second timer to wait until it elapses
            # Then changes state and sets the Start_Flag
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
            """!
            S3: Wait For Stop
            Waits 10 seconds for the shooting phase, in which the turret is allowed to fire, to end
            """
            # Sets up a 10 second timer to wait until it elapses
            # Then changes state and sets the Stop_Flag
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
            """!
            S4: Stopped
            Waits 1 second for the for the turret to stop before returning to its original position
            """
            # Sets up a 1 second timer to wait until it elapses
            # Then changes state and sets the Return_Flag
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
            """!
            S5: Return
            Waits 3 seconds for the for the turret to return to its original position
            """
            # Sets up a 3 second timer to wait until it elapses
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
    Shooting task that controls the targetting, panning, and firing of the Nerf gun turret with its timings to change certain states set by the Timer task
    @param shares A list holding the three shares, Start_Flag, Stop_Flag, Return_Flag, and Button_Flag used by this task
    """
    # Get references to the share and queue which have been passed to this task
    Start_Flag, Stop_Flag, Return_Flag, Button_Flag = shares
    # Init yield
    yield 0
    
    # Shooting task's state management
    state = 0
    while True:
        if state == 0:
            """!
            S0: Init
            Initializes the required pins, timers, I2C channels, drivers, controller variables, and miscellaneous setting variables for the panning motor, encoder, flywheel GPIO pin, thermal camera, and servo
            """
            print('state 0 for task 2')

            # Initializes the GPIO Pin for the flywheel motor MOSFET
            PC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
            PC1.low()

            # Initializes the I2C for the thermal camera
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
    
            # Initializes the motor pins and timers
            a_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
            in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
            in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
            a_timer = pyb.Timer(3, freq=1000)
            # Creates the motor driver object
            moe = motor_driver.MotorDriver(a_pin, in1pin, in2pin, a_timer)
            moe.enable()

            # Initializes the encoder counter and pins
            timer_C = pyb.Timer(8, period=65535, prescaler=0)
            pinC6 = pyb.Pin(pyb.Pin.board.PC6)
            pinC7 = pyb.Pin(pyb.Pin.board.PC7)
            # Creates the encoder object
            enc = encoder_reader.Encoder(pinC6, pinC7, timer_C)
            
            # PID controller setup
            # Initializes controller gains and setpoint
            des_pos = 0
            Kp = 0
            Ki = 0
            Kd = 0
            setpoint = 0
            # Creates the motor controller object
            moe_con = motor_control.MotorControl(setpoint, Kp, Ki, Kd)
            
            # Initializes the servo pins and timers
            servo_pin = pyb.Pin(pyb.Pin.board.PA8, pyb.Pin.OUT_PP)
            s_timer = pyb.Timer(1, prescaler=79, period=19999)
            my_servo = servo.Servo(pin=servo_pin, timer=s_timer, zero_angle=80)
            
            # Miscellaneous setting variables
            shoot = 1
            refire = 0 # EDIT: Adjust for the number of ADDITIONAL shots
            state = 1
            print('state 1 for task 2')
        elif state == 1:
            """!
            S3: Wait For Start
            Rotates the turret 180 degrees and waits during the initial 5 seconds until the Timer task sets the Start_Flag
            """
            # Waits for the start of the shooting phase
            if Start_Flag.get():
                state = 2
                print('state 2 for task 2')
            
            # Rotates the turret 180 degrees (count of 80000)
            elif Button_Flag.get():  
                # Sets the setpoint corresponding to 180 degrees and sets the gains for the controller
                des_pos = 80000
                setpoint = des_pos
                Kp = 0.25
                Ki = 0
                Kd = 0
                moe_con.set_gain(Kp, Ki, Kd)
                moe_con.set_setpoint(setpoint)
                    
                # Runs the PID controlled motor until the encoder reads that the motor position is within a stay-within-range, range_interval, for a stay-within-range time, time_interval
                time_interval = 1000 # 1 second stay-within-range time
                range_interval = 1000 # 1000 count stay-within-range
                first_time = 1 # Check for initial stay-within-range
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
                        # Checks if we are within the stay-within-range interval of our desired position and starts the stay-within-range timer
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
            """!
            S2: Locate
            Uses the thermal camera to determine the centroid/hotspot where the target should be locatedand calculates the required position the motor needs to move to
            """
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
                
                # Processes image to get the centroid and hotspot of the hottest region, ignoring temperatures besides those between the ignore range (%)
                ignore = [91, 100] # EDIT: Adjust until we get an appropriate/accurate shot (See camera outputs in mlx_cam.py if needed)
                centered = True # Boolean for x-y locations either from the top-left corner or from the center
                x_bar_centroid, y_bar_centroid = camera.get_centroid(image, ignore, centered)
                x_bar_hotspot, y_bar_hotspot = camera.get_hotspot(image, centered)
                
                # Calculates the angle of the weighted average of the centroid and hotspot X-positions for the 32x28 pixel resolution camera
                count_per_180 = 80000 # Counts per 180 degrees
                count_per_degree = count_per_180/180 # Count per every 1 degree
                weight_dist = [70/100, 30/100] # EDIT: Adjust to make the effect of centroid or hotspot more impactful
                horz_angle_centroid = 55/32*x_bar_centroid
                horz_angle_hotspot = 55/32*x_bar_hotspot
                horz_angle = (horz_angle_centroid*weight_dist[0]+horz_angle_hotspot*weight_dist[1])/2
                print(f'Centroid X: {horz_angle_centroid}')
                print(f'Hotspot X: {horz_angle_hotspot}')
                print(f'Weighted Average X: {horz_angle}')
                
                # Calculates the count position of the motor
                dcount = horz_angle*count_per_degree
                des_pos = count_per_180 + dcount
                state = 3
                print('state 3 for task 2')
        elif state == 3:
            """!
            S3: Target
            Uses the motor position calculated from the Locate state to rotate the turret correspondingly
            """
            # Rerotates the turret to the new located position
            if Stop_Flag.get():
                state = 5
                print('state 5 for task 2')
            else:
                # Turns on the flywheel
                PC1.high()
                # Sets the setpoint corresponding to the calculated position and sets the gains for the controller
                setpoint = des_pos
                Kp = 0.2 # EDIT: Adjust Kp if there is a lot of slip(?)
                Ki = 0 # EDIT: You shouldn't need to touch Ki or Kd. Time-to-speed isn't that bad and gear slip is worse.
                Kd = 0
                moe_con.set_gain(Kp, Ki, Kd)
                moe_con.set_setpoint(setpoint)
                
                # EDIT: Adjust time_interval and range_interval if you need shorter waiting time before firing and don't care as much about accuracy
                # (decrease time_interval, increase range_interval)
                time_interval = 100 # 0.1 second stay-within-range time
                range_interval = 2000 # 2000 count stay-within-range
                first_time = 1
                # Runs the PID controlled motor until the encoder reads that the motor position is within a stay-within-range, range_interval, for a stay-within-range time, time_interval
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
                        # Checks if we are within the stay-within-range interval of our desired position and starts the stay-within-range timer
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
            """!
            S4: Shoot
            Uses the flywheel and servo to pull the trigger and fire the Nerf dart at the motors set position
            """
            # Sets the servo position to either 45 for shooting or 80 for not shooting
            if Stop_Flag.get():
                state = 5
                print('state 5 for task 2')
            else:
                if shoot:
                    # Moves servo to firing angle of 45 degrees
                    my_servo.SetAngle(45)
                    refire -= 1
                    time_interval = 200 # 0.2 second overall run time
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
                    # Moves servo to non-firing angle of 80 degrees and turns the flywheel off
                    my_servo.SetAngle(80)
                    PC1.low()
                    # Resets the shooting state and reloactes the target if refire isn't less than 0
                    if refire >= 0:
                        shoot = 1
                        state = 2
        elif state == 5:
            """!
            S5: Stop
            Stops all motor motion and resets the servo
            """
            # Sets pins and motors to passive settings
            PC1.low()
            moe.set_duty_cycle(0)
            my_servo.SetAngle(80)
            # Waits until the 10 seconds for firing has elapsed before returning
            if Return_Flag.get():
                des_pos = 0
                state = 6
                print('state 6 for task 2')
        elif state == 6:
            """!
            S6: Return
            Rotates the turret back to 0 degrees and disables the motors and waits
            """
            # Sets the setpoint to 0 degrees and sets the gains for the controller
            setpoint = des_pos
            Kp = 0.25
            Ki = 0
            Kd = 0
            moe_con.set_gain(Kp, Ki, Kd)
            moe_con.set_setpoint(setpoint)
                
            time_interval = 1000 # 1 second stay-within-range time
            range_interval = 2500 # 2500 count stay-within-range
            first_time = 1
            
            # Runs the PID controlled motor until the encoder reads that the motor position is within a stay-within-range, range_interval, for a stay-within-range time, time_interval
            while True:
                pos = enc.read_position()
                PWM = moe_con.run(pos, 7)
                moe.set_duty_cycle(PWM)
                # Checks if we are within the stay-within-range interval of our desired position and starts the stay-within-range timer
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
            
            # Turns off the motor and waits
            moe.set_duty_cycle(0)
            moe.disable()
            while True:
                yield 0
        yield 0
        

# This code creates 4 shares and 2 tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops.
if __name__ == "__main__":
    # Creates 4 shares to be intertask variables
    Start_Flag = task_share.Share('h', thread_protect=False, name="Start Flag")
    Stop_Flag = task_share.Share('h', thread_protect=False, name="Stop Flag")
    Return_Flag = task_share.Share('h', thread_protect=False, name="Return Flag")
    Button_Flag = task_share.Share('h', thread_protect=False, name="Button Flag")

    # Creates the tasks two cotasks. If trace is enabled for any task, memory will be
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

