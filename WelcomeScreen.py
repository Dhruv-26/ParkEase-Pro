import base64
import datetime
import pickle
from tkinter import *
from tkinter import filedialog
import cv2
import cvzone
import numpy as np
import requests
from PIL import ImageTk, Image
from authKey import SECRET_KEY
from dbConnection import mycursor, connection
import multiprocessing
import easyocr

# import matplotlib.pyplot as plt
# import easyocr
# from IPython.display import Image


def process_video():
    # Your video processing code goes here
    cap = cv2.VideoCapture('./images/carPark.mp4')
    width, height = 103, 43
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)

    def empty(a):
        pass

    cv2.namedWindow("Vals")
    cv2.resizeWindow("Vals", 640, 240)
    cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
    cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
    cv2.createTrackbar("Val3", "Vals", 5, 50, empty)

    def checkSpaces():
        spaces = 0
        for pos in posList:
            x, y = pos
            w, h = width, height

            imgCrop = imgThres[y:y + h, x:x + w]
            count = cv2.countNonZero(imgCrop)

            if count < 800:
                color = (0, 200, 0)
                thic = 5
                spaces += 1

            else:
                color = (0, 0, 200)
                thic = 2

            cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)

            cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                        color, 2)

        cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20,
                           colorR=(0, 200, 0))

    while True:
        # Get image frame
        success, img = cap.read()
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

        val1 = cv2.getTrackbarPos("Val1", "Vals")
        val2 = cv2.getTrackbarPos("Val2", "Vals")
        val3 = cv2.getTrackbarPos("Val3", "Vals")
        if val1 % 2 == 0: val1 += 1
        if val3 % 2 == 0: val3 += 1
        imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, val1, val2)
        imgThres = cv2.medianBlur(imgThres, val3)
        kernel = np.ones((3, 3), np.uint8)
        imgThres = cv2.dilate(imgThres, kernel, iterations=1)

        checkSpaces()
        # Display Output

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('r'):
            pass
        if key == ord('q'):
            break

