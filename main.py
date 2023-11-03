# instalar: pip install opencv-contrib-python
# instalar: pip install opencv-python

from pathlib import Path
from calibracion_camara.calibracion_funcion import generar_matriz_y_dist
import cv2
import numpy as np
from time import sleep

# Inicializar paramtros de detector de arucos
parametros = cv2.aruco.DetectorParameters()

# Cargar diccionario de aruco
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)

# Inicializar camara
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
cont = 0

# Calibracion
matrix, dist = generar_matriz_y_dist()
print(f"Matriz de la camara: {matrix}")
print(f"Coeficiente de Distorsion: {dist}")

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
cont = 0

while cap.isOpened():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Deteccion de marcadores de la imagen
    esquinas, ids, candidatos_malos = cv2.aruco.detectMarkers(
        gray, diccionario, parameters=parametros
    )

    if np.all(ids != None):
        # Iterar en marcadores
        for i in range(0, len(ids)):
            # Estime la pose de cada marcador y devuelve los valores rvec y tvec (son distintos a los de la calibracion)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(
                esquinas[i], 0.02, matrix, dist
            )

            # eliminar error en matriz de numpy
            (rvec - tvec).any()

            # dibujar cuadrado en los alrededores
            cv2.aruco.drawDetectedMarkers(frame, esquinas)

            # # Dibujar marcadores
            # cv2.aruco.drawAxis(frame, matrix, dist, rvec, tvec, 0.01)  # Draw Axis

            # # Centro del marcador en el eje X
            # c_x = (
            #     esquinas[i][0][0][0]
            #     + esquinas[i][0][1][0]
            #     + esquinas[i][0][2][0]
            #     + esquinas[i][0][3][0]
            # ) / 4

            # # Centro del marcador en el eje y
            # c_y = (
            #     esquinas[i][0][0][1]
            #     + esquinas[i][0][1][1]
            #     + esquinas[i][0][2][1]
            #     + esquinas[i][0][3][1]
            # ) / 4

            # # Texto
            # cv2.putText(
            #     frame,
            #     "id" + str(ids[i]),
            #     (int(c_x), int(c_y)),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.5,
            #     (50, 225, 250),
            #     2,
            # )

            # # Extraer los puntos de las esquinas en coordenadas separadas
            c1 = (esquinas[0][0][0][0], esquinas[0][0][0][1])
            c2 = (esquinas[0][0][1][0], esquinas[0][0][1][1])
            c3 = (esquinas[0][0][2][0], esquinas[0][0][2][1])
            c4 = (esquinas[0][0][3][0], esquinas[0][0][3][1])
            v1, v2 = c1[0], c1[1]
            v3, v4 = c2[0], c2[1]
            v5, v6 = c3[0], c3[1]
            v7, v8 = c4[0], c4[1]

            copy = frame

            # leer la imagen
            imagen = cv2.imread("./images/images_over_pattern/img2.jpg")

            # Tamano de la imagen
            tamano = imagen.shape

            puntos_aruco = np.array([c1, c2, c3, c4])

            # Organizar los puntos de la imagen
            puntos_imagen = np.array(
                [
                    [0, 0],
                    [tamano[1] - 1, 0],
                    [tamano[1] - 1, tamano[0] - 1],
                    [0, tamano[0] - 1],
                ],
                dtype=float,
            )

            # Realizamos la superposicion de la imagen (Homografia)
            h, estado = cv2.findHomography(puntos_imagen, puntos_aruco)

            # Realizamos la transformación de perspectiva
            perspectiva = cv2.warpPerspective(imagen, h, (copy.shape[1], copy.shape[0]))
            cv2.fillConvexPoly(copy, puntos_aruco.astype(int), 0, 16)
            copy = copy + perspectiva
            cv2.imshow("hola", copy)

    else:
        cv2.imshow("hola", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
