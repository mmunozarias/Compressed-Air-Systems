import serial                                       # Import serial(usb) support
import json                                         # Import JSON file format support
import os                                           # Find Operating system information
import time                                         # Import time specific functionality
import matplotlib.pyplot as plt                     # Import plotting package
import matplotlib.animation as animation            # import animated plot package for continuous plotting
from matplotlib import style                        # Import graph styles
from matplotlib.gridspec import GridSpec            # Import quadratic plot grid support
from matplotlib.backends.backend_pdf import PdfPages # Import PdfPages for saving to PDF
from dynamixel_sdk import *
import pandas as pd                                 # Import pandas for Excel handling

# Operating system-specific settings, used to deliver nice error messages. Can be ignored
if os.name == 'nt':                                 # Check if operating systems is windows
    import msvcrt                                   # import package for microsoft powershell functionality
    def getch():                                    # get keyboard input
        return msvcrt.getch().decode()
else:
    import sys, tty, termios                        # For Linux system get sys, tty and and termios package, sys give system information, tty and termios terminal functionality
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)            # Save terminal settings
    def getch():                                    # Get keyboard input
        try:
            tty.setraw(sys.stdin.fileno())          # Change terminal to raw input mode
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  #restore terminal settings
        return ch

# Dynamixel settings, function = Controltable ID for specific dynamixel. These values should not be changed when using the AX-12A series
ADDR_MX_TORQUE_ENABLE = 24
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_TORQUE_LIMIT = 34
ADDR_MX_PRESENT_POSITION = 36
PROTOCOL_VERSION = 1.0
# Dynamixel Connection Settings, you can find this information in the dynamixel wizard
DXL_ID = 0
BAUDRATE = 1000000
DEVICENAME = 'COM8'                 # Computer 
# Control setting values
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MINIMUM_POSITION_VALUE = 200        # These values correspond to a maximum angle change of 90 degrees
DXL_MAXIMUM_POSITION_VALUE = 512        # 200 degrees is fully closed 512 degrees is fully open
DXL_MOVING_STATUS_THRESHOLD = 0.5         # Degree of error allowed from goal angle.

# Initialize PortHandler and PacketHandler instances
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if not portHandler.openPort():
    print("Failed to open the port")
    getch()
    quit()

# Set port baudrate
if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the baudrate")
    getch()
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS or dxl_error != 0:
    print("Failed to enable torque")
    getch()
    quit()

# Define PID controller as a class function
class PID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.previous_error = 0
        self.integral = 0

    def compute(self, setpoint, pv):
        error = setpoint - pv
        self.integral += error
        derivative = error - self.previous_error
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.previous_error = error
        return output

# PID coefficient 
pid = PID(0.1, 0.02, 0.0003)
Desired_Speed = 210

# Set initial position to fully open
initial_position = 512

def set_servo_position(position):
    position = max(DXL_MINIMUM_POSITION_VALUE, min(DXL_MAXIMUM_POSITION_VALUE, int(position)))
    packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_POSITION, position)

def get_servo_position():
    position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result == COMM_SUCCESS and dxl_error == 0:
        return position
    else:
        return None

# Move servo to the initial position
set_servo_position(initial_position)

# Set up serial communication
ser = serial.Serial('COM6', 19200, timeout=0.1) # Reduced timeout for faster reading

# Set up the plot style
style.use('fivethirtyeight')

# Define common figure properties
figsize = (12, 8)
title_fontsize = 20  # Increased title font size by 4
axis_fontsize = 16   # Increased axis font size by 2
fontsize = 14        # Increased regular font size by 2

# Create figure and set up GridSpec layout with custom sizes
fig = plt.figure(figsize=figsize)
gs = GridSpec(2, 2, figure=fig, width_ratios=[1, 1], height_ratios=[1, 1])

# Create subplots
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])

# Data lists
time_data = []
rpm_data = []
pressure_data = []
flow_data = []
servo_position_data = []

start_time = time.time()
rpm_nonzero_start_time = None
avg_rpm_error = float('inf')

