
import numpy as np
import cv2
import RPi.GPIO as GPIO
import time



# Pin Definitons:
led_pin = 12  # Board pin 12
but_pin = 18  # Board pin 18
led_pin_2 = 13 



def gstreamer_pipeline (capture_width=3280, capture_height=2464, display_width=800, display_height=480, framerate=60, flip_method=0) :   
    return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))

def face_detect() :

    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output
    GPIO.setup(but_pin, GPIO.IN)  # button pin set as input
    GPIO.setup(led_pin_2, GPIO.OUT)

    GPIO.output(led_pin, GPIO.LOW)
    GPIO.output(led_pin_2, GPIO.HIGH)

    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        cv2.namedWindow('Face Detect', cv2.WINDOW_AUTOSIZE)
        while cv2.getWindowProperty('Face Detect',0) >= 0:
            ret, img = cap.read()
            

            print("Waiting for button event")
            GPIO.wait_for_edge(but_pin, GPIO.FALLING)

            # event received when button pressed
            print("Button Pressed!")
            cv2.imshow('boom',img)
            cv2.imwrite('red.png',img)
            GPIO.output(led_pin, GPIO.HIGH)
            GPIO.output(led_pin_2, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(led_pin, GPIO.LOW)
            GPIO.output(led_pin_2, GPIO.HIGH)


            keyCode = cv2.waitKey(30) & 0xff
            # Stop the program on the ESC key
            if keyCode == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")

if __name__ == '__main__':
    face_detect()
