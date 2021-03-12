import cv2
import time
import numpy as np


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

video = cv2.VideoCapture(0)

time.sleep(3)
cnt = 0
back = 0

for i in range(60):
    ret, back = video.read()
back = np.flip(back, axis=1)


while (video.isOpened()):
    ret, img = video.read()
    if not ret:
        break
    cnt += 1
    img = np.flip(img, axis=1)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255,255])

    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])

    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2
   
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
   
    mask2 = cv2.bitwise_not(mask1)

 
    out1 = cv2.bitwise_and(img, img, mask=mask2)
   
    out2 = cv2.bitwise_and(back, back, mask=mask1)
   

    final = cv2.addWeighted(out1, 1, out2, 1, 0)

    out.write(final)

    cv2.imshow("cloak", final)

    cv2.waitKey(1)
    


video.release()
out.release()
cv2.destroyAllWindows()