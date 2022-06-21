#-*- coding: utf-8 -*-
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
        password='ffreitas788'
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

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame, model='hog')
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []

                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)

                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Não identificado"

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            
            # Display the resulting image
            

            cv2.imshow('Captura de Face | Precione "q" para sair', frame)
            
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.desconecta_bd()
                break

        # Release handle to the webcam

        cv2.destroyAllWindows()
        video_capture.release()

