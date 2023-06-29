# WsnRoutPwr.py
# ***********************************************
# *       A new WSN Routing Algorithm           *
# *                  by                         *
# *	         Himanshu Mazumdar                  *
# *	       Date:- 28-May-2023                   *
# *	    Update Date:- 17-June-2023              *
# ***********************************************
# **************************************************************
from platform import node
import tkinter as tkR
from tkinter import colorchooser
from tkinter import simpledialog

# from tkinter import ttk
import tkinter.simpledialog as simpledialog
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import keyboard
import random
import os
import time
import threading
from random import randint
import math

# **************************************************************
# Set the initial line thickness and color
node = []  #  [ndx][sno,x,y,pow,pktno]
tx_delay = []  # transmit delay in mSec
packet = []  # [pktno,srcno,dstno,fromno,hopno,type]; type=>0:adm,1:msg,2:ack
packetold = []  # [pktno,srcno,dstno,fromno,hopno,type]
mynodes = []  # [ndx][n1,n2,n3,..,nn]; all nearest nodes n1,n2 in range txrange
screen_width = 0
screen_height = 0
distmax = 0
txrange = 100
srcno = 0
dstno = 0
pkthopno = 0
fromno = 0
line_thickness = 1
line_color = "black"
nodemx = "100"
rout_speed = 0.0100
auto = False
loop = 0
gridX, gridY = 4, 3
ofsX, ofsY = 22, 110
avghops = 4
cirobj = None


# **************************************************************
def event_handler():
    global tx_delay, srcno, dstno, fromno, packet, type, loop
    timer = threading.Timer(rout_speed, event_handler)
    rout_source_destination()
    time.sleep(max(rout_speed * 10, 0.5))
    # time.sleep(3)
    if auto == False:
        re_draw_nodes()
        return
    loop = loop + 1
    if loop == 1:  # was 10
        loop = 0
        draw_rand_src_dst_line()
        draw_weak_battery_nodes()
    timer.start()  # setup next Timer re-entry after 1.000 sec


# **************************************************************
def rout_source_destination():
    global node, srcno, dstno, type
    if len(node) == 0:
        return
    fromno = srcno
    # col = ("red", "green")
    type = 0  # message packet
    while True:
        r = new_packet(fromno, type)
        if r == False:
            fromno = dstno
            break
        for i in range(len(tx_delay)):
            # time.sleep(rout_speed)
            ndno = tx_delay[i]  # list of relay node in order
            if is_pkt_relayed() == False:  # check this packet status
                draw_this_node(
                    canvasR, ndno, "white", 4, "white"
                )  # disable other node black
                draw_this_node(
                    canvasR, ndno, "blue", 2, "white"
                )  # disable other node black
                # draw_this_node(canvasR, ndno, "black", 4, "white")  # disable other node black
            else:
                r = relay_packet(ndno)  # relay the packet
                if r == False:
                    fromno = dstno
                    auto = False
                    break
                draw_this_node(canvasR, ndno, "red", 4, "white")  # mark this node red
                if node[ndno][3] < 50:  # power low
                    a = 123
                time.sleep(rout_speed)
                draw_src_dst_line(fromno, ndno)  # draw a red transmit path
                fromno = ndno
                if fromno != srcno:
                    if fromno != dstno:
                        node[fromno][3] = node[fromno][3] - randint(8, 10)
        if fromno == dstno:
            tmp = srcno
            srcno = dstno
            dstno = tmp
            type = 1 - type
            if type == 0:
                if cirobj != None:
                    cirobj.remove_circle()
                break
    a = 123


# **************************************************************
def is_pkt_relayed():
    global packet, packetold
    if len(packet) == 0:
        return
    if packet[0] != packetold[0]:  # pkt no
        return False
    else:
        if packet[1] != packetold[1]:  # pkt src
            return False
        else:
            if packet[2] != packetold[2]:  # pkt dst
                return False
            else:
                if packet[4] != packetold[4]:  # pkt hop count
                    return False
                else:
                    return True
    return True
    a = 123


# **************************************************************
def relay_packet(fromno):
    global packet, pkthopno, auto
    if len(packet) == 0:
        return
    packet[3] = fromno
    packet[4] = packet[4] + 1  # hopno
    pkthopno = pkthopno + 1
    if pkthopno > 20:
        return False
    return True


