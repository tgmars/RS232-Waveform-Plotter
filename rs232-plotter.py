import argparse
import matplotlib.pyplot as pyplot

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("parity",help="Set parity bit calculation to even, odd or none.")
parser.add_argument("voltage",help="max/min voltage to plot, eg 15 would plot for +15V to -15V.", type=int)
parser.add_argument("data",help="String of data bits to plot.")
parser.add_argument("numstartbits",help="per sequence, the number of bits to include & mark as start bits.", type=int)
parser.add_argument("numstopbits",help="per sequence, the number of bits to include & mark as stop bits.", type=int)
parser.add_argument("numdatabits",help="per sequence, the number of data bits to include before calculating parity and initiating new sequence.", type=int)
args = parser.parse_args()

# X axis labels
idle = "Idle"
start = "Start"
stop  = "Stop"
data = "D"

# Graph vars
x = [] 
x_label = []
y = []

# Func to graph vars with idle state
def set_idle():
    x.append(x_pos)
    x_label.append(idle)
    y.append(-1)

# Keep our iteration through the graph consistent
def move_x_set_y(y_val):
        global x_pos
        x.append(x_pos)
        y.append(y_val)
        x_pos=x_pos+1

# Returns the input scaled by the voltage value, used for a map.
def scale_by_voltage(val):
    return val*args.voltage

# Initialise and x_pos manual setup.
x_pos = 0
set_idle()
x_pos = 1

# For each sequence of data bits as specified by the users numdatabits
for i in range(0,len(args.data),args.numdatabits):
    next = args.numdatabits + i
    # Keep track of the high bits in this chunk for calculating parity.
    high_bits = 0

    # Assign the data chunk given the user specified numdatabits
    data_chunk = args.data[i:next]

    # Add the required number of start bits to the axis data
    for strt in range(args.numstartbits):
        x_label.append(start + str(strt))
        move_x_set_y(1)

    # Add the required amount of data to the axis data
    for dindex,d in enumerate(data_chunk):
        x_label.append(data + str(dindex))
        if(int(d)==1): move_x_set_y(-1)
        if(int(d)==0): move_x_set_y(1)
        # Keep track of high data bits
        if int(d) == 1:
            high_bits += 1

    # Calculate the parity bit for the inputted option and add to axis data
    if((args.parity == "even") and high_bits%2 == 0): move_x_set_y(1)
    if((args.parity == "odd") and high_bits%2 == 1): move_x_set_y(1)

    # Add the required number of stop bits to the x axis data
    for stp in range(args.numstopbits):
        x_label.append(stop + str(stp))
        move_x_set_y(-1)

set_idle()

# Apply transform for required voltage using the previously defined func.
y = list(map(scale_by_voltage, y))

# Plot waveform
pyplot.step(x,y,where='mid')
pyplot.xlabel('bits')
pyplot.ylabel('voltage')
pyplot.xticks(x,x_label)
pyplot.grid(which='both')
pyplot.title('RS232 plot of data bits ' + args.data)
pyplot.show()