def animate(i, time_data, rpm_data, pressure_data, flow_data, servo_position_data):
    global rpm_nonzero_start_time, avg_rpm_error
    current_time = time.time() - start_time  # Current time in seconds since start
    if current_time >= 60:  # Stop after 60 seconds
        plt.close('all')
        return

    while ser.in_waiting > 0:
        line = ser.readline().rstrip()
        try:
            line = line.decode('utf-8', errors='ignore')  # Ignore invalid bytes
            data = json.loads(line)
            pressure_bar = data['pressure_bar']
            ir_pulse_count = data['ir_pulse_count']
            flow_rate = data['flow_rate']

            rpm = (ir_pulse_count * 60) / 3  # *60 to convert to minutes, /3 to account for rotor pieces

            if rpm > 0 and rpm_nonzero_start_time is None:
                rpm_nonzero_start_time = current_time

            # PID control
            pid_output = pid.compute(Desired_Speed, rpm)
            servo_position = 200 + ((512 - 200) * pid_output / Desired_Speed)
            set_servo_position(servo_position)

            # Get the current servo position
            current_servo_position = get_servo_position()
            if current_servo_position is not None:
                servo_position_data.append(current_servo_position)

            # Append data to lists
            time_data.append(current_time)
            rpm_data.append(rpm)
            pressure_data.append(pressure_bar)
            flow_data.append(flow_rate)

            # Calculate how close the desired RPM is to the measured RPM over the past 20 seconds
            if rpm_nonzero_start_time is not None:
                relevant_rpm_data = [r for t, r in zip(time_data, rpm_data) if t >= rpm_nonzero_start_time]
                if relevant_rpm_data:
                    avg_rpm_error = sum(abs(Desired_Speed - r) for r in relevant_rpm_data) / len(relevant_rpm_data)

        except json.JSONDecodeError:
            print("JSON Decode Error")
        except KeyError as e:
            print(f"KeyError: {e}")

    # Clear subplots
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Set font size for all subplots
    ax1.tick_params(axis='both', which='major', labelsize=fontsize)
    ax2.tick_params(axis='both', which='major', labelsize=fontsize)
    ax3.tick_params(axis='both', which='major', labelsize=fontsize)

    # Set face color of the plots to white
    fig.patch.set_facecolor('white')
    ax1.set_facecolor('white')
    ax2.set_facecolor('white')
    ax3.set_facecolor('white')

    # Outline the axes with a thin black line
    for ax in [ax1, ax2, ax3]:
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(0.5)

    # Check if lists are not empty before plotting
    if time_data and rpm_data:
        ax1.plot(time_data, rpm_data, label='RPM')
        ax1.axhline(y=Desired_Speed, color='r', linestyle='--', label='Desired Speed (RPM)')
        ax1.set_ylim(0, max(Desired_Speed + 10, max(rpm_data) + 10))
        ax1.set_xlim(0, current_time)
        ax1.set_title(f'RPM (Avg Error: {avg_rpm_error:.2f})', fontsize=title_fontsize)
        ax1.set_xlabel('Time (s)', fontsize=axis_fontsize)
        ax1.set_ylabel('RPM', fontsize=axis_fontsize)
        ax1.legend(loc='upper right', fontsize=fontsize)

    if time_data and pressure_data:
        ax2.plot(time_data, pressure_data, label='Pressure (Bar)')
        ax2.set_ylim(0, max(pressure_data) + 1)
        ax2.set_xlim(0, current_time)
        ax2.set_title('Pressure', fontsize=title_fontsize)
        ax2.set_xlabel('Time (s)', fontsize=axis_fontsize)
        ax2.set_ylabel('Pressure (Bar)', fontsize=axis_fontsize)
        ax2.legend(loc='upper right', fontsize=fontsize)

    if time_data and flow_data:
        ax3.plot(time_data, flow_data, label='Flow Rate (L/m)')
        ax3.set_ylim(0, max(flow_data) + 1)  # Set lower limit to 0
        ax3.set_xlim(0, current_time)
        ax3.set_title('Flow Rate', fontsize=title_fontsize)
        ax3.set_xlabel('Time (s)', fontsize=axis_fontsize)
        ax3.set_ylabel('Flow Rate', fontsize=axis_fontsize)
        ax3.legend(loc='upper right', fontsize=fontsize)

