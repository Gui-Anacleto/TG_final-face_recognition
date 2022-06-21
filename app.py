#-*- coding: utf-8 -*-
from tkinter import *
from mysql.connector import Error
from PIL import ImageTk, Image
import face_recognition  
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from funcs import Funcs


root = Tk()

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frame_da_tela()
        self.widgets_frame()
        root.mainloop()

    def tela(self): 
        self.root.title("Principal")
        self.root.resizable(False, False)
        self.root.geometry("700x500")
        self.root.resizable(True,True)
        self.root.configure(background = "#708090");
        self.root.maxsize(width= 325, height=300) 
        self.root.minsize(width= 325, height=300)
          

    def tela_cad(self, cad=None):
        
        cad = Tk()
        self.cad = cad
        self.cad.title("Cadastrar")
        self.cad.resizable(False, False)
        self.cad.geometry("700x500")
        self.cad.resizable(True,True)
        self.cad.configure(background = "#708090");
        self.cad.maxsize(width= 325, height=150)
        self.cad.minsize(width= 325, height=150)

        def gravarDados():
            if tb_name.get() != "":

                name=tb_name.get()

                filetypes = (
                ('text files', '*.jpg'),
                ('All files', '*.*')
                )

                filename = fd.askopenfilename(
                    title='Select an Image',
                    initialdir='/',
                    filetypes=filetypes)
                
                    
                showinfo(
                    title='Select an Image',
                    message=filename,
                    
                )

                image = face_recognition.load_image_file(filename)
                image_cod = face_recognition.face_encodings(image)[0]

                
                varhex=str(image_cod) 
                varhex = varhex.rstrip('\r\n')
                print(varhex)

            
                self.conecta_bd()
                mycursor = self.conn.cursor()
                mycursor.execute("INSERT INTO login (user,pass_img) VALUES ('"+name+"','"+varhex+"')")
                self.conn.commit()
                self.desconecta_bd()

                tb_name.delete(0,END)
                status2 = ""
                status1 = Label(self.frame1, text="Dados gravados com sucesso", height= 2, foreground="green")
                status1.place(relx = 0.02, rely=0.76, relwidth=0.95)
                        
                 
            else:
                #print("ERRO")
                status1 = ""
                status2 = Label(self.frame1, text="Erro ao gravar dados, selecione uma imagem que \n contenha um rosto, e não deixe em branco o nome !",height= 2, foreground="red")
                status2.place(relx = 0.02, rely=0.74, relwidth=0.95)
                
        
        self.frame1 = Frame(self.cad, bd=4, highlightbackground="#6495ED", highlightthickness=2)
        self.frame1.place(relx=0.02 , rely=0.02, relwidth=0.96, relheight=0.96)

        l2=Label(self.frame1, text="Nome")
        l2.place(relx = 0.10, rely=0.03)

        tb_name = Entry(self.frame1)
        tb_name.place(relx=0.10 , rely=0.23, relwidth=0.6)
        
        # open button
        open_button = Button(self.frame1,text='Select an Image',command=gravarDados)
        open_button.place(relx = 0.30, rely=0.44, relwidth=0.4 , relheight=0.30)

    def frame_da_tela(self):
        self.frame1 = Frame(self.root, bd=4, highlightbackground="#6495ED", highlightthickness=2)
        self.frame1.place(relx=0.02 , rely=0.02, relwidth=0.96, relheight=0.96) 

    def widgets_frame(self):

        load = Image.open("./imgs/imgcerta.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self.frame1, image=render)
        img.image = render
        img.place(relx = 0.15, rely=0.05)
        
        self.aut = Button(self.frame1, text="Autenticar", bd=2, bg="#DCDCDC" , highlightthickness=2, fg = "Black" , font =("Arial", 11), command=self.aut_face)
        self.aut.place(relx = 0.2, rely=0.8, relwidth=0.3 , relheight=0.15)

        self.cadastro = Button(self.frame1, text="Cadastrar", bd=2, bg="#DCDCDC" , highlightthickness=2 , font =("Arial", 11) , command=self.tela_cad)
        self.cadastro.place(relx = 0.51, rely=0.8, relwidth=0.3 , relheight=0.15)

Application()