# **************************************************************
def new_packet(frmno, type):
    global srcno, dstno, node, packet, packetold, pkthopno, fromno, auto
    fromno = frmno
    if srcno == fromno:
        node[srcno][4] = node[srcno][4] + 1
        pkthopno = 0
    packet = []
    packet.append(node[srcno][4])
    packet.append(srcno)
    packet.append(dstno)
    packet.append(fromno)
    packet.append(pkthopno)
    packet.append(type)
    packetold = []
    packetold.append(packet[0])
    packetold.append(packet[1])
    packetold.append(packet[2])
    packetold.append(packet[3])
    packetold.append(packet[4])
    packetold.append(packet[5])
    # print("New Pkt:", packet)
    # draw_this_node(canvasR, fromno, "red", 2, "white")
    r = map_all_signal_strength(fromno, dstno)
    if r == False:
        auto = False
        return False
    return True


# **************************************************************
def send_message():
    global packet, srcno, type
    rout_source_destination()
    a = 123


# **************************************************************
def auto_messaging_start():
    global auto
    auto = True
    event_handler()


# **************************************************************
def auto_messaging_exit():
    global auto
    auto = False


# **************************************************************
def battery_full():
    for i in range(len(node)):
        node[i][3] = 100
    re_draw_nodes()


# **************************************************************
def map_all_signal_strength(src, dst):
    global tx_delay, node, txrange, cirobj
    tx_queue = []
    for i in range(len(node)):
        col = []
        if i != src:
            ds = distance_n1_n2(src, i)
            if ds <= txrange:  # Range constrain
                if node[i][3] >= 50:  # Power constrain
                    # dly = int(100 * (1.0 - ds / txrange))
                    dd = distance_n1_n2(dst, i)
                    col.append(dd)
                    col.append(ds)
                    col.append(i)
                    tx_queue.append(col)
    tx_queue.sort()
    tx_delay = []
    if len(tx_queue) == 0:
        return False
    xc, yc = node[fromno][1], node[fromno][2]  # center of circle of rad txrange
    if cirobj != None:
        cirobj.remove_circle()
    cirobj = Circle(canvasR, "red", xc, yc, txrange)
    cirobj.draw_circle()

    # canvasR.create_oval(
    #     xc - txrange, yc - txrange, xc + txrange, yc + txrange, width=1, outline="red"
    # )

    for i in range(len(tx_queue)):
        draw_this_node(canvasR, tx_queue[i][2], "green", 4, "white")
        tx_delay.append(tx_queue[i][2])
        # if i >= 40:
        #     packetold = []
        #     packetold.append(packet[0])
        #     packetold.append(packet[1])
        #     packetold.append(packet[2])
        #     packetold.append(packet[3])
        #     packetold.append(packet[4])
        #     packetold.append(packet[5])
        #     break
    return True


# **************************************************************
def perform_option2():
    print("Option 2 selected.")
    # Perform the desired actions for Option 2


# **************************************************************
def perform_suboption1():
    print("Sub-option 1 selected.")
    # Perform the desired actions for Sub-option 1


# **************************************************************
def perform_suboption2():
    print("Sub-option 2 selected.")
    # Perform the desired actions for Sub-option 2


# Function to open the popup window ****************************
def open_popup_max_nodes():
    global nodemx
    default_text = str(nodemx)
    text = simpledialog.askstring(
        "Enter Text", "Enter Max Nodes:", initialvalue=default_text
    )
    if text:
        nodemx = int(text)
        # messagebox.showinfo("Text Entered", f"You entered: {text}")


# Function to open the popup window **************************
def open_popup_average_hops():
    global avghops
    if avghops > 7:
        avghops = 7
    if avghops < 2:
        avghops = 2
    default_text = str(avghops)
    text = simpledialog.askstring(
        "Enter Text", "Enter Average Hops:", initialvalue=default_text
    )
    if text:
        avghops = int(text)


# Populate node[] with (sno,x,y,pow,grp **********************
def GetRandomNodes(nods, gapx, wdt, gapy, hgt):
    global node, txrange
    arr1 = []
    for i in range(nods):
        col1 = []
        point = [
            random.randrange(gapx, wdt),
            random.randrange(gapy, hgt),
        ]
        col1.append(point[0])  # x
        col1.append(point[1])  # y
        col1.append(i)  # sno
        col1.append(100)  # pow
        col1.append(0)  # pktno
        arr1.append(col1)
    arr1.sort()
    node = []  #  [ndx][sno,x,y,pow,pktno]
    for i in range(nods):
        node.append([i, arr1[i][0], arr1[i][1], arr1[i][3], arr1[i][4]])
    brk = 123