# Create a separate figure for the servo position with the same height as the RPM plot
fig_servo = plt.figure(figsize=figsize)
ax_servo = fig_servo.add_subplot(1, 1, 1)

def animate_servo(i, time_data, servo_position_data):
    current_time = time.time() - start_time  # Current time in seconds since start
    if current_time >= 60:  # Stop after 60 seconds
        plt.close('all')
        return
    
    if time_data and servo_position_data:
        ax_servo.clear()
        ax_servo.plot(time_data, servo_position_data, label='Servo Position')
        ax_servo.set_ylim(200, 512)
        ax_servo.set_xlim(0, time_data[-1])
        ax_servo.set_title('Servo Motor Position', fontsize=title_fontsize)
        ax_servo.set_xlabel('Time (s)', fontsize=axis_fontsize)
        ax_servo.set_ylabel('Position', fontsize=axis_fontsize)
        ax_servo.legend(loc='upper right', fontsize=fontsize)

    # Set the face color of the plot to white
    ax_servo.set_facecolor('white')

    # Outline the axes with a thin black line
    for spine in ax_servo.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(0.5)

# Set up the animation
ani = animation.FuncAnimation(fig, animate, fargs=(time_data, rpm_data, pressure_data, flow_data, servo_position_data), interval=100, save_count=600)
ani_servo = animation.FuncAnimation(fig_servo, animate_servo, fargs=(time_data, servo_position_data), interval=100, save_count=600)

# Save to PDF after 60 seconds
def save_to_pdf():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'experiment_data.pdf')
    avg_error_40_60 = calculate_avg_error(40, 60)
    with PdfPages(desktop_path) as pdf:
        # Save the main figure
        fig.patch.set_alpha(0)  # Make background transparent
        pdf.savefig(fig)
        # Save the servo position figure
        fig_servo.patch.set_alpha(0)  # Make background transparent
        pdf.savefig(fig_servo)
        # Save data as a text page in the PDF
        plt.figure(figsize=figsize)
        plt.text(0.1, 0.9, 'Experiment Data', fontsize=fontsize)
        plt.text(0.1, 0.85, f'Time Data: {time_data}', fontsize=fontsize)
        plt.text(0.1, 0.80, f'RPM Data: {rpm_data}', fontsize=fontsize)
        plt.text(0.1, 0.75, f'Pressure Data: {pressure_data}', fontsize=fontsize)
        plt.text(0.1, 0.70, f'Flow Data: {flow_data}', fontsize=fontsize)
        plt.text(0.1, 0.65, f'Servo Position Data: {servo_position_data}', fontsize=fontsize)
        plt.text(0.1, 0.60, f'Avg Error (40-60s): {avg_error_40_60:.2f}', fontsize=fontsize)
        plt.axis('off')
        pdf.savefig()
        plt.close()

def calculate_avg_error(start_time, end_time):
    if rpm_nonzero_start_time is None or start_time < rpm_nonzero_start_time:
        start_time = rpm_nonzero_start_time or start_time

    relevant_rpm_data = [rpm for t, rpm in zip(time_data, rpm_data) if start_time <= t <= end_time and t >= rpm_nonzero_start_time]
    if relevant_rpm_data:
        return sum(abs(Desired_Speed - rpm) for rpm in relevant_rpm_data) / len(relevant_rpm_data)
    else:
        return float('inf')

# Save data to Excel
def save_to_excel():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'DATACAE.xlsx')
    data = {
        'Time (s)': time_data,
        'RPM': rpm_data,
        'Pressure (Bar)': pressure_data,
        'Flow Rate (L/m)': flow_data,
        'Servo Position': servo_position_data
    }
    df = pd.DataFrame(data)
    df.to_excel(desktop_path, index=False)

# Define cleanup function before calling it
def cleanup():
    global portHandler, packetHandler
    try:
        if portHandler:
            packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    except Exception as e:
        print(f"Cleanup error: {e}")
    finally:
        if portHandler:
            portHandler.closePort()

import atexit
atexit.register(cleanup)

# Run animation for 60 seconds
try:
    plt.tight_layout(pad=3.0, h_pad=3.0)
    plt.show()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    save_to_pdf()
    save_to_excel()
    cleanup()
