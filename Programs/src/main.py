"""!
@file main.py
    This program sets up two tasks to run two different DC motors with encoders, 4 inter-task shared variables, and a queue.
    Upon the microcontroller's reset, the program will wait for an pair of input, Kps and position setpoints.
    A pair of encoders, motor drivers, and proportional contollers are then set up and controlled as separate cotasks with these input values.
    These cotasks are run without blocking each other and the responses are printed out.
    
@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import utime
import cotask
import task_share
import motor_driver
import encoder_reader
import motor_control

def task1_fun(shares):
    """!
    Task that controls MotorB (The first motor)
    @param shares A list holding the two shares, share1(setpoint) and share2(Kp), and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    share1, share2, my_queue = shares


    # Motor setup from Lab1
    
    # Initializing the Motor Pins and Timers
    a_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    a_timer = pyb.Timer(3, freq=1000)

    # Creating the Motor Driver Object
    moe = motor_driver.MotorDriver(a_pin, in1pin, in2pin, a_timer)
    moe.enable()
    
    # Encoder setup from Lab2

    # Initializing the Encoder Counter and Pins
    timer_C = pyb.Timer(8, period=65535, prescaler=0)
    pinC6 = pyb.Pin(pyb.Pin.board.PC6)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7)
    
    # Creating the Encoder Object
    enc = encoder_reader.Encoder(pinC6, pinC7, timer_C)
    
    # Motor Controller setup
    
    # Initialize Kp and setpoint
    Kp = 0
    setpoint = 0
    
    # Creating the Motor Controller Object
    moe_con = motor_control.MotorControl(Kp, setpoint)
    
    # Sets the setpoint and Kp
    setpoint = share1.get()
    Kp = share2.get()
    moe_con.set_Kp(Kp)
    moe_con.set_setpoint(setpoint)
    
    # Init Yield
    yield 0
    
    # Runs the closed-loop motor position step response
    time_interval = 2000 # 1 second overall run time
    start_time = utime.ticks_ms()
    end_time = utime.ticks_add(start_time,time_interval)
    curr_time = start_time
    positions = []
    times = []
    while utime.ticks_diff(end_time,curr_time) > 0:
        curr_time = utime.ticks_ms()
        pos = enc.read_position()
        PWM = moe_con.run(pos)
        moe.set_duty_cycle(PWM)
        positions.append(pos)
        yield 0
    print("Start")
    moe_con.print_step_response(start_time)
    print("End")
    moe.disable()
        
    while True:
        yield 0


def task2_fun(shares):
    """!
    Task that controls MotorC (The second motor)
    @param shares A list holding the two shares, share1(setpoint) and share2(Kp), and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    share1, share2, my_queue = shares


    # Motor setup from Lab1
    
    # Initializing the Motor Pins and Timers
    a_pin = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    in1pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    a_timer = pyb.Timer(5, freq=1000)

    # Creating the Motor Driver Object
    moe = motor_driver.MotorDriver(a_pin, in1pin, in2pin, a_timer)
    moe.enable()
    
    # Encoder setup from Lab2

    # Initializing the Encoder Counter and Pins
    timer_B = pyb.Timer(4, period=65535, prescaler=0)
    pinB6 = pyb.Pin(pyb.Pin.board.PB6)
    pinB7 = pyb.Pin(pyb.Pin.board.PB7)
    
    # Creating the Encoder Object
    enc = encoder_reader.Encoder(pinB6, pinB7, timer_B)
    
    # Motor Controller setup
    
    # Initialize Kp and setpoint
    Kp = 0
    setpoint = 0
    
    # Creating the Motor Controller Object
    moe_con = motor_control.MotorControl(Kp, setpoint)
    
    # Sets the setpoint and Kp
    setpoint = share1.get()
    Kp = share2.get()
    moe_con.set_Kp(Kp)
    moe_con.set_setpoint(setpoint)
    
    # Init Yield
    yield 0
    
    # Runs the closed-loop motor position step response
    time_interval = 2000 # 1 second overall run time
    start_time = utime.ticks_ms()
    end_time = utime.ticks_add(start_time,time_interval)
    curr_time = start_time
    positions = []
    times = []
    while utime.ticks_diff(end_time,curr_time) > 0:
        curr_time = utime.ticks_ms()
        pos = enc.read_position()
        PWM = moe_con.run(pos)
        moe.set_duty_cycle(PWM)
        positions.append(pos)
        yield 0
    print("Start")
    moe_con.print_step_response(start_time)
    print("End")
    moe.disable()
        
    while True:
        yield 0


# This code creates 4 shares, a queue, and 2 tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    # Create a share and a queue to test function and diagnostic printouts
    share1 = task_share.Share('f', thread_protect=False, name="Share 1")
    share3 = task_share.Share('f', thread_protect=False, name="Share 3")
    q1 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 1")
    share2 = task_share.Share('f', thread_protect=False, name="Share 2")
    share4 = task_share.Share('f', thread_protect=False, name="Share 4")
    q2 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 2")


    # Prints "Input" to be read by "lab3.py"
    print("Input")
    while True:
        try:
            # Waits for an input position 1 to be .write() to the shell
            val = input()
            share1.put(int(val))
        except TypeError:
            # Returns "Invalid" if the input value is invalid
            print("Invalid")
        except ValueError:
            # Returns "Invalid" if the input value is invalid
            print("Invalid")
        else:
            # Otherwise returns "Valid" if the input value is valid
            print("Valid")
            break
        
    # Prints "Input" to be read by "lab3.py"
    print("Input")
    while True:
        try:
            # Waits for an input position 2 to be .write() to the shell
            val = input()
            share2.put(int(val))
        except TypeError:
            # Returns "Invalid" if the input value is invalid
            print("Invalid")
        except ValueError:
            # Returns "Invalid" if the input value is invalid
            print("Invalid")
        else:
            # Otherwise returns "Valid" if the input value is valid
            print("Valid")
            break
    
    # Prints "Input" to be read by "lab3.py"
    print("Input")
    while True:
        try:
            # Waits for an input Kp 1 to be .write() to the shell
            val = input()
            share3.put(float(val))
        except TypeError:
            # Returns "Invalid" if the input value is invalid
            print("Invalid")
        except ValueError:
            # Returns "Invalid" if the input value is invalid
            print("Invalid")
        else:
            # Otherwise returns "Valid" if the input value is valid
            print("Valid")
            break
    
    # Prints "Input" to be read by "lab3.py"
    print("Input")
    while True:
        try:
            # Waits for an input Kp 2 to be .write() to the shell
            val = input()
            share4.put(float(val))
        except TypeError:
            # Returns "Invalid" if the input value is invalid
            print("Invalid")
        except ValueError:
            # Returns "Invalid" if the input value is invalid
            print("Invalid")
        else:
            # Otherwise returns "Valid" if the input value is valid
            print("Valid")
            break
    

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=20,
                        profile=True, trace=False, shares=(share1, share3, q1))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=25,
                        profile=True, trace=False, shares=(share2, share4, q2))
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