if __name__ == "__main__":
    # Run process_video in a separate process
    video_process = multiprocessing.Process(target=process_video)
    video_process.start()

    # root = Tk()
    # root.title("Welcome Screen")
    # # root.attributes('-fullscreen',True)
    # root.configure(background='#17202A')
    # BG_GRAY = "#ABB2B9"
    # BG_COLOR = "#17202A"
    # TEXT_COLOR = "#EAECEE"
    # BG_WHITE = "#FFF"
    # COLOR_GREEN = "#008000"
    # COLOR_RED = "#FF0000"
    #
    # FONT = "Helvetica 14"
    # FONT_BOLD = "Helvetica 13 bold"
    #
    # root.geometry("1300x800")
    # # set minimum window size value
    # root.minsize(700, 700)
    # # set maximum window size value
    # root.maxsize(1350, 800)

    # Colors and Fonts
    BG_COLOR = "#1E1E1E"
    TEXT_COLOR = "#FFFFFF"
    COLOR_RED = "#FF3B3B"
    COLOR_GREEN = "#4CAF50"
    BUTTON_BG = "#FFD700"
    BUTTON_FG = "#006400"
    FONT_BOLD = ("Helvetica", 16, "bold")

    # Root Window
    root = Tk()
    root.title("Welcome Screen")
    # root.geometry("800x500")
    root.configure(bg=BG_COLOR)
    root.geometry("1300x800")
    # set minimum window size value
    root.minsize(700, 700)
    # set maximum window size value
    root.maxsize(1350, 800)



    global fare_text
    fare_text = "Nothing to Show"


    def show_fare():
        fare_label = Label(root, text=fare_text, bg="grey", font=("Helvetica", 15), fg="white", width=30, height=3,
                           borderwidth=5, relief="solid").place(relx=0.17, rely=0.83)


    def exit_command():
        root.quit()


    def select_from_camera():
        cam = cv2.VideoCapture(0)
        while True:
            _, img = cam.read()
            key = cv2.waitKey(1) & 0xff
            cv2.imshow("Capture License Number", img)
            if (key == ord('q')):
                cv2.destroyAllWindows()
                print("Captured...")
                cv2.imwrite("first1.jpg", img)
                # time.sleep(5)
                IMAGE_PATH1 = "first1.jpg"

                reader = easyocr.Reader(['en'])
                output = reader.readtext('/Users/acer/Documents/GitHub/ParkEasePro/first1.jpg')
                print("OCR:>>>",output)
                print("OUTPUT>>>>>>>>>>>>>>>>>>>", (output[0])[1])

                my_image1 = ImageTk.PhotoImage(Image.open(IMAGE_PATH1))
                my_image_label = Label(root, image=my_image1, width=650, height=300)
                my_image_label.image = my_image1
                my_image_label.place(relx=0.03, rely=0.4)

                with open(IMAGE_PATH1, 'rb') as image_file:
                    img_base64 = base64.b64encode(image_file.read())

                url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (
                    SECRET_KEY)
                r = requests.post(url, data=img_base64)
                data = r.json()
                print(data)
                results = data.get("results", [])
                # if results is None
                first_result = results[0]
                plate_info = first_result.get("plate", "")
                print("plate_info===>" + plate_info)
                print("==========number plate===============")
                print(plate_info)

                getnumber = "SELECT * FROM users WHERE number_plate = '{}'".format(plate_info)
                mycursor.execute(getnumber)
                templist = list(mycursor)
                # print(len(templist))
                # print(templist)
                if len(templist) == 0:
                    temp_time = datetime.datetime.now()
                    entered_time = temp_time.strftime("%Y %m %d %H %M %S")
                    print("entered time ", entered_time)
                    mycursor.execute("INSERT INTO users VALUES ('{}', '{}')".format(plate_info, entered_time))
                    list_of_globals = globals()
                    list_of_globals['fare_text'] = "Vehicle details has been \n entered into the database"
                    show_fare()
                    connection.commit()
                else:
                    for temp in templist:
                        # print(temp)
                        if plate_info == temp[0]:
                            print(temp[1])
                            # result = datetime.datetime.now() - temp[1]
                            current_time = datetime.datetime.now()
                            arrival_time_temp = temp[1].split('.')
                            print("arrival time temp ", arrival_time_temp[0])
                            arrival_time_temp[0] = str(arrival_time_temp[0])
                            arrival_time = datetime.datetime.strptime(arrival_time_temp[0], "%Y %m %d %H %M %S")
                            result = current_time - arrival_time
                            print("result = ", result)
                            days = result.days
                            hours = result.seconds / 3600
                            print("hours : ", hours, "days : ", days)
                            fare = (days * 24 + hours) * 20
                            if hours < 6:
                                fare = 20

                            query = "DELETE FROM users WHERE number_plate = '{}'".format(temp[0])
                            mycursor.execute(query)
                            connection.commit()
                            list_of_globals = globals()
                            list_of_globals['fare_text'] = "Vehicle Number : {} \n Parking Charge : {}".format(temp[0],
                                                                                                               fare)
                            show_fare()
                            print("deleted")
                            print(temp[0], fare)
                break


            elif (key == ord('w')):
                break

        cam.release()
        cv2.destroyAllWindows()
        showBoxes()


    def select_from_file():
        global my_image
        root.filename = filedialog.askopenfilename(
            initialdir="E:/Python machine learning projects/ParkingChargeCalc_ML",
            title="Select A File",
            filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
        print("Root>>>>...",root.filename)
        IMAGE_PATH = root.filename
        my_image = ImageTk.PhotoImage(Image.open(root.filename))
        my_image_label = Label(root, image=my_image, width=650, height=300).place(relx=0.03, rely=0.4)

        # IMAGE_PATH = 'first1.jpg'

        with open(IMAGE_PATH, 'rb') as image_file:
            img_base64 = base64.b64encode(image_file.read())

        url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
        r = requests.post(url, data=img_base64)
        # reader = easyocr.Reader(['en'])
        # output = reader.readtext('/Users/acer/Documents/GitHub/ParkEasePro/first1.jpg')
        # print("OUTPUT>>>>>>>>>>>>>>>>>>>", (output[0])[1])

        data = r.json()
        print(data)
        results = data.get("results", [])
        # if results is None
        first_result = results[0]
        plate_number = first_result.get("plate", "")
        print("plate_info===>" + plate_number)
        print(plate_number)
        getnumber = "SELECT * FROM users WHERE number_plate = '{}'".format(plate_number)
        mycursor.execute(getnumber)
        templist = list(mycursor)
        # print(len(templist))
        # print(templist)
        if len(templist) == 0:
            temp_time = datetime.datetime.now()
            entered_time = temp_time.strftime("%Y %m %d %H %M %S")
            print("entered time ", entered_time)
            mycursor.execute("INSERT INTO users VALUES ('{}', '{}')".format(plate_number, entered_time))
            # mycursor.execute("Delete from users")

            list_of_globals = globals()
            list_of_globals['fare_text'] = "Vehicle details has been\nentered into the database"
            show_fare()
            connection.commit()

        else:
            for temp in templist:
                # print(temp)qqq
                if plate_number == temp[0]:
                    print(temp[1])
                    # result = datetime.datetime.now() - temp[1]
                    current_time = datetime.datetime.now()
                    arrival_time_temp = temp[1].split('.')
                    print("arrival time temp ", arrival_time_temp[0])
                    arrival_time_temp[0] = str(arrival_time_temp[0])
                    arrival_time = datetime.datetime.strptime(arrival_time_temp[0], "%Y %m %d %H %M %S")
                    result = current_time - arrival_time
                    print("result = ", result)
                    days = result.days
                    hours = result.seconds / 3600
                    print("hours : ", hours, "days : ", days)
                    fare = (days * 24 + hours) * 20
                    if hours < 6:
                        fare = 20

                    query = "DELETE FROM users WHERE number_plate = '{}'".format(temp[0])
                    mycursor.execute(query)
                    connection.commit()
                    list_of_globals = globals()
                    list_of_globals['fare_text'] = "Vehicle Number : {} \n Parking Charge : {}".format(temp[0], fare)
                    show_fare()
                    print("deleted")
                    print(temp[0], fare)

        showBoxes()


    # lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, justify=CENTER, padx=10, pady=10,
    #                width=140, height=1).grid(row=0)

    # Welcome Label
    lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=("Helvetica", 20, "bold"))
    lable1.pack(pady=40)

    # parking_slot_lable = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Slot", font=FONT_BOLD).place(relx=0.7, rely=0.1)
    # Slot Label
    parking_slot_label = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Slot", font=FONT_BOLD)
    parking_slot_label.place(relx=0.78, rely=0.2)

    # Creating a photoimage object to use image
    photo = PhotoImage(file="images/admin.png")

    #2# def create_button(text, command, x_pos):
    #     return Button(root, text=text, bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica", 14, "bold"),
    #                   bd=3, padx=10, pady=5, relief=RAISED, activebackground="#FFC300", activeforeground="#006400",
    #                   cursor="hand2", width=22, command=command).place(relx=x_pos, rely=0.1)

    # def create_button(text, command, x_pos):
    #     return Button(root, text=text, bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica", 14, "bold"),
    #                   bd=3, padx=10, pady=5, relief=RAISED, activebackground="#FFC300", activeforeground="#006400",
    #                   cursor="hand2", width=22, command=command).place(relx=x_pos, rely=0.1)

    # Pehle se buttons create karna, taki bar-bar naye buttons na banaye jaye
    button_file = Button(root, text="Select Image From File System", bg=BUTTON_BG, fg=BUTTON_FG,
                         font=("Helvetica", 14, "bold"), bd=3, relief=RAISED, activebackground="#FFC300",
                         activeforeground="#006400", cursor="hand2", command=select_from_file)
    button_file.place(relx=0.05, rely=0.15, relwidth=0.3)

    button_camera = Button(root, text="Image From Camera", bg=BUTTON_BG, fg=BUTTON_FG,
                           font=("Helvetica", 14, "bold"), bd=3, relief=RAISED, activebackground="#FFC300",
                           activeforeground="#006400", cursor="hand2", command=select_from_camera)
    button_camera.place(relx=0.4, rely=0.15, relwidth=0.3)


    # Button(root, text='Click Me !', ).pack(side=TOP)
    # image_from_file_button = Button(root, text="Select Image From File System", bg="yellow", font=("Helvetica", 15),
    #                                 fg="green", bd=4, padx=1, pady=1, command=select_from_file)
    # image_from_camera_button = Button(root, text="Image From Camera", bg="yellow", font=("Helvetica", 15),
    #                                   fg="green", bd=4, padx=1, pady=1, command=select_from_camera)

    # create_button("Select Image From File System", select_from_file, 0.05)
    # create_button("Image From Camera", select_from_camera, 0.4)

    def countNumberOfSlotInDB():
        query = "select count(*) from users"
        mycursor.execute(query)
        print("============number of car in parking slot")
        # print(list(mycursor)[0][0])
        n = list(mycursor)[0][0]
        return n


    # def createLable(param, param1, color, text):
    #     lable = Label(root, bg=color, fg=TEXT_COLOR, padx=3, pady=1, text=text, font=FONT_BOLD).place(relx=param,
    #                                                                                                   rely=param1)

    def create_label(x, y, color, text):
        return Label(root, bg=color, fg=TEXT_COLOR, padx=10, pady=5, text=text, font=("Helvetica", 14, "bold"),
                     relief=RIDGE, width=3).place(relx=x, rely=y)


    # def showBoxes():
    #     n = countNumberOfSlotInDB()
    #     r = 0.6
    #     c = 0.2
    #     increase = 0.06
    #     count_fill_color = 1
    #     for row in range(6):
    #         temp = r
    #         for col in range(5):
    #             if (count_fill_color <= n):
    #                 createLable(temp, c, COLOR_RED, "F")
    #             else:
    #                 createLable(temp, c, COLOR_GREEN, "E")
    #             temp += increase
    #             count_fill_color += 1
    #         c += 0.1

    def showBoxes():
        n = countNumberOfSlotInDB()
        x, y = 0.65, 0.3
        x_inc, y_inc = 0.07, 0.1
        count = 1

        for row in range(5):
            temp_x = x
            for col in range(5):
                color, text = (COLOR_RED, "F") if count <= n else (COLOR_GREEN, "E")
                create_label(temp_x, y, color, text)
                temp_x += x_inc
                count += 1
            y += y_inc


    def adjust_layout(event):
        width = root.winfo_width()

        # Adjust font sizes dynamically
        lable1.config(font=("Helvetica", int(width * 0.02), "bold"))
        parking_slot_label.config(font=("Helvetica", int(width * 0.02), "bold"))

        # Adjust button width dynamically
        button_file.config(font=("Helvetica", int(width * 0.015), "bold"))
        button_camera.config(font=("Helvetica", int(width * 0.015), "bold"))


    root.bind("<Configure>", adjust_layout)
    showBoxes()

    root.mainloop()

    # showBoxes()
    # root.mainloop()

    # showBoxes()
    # image_from_file_button.place(relx=0.03, rely=0.1)
    # image_from_camera_button.place(relx=0.3, rely=0.10)
    # root.mainloop()

    # Wait for the video_process to finish
    video_process.join()


