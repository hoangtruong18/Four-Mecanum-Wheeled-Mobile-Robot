# Four Mecanum Wheeled Mobile Robot
Notes: 
- This WebServer hasn't been hosted yet.
- Using camera mounted on ceiling
# About this project
This project uses microcontroller Adruino MEGA 2560 board and 4 Motor & 9 Servo motor driver board (which can drive 4 motors with two IC TB6612), especially this project uses ESP8266 for controlling the Mecanum wheel robot wirelessly. So we can improve and develop this project by combining the Computer Vision technology and http requests from URL for further function such as tracking control using camera and applying control theory algorithms.

# Requirements
Download Adruino IDE.

Download CH340 or CP210 Driver to get the COM port in Adruino IDE for uploading code.

Installing ESP8266 Board in Arduino IDE.

Pycharm or Python with Visual Studio Code.

All the libraries used in the project.

# Connection
![image](https://user-images.githubusercontent.com/104365389/167612848-7b9ce896-af12-422d-874b-f95f2e936a8c.png)

# How to run
1. Upload code for Adruino Mega2560 (ESP8266_with_Adruino.ino).
2. Upload code for ESP 8266 (Web_Server.ino), connect to your wifi with SSID and Password, then run the Serial Monitor in AdruinoIDE (where you upload the code for ESP 8266) to get ESP's IP address.
3. Copy ESP's url and paste it to line 8 in mylib.py: root_url = "paste url here".
4. Change the location of the dataset folder in test.py in line 52: img = cv2.imread(r"Your location\dataset\sample191.jpg")
5. Run getdata.py to get images of Marker from the camera for training, these images will be stored in dataset folder. 
6. Run test.py and adjust the trackbar to get the best mask of color.
7. Run main.py for trajectory tracking control.
# Robot model
![image](https://user-images.githubusercontent.com/104365389/167612064-ee5ca311-7745-4c1f-9225-c0a46ef3ab7f.png)


# Demo
- Mecanum Manual Control through WebSever with 8 directions: Link youtube: https://youtube.com/shorts/zPbL1e1BjeU
- Mecanum tracking control with rectangle trajectory using openCV and urllib.request library (with low quality): Link youtube: https://www.youtube.com/watch?v=ouCDkRBMcl0