# Draw Grid ***************************************************
def draw_grid(canvas):
    global nodemx, screen_width, screen_height, gridX, gridY, ofsX, ofsY
    gapx = (screen_width - ofsX) / gridX
    gapy = (screen_height - ofsY) / gridY
    for x in range(gridX + 1):
        xl = x * gapx
        canvas.create_line(
            xl, 0, xl, screen_height - 1, width=1, fill="#CCCCCC"
        )  # draw line
    for y in range(gridY + 1):
        yl = y * gapy
        canvas.create_line(
            0, yl, screen_width - 1, yl, width=1, fill="#CCCCCC"
        )  # draw line


# Draw node[] with sno ****************************************
def draw_nodes():
    global nodemx, screen_width, screen_height, distmax, txrange, distmax, avghops
    mxnodes = int(nodemx)
    nods = mxnodes
    GetRandomNodes(nods, 10, screen_width - 30, 10, screen_height - 120)
    canvasR.delete("all")
    draw_grid(canvasR)
    for i in range(len(node)):
        draw_this_node(canvasR, i, "blue", 2, "white")
    canvasR.pack()
    distmax = math.sqrt(screen_width * screen_width + screen_height * screen_height)
    txrange = distmax / avghops
    a = 123


# Re-Draw Nodes ***********************************************
def re_draw_nodes():
    global nodemx, canvasR, canvas1, canvas2, txrange
    mxnodes = int(nodemx)
    canvas2.delete("all")
    canvasR.pack_forget()
    nods = mxnodes
    draw_grid(canvas2)
    for i in range(len(node)):
        draw_this_node(canvas2, i, "blue", 2, "white")
    # canvasR.delete("all")
    canvasR = canvas2
    canvasR.pack()
    txrange = distmax / avghops
    a = 123


# Draw One Node node[ndx] of width wdt ************************
def draw_this_node(canvas, ndx, col, wdt, bcol):
    global node
    r = True
    if node[ndx][3] < 50:  # if battery low
        bcol = "#00FFFF"  # change back col of node
        r = False
    canvas.create_oval(
        node[ndx][1],
        node[ndx][2],
        node[ndx][1] + 20,
        node[ndx][2] + 20,
        fill=bcol,
        width=wdt,
        outline=col,
    )
    canvas.create_text(
        node[ndx][1] + 10,
        node[ndx][2] + 10,
        text=str(node[ndx][0]),
        fill="red",
        font=("Helvetica 10 bold"),
    )
    return r


# Draw Line between 2 random node *****************************
def draw_rand_src_dst_line():
    global nodemx, srcno, dstno, packet
    if len(node) == 0:
        return
    pkthopno = 0
    re_draw_nodes()
    mxnodes = int(nodemx)
    mxn2 = int(mxnodes / 2)
    dn = 0
    for i in range(5):
        srcno2 = random.randint(0, mxn2) - 1  # Random src
        dstno2 = random.randint(mxn2, mxnodes - 1)  # Random dst
        d = distance_n1_n2(srcno2, dstno2)
        if dn < d:
            dn = d
            srcno = srcno2
            dstno = dstno2
    x1 = node[srcno][1] + 10
    y1 = node[srcno][2] + 10
    x2 = node[dstno][1] + 10
    y2 = node[dstno][2] + 10
    col = "blue"
    canvasR.create_line(x1, y1, x2, y2, width=2, fill=col)  # draw line
    packet = []
    a = 123


# Draw Line between src and dst *******************************
def draw_src_dst_line(src, dst):
    global nodemx, srcno, dstno, type
    x1 = node[src][1] + 10
    y1 = node[src][2] + 10
    x2 = node[dst][1] + 10
    y2 = node[dst][2] + 10
    col = "red"
    if type == 1:
        col = "green"
    canvasR.create_line(x1, y1, x2, y2, width=2, fill=col)  # draw line
    a = 123


# Line thickness menu event handler ***************************
def change_rout_speed(speed):
    global rout_speed
    rout_speed = speed
    a = 123


# Line thickness menu event handler ***************************
def change_line_thickness(new_thickness):
    global line_thickness
    line_thickness = new_thickness


# Line color menu event handler *******************************
def change_line_color():
    global line_color
    color = colorchooser.askcolor(title="Select Line Color")
    if color[1] is not None:
        line_color = color[1]


# get distance between n1,n2 ***********************************
def distance_n1_n2(n1, n2):
    d1x = node[n1][1]
    d1y = node[n1][2]
    d2x = node[n2][1]
    d2y = node[n2][2]
    dst2 = math.sqrt((d1x - d2x) * (d1x - d2x) + (d1y - d2y) * (d1y - d2y))
    dst2 = round(dst2, 2)
    return dst2
    a = 123


