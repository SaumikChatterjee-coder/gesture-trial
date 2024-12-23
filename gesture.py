import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import pyautogui as auto
import subprocess

def is_hand_open(landmark):

    fingers=[(i,i-1) for i in range(4,24,4)]
    hand_open=False
    for tip,mid in fingers:
        if landmark[tip].y > landmark[mid].y:
            hand_open=True
        else:
            continue

    return hand_open

def is_claw(landmark):
    
    claw=False
    fingers = [(4, 2), (8, 6), (12, 10), (16, 14), (20, 18)]
    for tip,base in fingers:
        if landmark[tip].y > landmark[base].y:
            claw=True
        else:
            continue


    return claw



mp_hands=mp.solutions.hands
hands = mp_hands.Hands(

    static_image_mode=False, 
    model_complexity=1, 
    min_detection_confidence=0.75, 
    min_tracking_confidence=0.75, 
    max_num_hands=2
)

buffer=cv2.VideoCapture(0)
current_process=None

while True:
    
    ret,img=buffer.read()

    if not ret:
        break

    img=cv2.flip(img,1)
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)

    if results.multi_hand_landmarks:
      
      for hand_landmarks in results.multi_hand_landmarks:
        if is_claw(hand_landmarks.landmark):
            if current_process is None or current_process.poll() is not None:  
                current_process = subprocess.Popen(["leafpad"])
        elif current_process and is_hand_open(hand_landmarks.landmark):
            current_process.terminate()
            currentq_process= None
            
    cv2.imshow("img",img)
    if cv2.waitKey(1)==ord('q'):
        break

buffer.release()
cv2.destroyAllWindows()
