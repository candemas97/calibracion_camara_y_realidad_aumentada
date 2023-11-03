from pathlib import Path
from time import sleep
import cv2

# cap = cv2.VideoCapture(2) # Camara externa
cap = cv2.VideoCapture(0)  # Camara Interna
num = 0


while cap.isOpened():
    succes, img = cap.read()
    for i in range(2):
        sleep(2)
        if i == 0:
            print("Preparate para la foto (2 seg)")

    cv2.imwrite(
        "./images/images_calibration/img" + str(num) + ".png", img
    )  # Toma la foto
    print("¡Foto Tomada!")
    num += 1

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    if num >= 20:
        break

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()
