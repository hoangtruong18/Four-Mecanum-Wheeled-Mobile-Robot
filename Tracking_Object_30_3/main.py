from tkinter import *
from tkinter.ttk import *
import tkinter.font as font
import PIL.ImageTk
import PIL.Image
import tkinter
from mylib import *
import threading
from tkinter import messagebox


cam_index = 1


'''Functions Sector---------------------------------------------------------------------------------'''


def update():
    global webcam, img, state_control

    mode = operating_option.get()
    notification.delete(1.0, END)
    position.delete(1.0, END)
    angle.delete(1.0, END)
    trajectory = trajectory_type.get()

    ret, frame = cap.read()
    frame, state_vector = handle(frame)

    if state_control:
        if trajectory == "Rectangle":
            x, y, h, w, cmd = control(trajectory, state_vector, mode, cmd_old)
            cv2.rectangle(frame, (x, y), (x+h, y+w), (0, 255, 0), 2)
            cv2.putText(frame, "Rectangle Trajectory", (x+30, y+30), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0))

            notification.insert(END, cmd)
            if len(state_vector) != 0:
                position.insert(END, str(state_vector[1]))
                angle.insert(END, str(state_vector[0]))

        if trajectory == "Circle":
            c, r, des_point, cmd = control(trajectory, state_vector, mode, cmd_old)
            cv2.circle(frame, c, r, (0, 255, 0), 2)

            if len(state_vector) != 0:
                cv2.arrowedLine(frame, state_vector[1], des_point, (255, 0, 0), 2)
            cv2.putText(frame, "Circle Trajectory", (c[0]-100, c[1]), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0))

            notification.insert(END, cmd)
            if len(state_vector) != 0:
                position.insert(END, str(state_vector[1]))
                angle.insert(END, str(state_vector[0]))

    img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    webcam.create_image(0, 0, image=img, anchor=tkinter.NW)
    webcam.after(20, update)


def start():
    global state_control
    state_control = True
    trajectory = trajectory_type.get()

    if trajectory == "Rectangle":
        print("Choose Rectangle Trajectory - State: " + str(state_control))
    elif trajectory == "Circle":
        print("Choose Circle Trajectory - State: " + str(state_control))
    else:
        messagebox.showerror("Error", "You have not chosen trajectory")


def stop():
    global state_control
    send = threading.Thread(target=sendrequest, args=(root_url+"/0/off", ))
    send.start()
    state_control = False
    print("Stop controlling - State: " + str(state_control))


def go_straight():
    mode = operating_option.get()
    if mode == "Manual":
        print("Go straight")


def turn_left():
    mode = operating_option.get()
    if mode == "Manual":
        print("Turn left")


def turn_right():
    mode = operating_option.get()
    if mode == "Manual":
        print("Turn right")


'''App window sector---------------------------------------------------------------------------------'''


window = Tk()
window.title("Mecanum Control Panel")
window.geometry("1130x540")
window.resizable(width=False, height=False)
window.iconbitmap('favicon.ico')

cap = cv2.VideoCapture(cam_index)
webcam_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
webcam_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

label_webcam = Label(window, text="Your Camera", font=("Barlow", 13))
label_webcam.place(x=webcam_w/2-30, y=20+webcam_h)

webcam = Canvas(window, width=webcam_w, height=webcam_h)
webcam.place(x=20, y=20)

operating_system = Canvas(window, width=427, height=250, bg="#DDDDDD")
operating_system.place(x=680, y=20)

'''------------------------------------------------------------------------------------'''
operating_option = Combobox(window, font=('Barlow', 11), width=6, state='readonly')
operating_option['values'] = ("Auto", "Manual")
operating_option.current(0)
operating_option.place(x=755, y=90)

trajectory_type = Combobox(window, font=('Barlow', 11), width=15, state='readonly')
trajectory_type['values'] = ("Rectangle", "Circle")
trajectory_type.current(0)
trajectory_type.place(x=945, y=90)

label1 = Label(window, text="Operating System", font=("Barlow", 15, "bold"), foreground="#8C1A35", background="#DDDDDD")
label1.place(x=807, y=35)

label2 = Label(window, text="Mode:", font=("Barlow", 13, "bold"), foreground="black", background="#DDDDDD")
label2.place(x=700, y=90)

label3 = Label(window, text="Trajectory:", font=("Barlow", 13, "bold"), foreground="black", background="#DDDDDD")
label3.place(x=850, y=90)

'''-------------------------------------------------------------------------------------------------------------'''
bf = font.Font(family="Barlow", size=12, weight="bold")
start_button = tkinter.Button(window, text="Run", font=bf, command=start, width=8, bg='#2E6BC5', fg="white")
start_button.place(x=710, y=155)

stop_button = tkinter.Button(window, text="Stop", font=bf, command=stop, width=8, bg='#2E6BC5', fg="white")
stop_button.place(x=710, y=205)

'''---------------------------------------------------------------------------------------------------------'''
up_img = PhotoImage(file="Icon/up.gif")
up_bt = tkinter.Button(window, image=up_img, bd=0, bg="#FF99FF", command=go_straight)
up_bt.place(x=870, y=300)

right_img = PhotoImage(file="Icon/right.gif")
up_bt = tkinter.Button(window, image=right_img, bd=0, bg="#FF99FF", command=turn_right)
up_bt.place(x=940, y=370)

down_img = PhotoImage(file="Icon/down.gif")
up_bt = tkinter.Button(window, image=down_img, bd=0, bg="#FF99FF")
up_bt.place(x=870, y=440)

left_img = PhotoImage(file="Icon/left.gif")
up_bt = tkinter.Button(window, image=left_img, bd=0, bg="#FF99FF", command=turn_left)
up_bt.place(x=800, y=370)

'''--------------------------------------------------------------------------------------------------'''
label_notice = Label(window, text="Control Command:", font=("Barlow", 13), background="#DDDDDD")
label_notice.place(x=830, y=150)

label_state1 = Label(window, text="Position [Descartes]:", font=("Barlow", 13), background="#DDDDDD")
label_state1.place(x=830, y=185)

label_state2 = Label(window, text="Located Angle [°]:", font=("Barlow", 13), background="#DDDDDD")
label_state2.place(x=830, y=220)

notification = Text(window, width=10, height=1, font=("Barlow", 13), fg="#003300", bg="#E9F0FD")
notification.place(x=990, y=150)

position = Text(window, width=10, height=1, font=("Barlow", 13), fg="#003300", bg="#E9F0FD")
position.place(x=990, y=185)

angle = Text(window, width=10, height=1, font=("Barlow", 13), fg="#003300", bg="#E9F0FD")
angle.place(x=990, y=220)

'''------------------------------------------------------------------------------------------------'''
img = None
state_control = False
cmd_old = None

update()
window.mainloop()