# Populate Distance Matrix in node [] ************************
def init_pktno(nodmx):
    global pktno
    pktno = []
    for n1 in range(nodmx):
        pktno.append(0)
    a = 123


# Populate Distance Matrix in node [] ************************
def draw_weak_battery_nodes():
    global node
    for n1 in range(len(node)):
        if node[n1][3] < 50:
            draw_this_node(canvasR, n1, "blue", 2, "#00FFFF")
    a = 123


# **************************************************************
# Mouse event handlers
def on_mouse_press3(event):
    global mouse_position
    x, y = event.x, event.y
    mouse_position = (x, y)


# Mouse event handlers ****************************************
def on_mouse_press(event):
    global drawing
    drawing = True


# **************************************************************
def on_mouse_release(event):
    global drawing
    drawing = False


# **************************************************************
def on_mouse_move(event):
    if drawing:
        global mouse_position
        x, y = event.x, event.y
        canvasR.create_line(
            mouse_position[0],
            mouse_position[1],
            x,
            y,
            width=line_thickness,
            fill=line_color,
        )
        mouse_position = (x, y)


# **************************************************************
def search_in_lines():
    global node, srcno, dstno, mynodes
    populate_mynodes()
    buf1 = []
    for i in range(len(mynodes)):
        buf2 = []
        for j in range(len(mynodes)):
            if i != j:
                r = no_common_nodes(i, j)
                if r == True:
                    buf2.append(j)
        buf1.append(buf2)
    a = 123


# **************************************************************
def no_common_nodes(n1, n2):
    global mynodes
    for i in range(len(mynodes[n1])):
        n3 = mynodes[n1][i]
        for j in range(len(mynodes[n2])):
            n4 = mynodes[n2][j]
            if n3 == n4:
                return False
    return True
    a = 123


# Populate my nearest mynodes **********************************
def populate_mynodes():
    global node, srcno, dstno, mynodes, txrange
    mynodes = []
    for i in range(len(node)):
        buf1 = []
        for j in range(len(node)):
            if i != j:
                buf2 = []
                d = distance_n1_n2(i, j)
                buf2.append(d)
                buf2.append(j)
                buf1.append(buf2)
        buf1.sort()
        mynds = []
        for k in range(len(buf1)):
            if buf1[k][0] <= txrange:
                mynds.append(buf1[k][1])
        mynodes.append(mynds)
    a = 123


# **************************************************************
def on_resize(event):
    # Get the new size of the form
    global canvasR, screen_width, screen_height
    canvasR.config(width=event.width - 4, height=event.height - 4)
    screen_width, screen_height = event.width, event.height


# **************************************************************
def open_file():
    global node, nodexy, txrange
    flnm = filedialog.askopenfilename(
        initialdir="", filetypes=(("data files", "*.txt"), ("all files", "*.*"))
    )
    file1 = open(flnm, "r")
    wrd = file1.readline().removesuffix("\n").split(",")
    flnm = wrd[0]
    sz = int(wrd[1])
    node = []
    nodexy = []
    for i in range(sz):
        wrd = file1.readline().removesuffix("\n").split(",")
        row = []
        row.append(int(wrd[0]))  # sno
        row.append(int(wrd[1]))  # x
        row.append(int(wrd[2]))  # y
        row.append(int(wrd[3]))  # pow
        row.append(int(wrd[4]))  # state
        node.append(row)
        dt = [int(wrd[0]), 0.0, 0.0, 0]  # [sno, x, y, flg]
        nodexy.append(dt)
    file1.close()
    distmax = math.sqrt(screen_width * screen_width + screen_height * screen_height)
    txrange = distmax / avghops
    populate_mynodes()
    re_draw_nodes()


# **************************************************************
def save_file():
    a = 123


