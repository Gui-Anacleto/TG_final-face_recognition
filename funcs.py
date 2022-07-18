# _*_ coding: utf-8 _*_
from tkinter import *
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from PIL import ImageTk, Image
import os
import face_recognition  
import cv2
import numpy as np
from tkinter.messagebox import showinfo

class Funcs():
    
    def conecta_bd(self):
        self.conn= mysql.connector.connect(
        host='localhost',
        database='tg',
        user='root',
        password='fox115348'
        )
        self.conn.cursor();print("Conectado ao banco de dados")

    def desconecta_bd(self):
        self.conn.close();print("Desconectando do banco de dados")

    def aut_face(self):
        
        # Conexao com o banco de dados:
        self.conecta_bd()

        # Indica aonde será capturado o video:
        video_capture = cv2.VideoCapture(0)

        # Comandos no banco
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT pass_img FROM login")
        known_face_encodings = [item[0] for item in mycursor.fetchall()]

        mycursor = self.conn.cursor()
        mycursor.execute("SELECT user FROM login")
        known_face_names = [item[0] for item in mycursor.fetchall()]

        cont = 0

        for cont in range(len(known_face_encodings)):

            known_face_encodings[cont] = known_face_encodings[cont].replace("[","")
            known_face_encodings[cont] = known_face_encodings[cont].replace("]","")
            known_face_encodings[cont] = known_face_encodings[cont].replace('\n',"")
            known_face_encodings[cont] = known_face_encodings[cont].split(' ')
            known_face_encodings[cont] = list(filter(lambda x : x != '', known_face_encodings[cont]))
            known_face_encodings[cont] = np.array(known_face_encodings[cont])
            known_face_encodings[cont] = known_face_encodings[cont].astype(float)
            
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            # Grab a single frame of video
            
            ret, frame =  video_capture.read()

            # Tamanho do frame 1/4 
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Converte a imagem de BGR color (OpenCV) para RGB color (face_recognition)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Pesquisar todas as faces, e rostos encodados no video
                face_locations = face_recognition.face_locations(rgb_small_frame, model='hog')
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []

                for face_encoding in face_encodings:
                    # Verifica se os rostos encontrados são compatíveis com os rostos cadastrados.

                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    b=0
                    g=0
                    r=255
                    name = ("Nao identificado")

                    # Ou em vez disso use a face conhecida com a menor distância da nova face.
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        b=0
                        g=255
                        r=0
                        name = known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame

            # Display dos resultados
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Redimencionar os rostos.
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Desenhar o quadrado em volta do rosto
                cv2.rectangle(frame, (left, top), (right, bottom), (b, g, r), 2)

                # Deseshar a label do nome
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (b, g, r), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Captura de Face | Precione "q" para sair', frame)
            
            # Clicar em "q" para fechar tela de autenticação.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.desconecta_bd()
                break

        # Destroi o processo da webcam.

        cv2.destroyAllWindows()
        video_capture.release()