# **************************************************************
def main_menuR():
    global windowR, canvasR, canvas1, canvas2, screen_width, screen_height

    # windowR = tk.Tk()
    windowR.title("WSN Auto Routing-HSM")
    # Configure the resize event handler
    windowR.bind("<Configure>", on_resize)
    # Create a Canvas widget
    # screen_width = windowR.winfo_screenwidth()
    # screen_height = windowR.winfo_screenheight()
    screen_width, screen_height = 800, 600
    ofsX, ofsY = 0, 0
    canvas1 = tkR.Canvas(windowR, width=screen_width, height=screen_height)
    canvas2 = tkR.Canvas(windowR, width=screen_width, height=screen_height)
    canvasR = canvas2
    canvasR.pack()

    # Maximize the windowR
    # windowR.state("zoomed")

    # Create a menu bar
    menubar = tkR.Menu(windowR)
    windowR.config(menu=menubar)

    # Create the file menu
    file_menu = tkR.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    # Create the tool menu
    tool_menu = tkR.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Tool", menu=tool_menu)

    # Add options to the file menu
    file_menu.add_command(label="Max Nodes ", command=lambda: open_popup_max_nodes())
    file_menu.add_command(label="Avg Hops ", command=lambda: open_popup_average_hops())
    file_menu.add_command(label="Draw Nodes (cnt+d)", command=lambda: draw_nodes())
    file_menu.add_command(label="ReDraw Nodes (cnt+r)", command=lambda: re_draw_nodes())
    file_menu.add_command(
        label="Rand Src-Dst (cnt+l)", command=lambda: draw_rand_src_dst_line()
    )
    file_menu.add_command(label="Send Pkt  (cnt+s)", command=lambda: send_message())
    file_menu.add_command(
        label="Auto Pkt ON (cnt+a)", command=lambda: auto_messaging_start()
    )
    file_menu.add_command(
        label="Auto Pkt OFF (cnt+e)", command=lambda: auto_messaging_exit()
    )
    file_menu.add_command(label="Battery Full (cnt+b)", command=lambda: battery_full())
    file_menu.add_separator()
    file_menu.add_command(label="Open", command=lambda: open_file())
    file_menu.add_command(label="Save", command=lambda: save_file())
    file_menu.add_separator()
    file_menu.add_command(label="Exit (cnt+x)", command=windowR.quit)

    # Create the sub-menu
    rout_speed = tkR.Menu(tool_menu, tearoff=0)
    linethickness = tkR.Menu(tool_menu, tearoff=0)
    linecolour = tkR.Menu(tool_menu, tearoff=0)
    tool_menu.add_cascade(label="Rout Speed", menu=rout_speed)
    tool_menu.add_cascade(label="Line Thickness", menu=linethickness)
    tool_menu.add_cascade(label="Line Colour", menu=linecolour)

    # Add options to the sub-menu
    rout_speed.add_command(label="fast", command=lambda: change_rout_speed(0))
    rout_speed.add_command(label="medium", command=lambda: change_rout_speed(1.0))
    rout_speed.add_command(label="slow", command=lambda: change_rout_speed(10.0))
    linethickness.add_command(label="Thin", command=lambda: change_line_thickness(1))
    linethickness.add_command(label="Medium", command=lambda: change_line_thickness(3))
    linethickness.add_command(label="Thick", command=lambda: change_line_thickness(5))

    linecolour.add_command(label="Select Color", command=change_line_color)

    # register the hotkey using the keyboard library
    keyboard.add_hotkey("ctrl+d", draw_nodes)
    keyboard.add_hotkey("ctrl+r", re_draw_nodes)
    keyboard.add_hotkey("ctrl+l", draw_rand_src_dst_line)
    keyboard.add_hotkey("ctrl+s", send_message)
    keyboard.add_hotkey("ctrl+a", auto_messaging_start)
    keyboard.add_hotkey("ctrl+b", battery_full)
    keyboard.add_hotkey("ctrl+e", auto_messaging_exit)
    keyboard.add_hotkey("ctrl+x", windowR.quit)

    # Bind the mouse event handlers to the canvasR
    canvasR.bind("<ButtonPress-3>", on_mouse_press3)
    canvasR.bind("<ButtonPress-1>", on_mouse_press)
    canvasR.bind("<ButtonRelease-1>", on_mouse_release)
    canvasR.bind("<B1-Motion>", on_mouse_move)

    # Run the main loop
    windowR.mainloop()


# **************************************************************
class Circle:
    def __init__(self, canvas, color, xc, yc, sz):
        self.canvas = canvas
        self.color = color
        self.shape_id = None
        self.xc = xc
        self.yc = yc
        self.sz = sz

    def draw_circle(self):
        x1, y1 = self.xc - self.sz, self.yc - self.sz
        x2, y2 = self.xc + self.sz, self.yc + self.sz
        self.shape_id = self.canvas.create_oval(x1, y1, x2, y2, outline=self.color)

    def remove_circle(self):
        self.canvas.delete(self.shape_id)


# **************************************************************
# Start the program
windowR = tkR.Tk()
print(os.path.dirname(__file__))
main_menuR()
# **************************************************************
