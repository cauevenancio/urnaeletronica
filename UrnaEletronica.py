import mysql.connector
from tkinter import *
from mysql.connector import Error
from time import sleep
from threading import Timer
from PIL import Image, ImageTk
import pygame


class Urna():
    def __init__(self, window):
        
        self.root = window 
        self.root.title("Urna do SENAI")
        self.root.geometry("1280x850+100+100")
        self.root.config(bg = "light grey")
        
        self.root.bind('<KeyPress>', self.bloqueio)

        
        self.apresentacao = '''
JUSTIÇA
DO SENAI
                    '''

        self.rodape = ''
        
        self.ponteiro = 0
        self.imagem = ''
        self.nome = ''
        self.branco = 0
        self.confirma = StringVar()
        self.gatilho = 0
        
        self.layout()
        self.configLista()
        self.conecta()

        self.cursor = self.conexao.cursor()
        

        

        if self.conexao != 1:
            self.usaDb()
            self.candidatotable()
            self.candidatoinfo()
            self.foto('cinza.png')

        else:
            print("Não conseguimos conectar ao Banco de dados. Por favor, revise sua conexão.\n Programa fechando...")
            exit()

        

    def layout(self):
        
        self.lbl1 = Label(self.root, bg= "light grey", text= self.apresentacao, font="Helvetica 30")
        self.lbl1.place(relx=0.8 ,rely=0.05)

        self.esc = Label(self.root, bg= "light grey", text= "Melhor escritor", font="Helvetica 30")
        self.esc.place(relx=0.2 ,rely=0.1)

        self.img = Label(self.root, image = self.imagem, anchor = CENTER)
        self.img.place(relx=0.1 ,rely=0.2, relwidth = 0.4, relheight = 0.3 )
        
        self.lbl4 = Label(self.root, text="",bd="2", font = "Helvetica 20", bg = "light grey")
        self.lbl4.place(relx=0.2,rely=0.65)

        self.lbl3 = Label(self.root, text="",bd="2", font = "Helvetica 20", bg = "light grey", anchor = CENTER)
        self.lbl3.place(relx=0.2,rely=0.55)

        self.lbl2 = Frame(self.root,bg= "light grey")
        self.lbl2.place(relx=0.6 ,rely=0.28)

        self.lbl5 = Label(self.root, text="",bd="2", font = "Helvetica 20", bg = "light grey", anchor = CENTER)
        self.lbl5.place(relx=0.25 ,rely=0.5)
        #---------tela----------#

        tela = Frame(self.root, bg= "light grey")
        tela.place(relx=0,rely=0.8, relwidth = 0.6, relheight = 0.15)
        self.lblroda = Label(tela, bg= "light grey", text = self.rodape, font="Helvetica 20")
        self.lblroda.place(relx = 0, rely = 0.05, relwidth = 1, relheight = 1)

        

    def configLista(self):
       self.criaBtn("btn1",self.lbl2, "1",0,0, '1')
       self.criaBtn("btn2",self.lbl2, "2",0,1, '2')#, adicionar(2))
       self.criaBtn("btn3",self.lbl2, "3",0,2, '3')#, adicionar(3))
       self.criaBtn("btn4",self.lbl2, "4",1,0, '4')#, adicionar("4"))
       self.criaBtn("btn5",self.lbl2, "5",1,1, '5')#, adicionar("5"))
       self.criaBtn("btn6",self.lbl2, "6",1,2, '6')#, adicionar("6"))
       self.criaBtn("btn7",self.lbl2, "7",2,0, '7')#, adicionar("7"))
       self.criaBtn("btn8",self.lbl2, "8",2,1, '8')#, adicionar("8"))
       self.criaBtn("btn9",self.lbl2, "9",2,2, '9')#, adicionar("9"))
       self.criaBtn("btn0",self.lbl2, "0",3,1, '0')#, adicionar("0"))
       esp = Button(self.lbl2, bg="light grey",state=DISABLED, relief=FLAT,activebackground="light grey", width="7")
       esp.grid(row=4,column=0)
       branco = Button(self.lbl2, bg="white", relief=RAISED, text="Branco",font="Helvetica 30",activebackground="white", activeforeground="grey", fg="black", width="7", command = self.brancro)
       branco.grid(row=5,column=0)
       corrige = Button(self.lbl2, bg="red", relief=RAISED, text="Corrige",font="Helvetica 30",activebackground="red", activeforeground="grey", fg="black", width="7", command = self.cancelar)
       corrige.grid(row=5,column=1)
       confirma = Button(self.lbl2, bg="green", relief=RAISED, text="Confirma",font="Helvetica 30",activebackground="green", activeforeground="grey", fg="black", width="7", command = self.confirmar)
       confirma.grid(row=5,column=2)

    def conecta(self):
        try:
            self.conexao = mysql.connector.connect(user = "root",
						   host = "127.0.0.1")                                       
            return self.conexao
        
        except:
            print("Não foi possível conectar ao SGBD.")
            return 1

    def usaDb(self):
        try:
            self.cursor.execute("CREATE DATABASE urna;")
            self.cursor.execute("USE urna;")
            print("Banco de dados Urna criado")
        except:
            self.cursor.execute("USE urna;")
            print("Banco de dados Urna selecionado")

    def candidatotable(self):
        try:
            self.cursor.execute('''CREATE TABLE escritor(
                            nome VARCHAR(100) NOT NULL,
                            chapa VARCHAR(2) NOT NULL PRIMARY KEY,
                            imagem VARCHAR(250) NOT NULL,
                            votos INT(10));''')

            self.cursor.execute('''CREATE TABLE branco(
                            nome VARCHAR(100) NOT NULL PRIMARY KEY,
                            votos INT(10));''')

            self.cursor.execute('''CREATE TABLE nulo(
                            nome VARCHAR(100) NOT NULL PRIMARY KEY,
                            votos INT(10));''')
        
            print("Tabela criada com sucesso!")

        except:
            print("Tabelas já foi criada!")

    def candidatoinfo(self):
        try:
            
            joanaNome = "Joana Darc"     
            joanaChapa = "22"
            joanaImagem = "joaninha.png"

            votos = "0"

            tiriricaNome = "Tiririca"
            tiriricaChapa = "57"
            tiriricaImagem = "tiririca.png"

            moçonome = "Careca do T.I."
            moçoChapa = "11"
            moçoImagem = "moço.png"

            jkNome = "J. K. Rowling"
            jkChapa = "89"
            jkImagem = "jk.png"

            georgeNome = "George Lucas"
            georgeChapa = "04"
            georgeImagem = "george.png"

            pfizerNome = 'Pfizer'
            pfizerChapa = '19'
            pfizerImagem = 'pfizer.png'

            trName = 'The Rock'
            trChapa = '99'
            trImagem = 'tr.png'



            
            self.cursor.execute(f"INSERT INTO escritor(nome, chapa, imagem, votos) VALUES ('{joanaNome}', '{joanaChapa}', '{joanaImagem}', '{votos}');")
            self.conexao.commit()

            self.cursor.execute(f"INSERT INTO escritor(nome, chapa, imagem, votos) VALUES ('{moçonome}', '{moçoChapa}', '{moçoImagem}', '{votos}');")
            self.conexao.commit()

            self.cursor.execute(f"INSERT INTO escritor(nome, chapa, imagem, votos) VALUES ('{tiriricaNome}', '{tiriricaChapa}', '{tiriricaImagem}', '{votos}');")
            self.conexao.commit()

            self.cursor.execute(f"INSERT INTO escritor(nome, chapa, imagem, votos) VALUES ('{georgeNome}', '{georgeChapa}', '{georgeImagem}', '{votos}');")
            self.conexao.commit()

            self.cursor.execute(f"INSERT INTO escritor(nome, chapa, imagem, votos) VALUES ('{jkNome}', '{jkChapa}', '{jkImagem}', '{votos}');")
            self.conexao.commit()

            self.cursor.execute(f"INSERT INTO escritor(nome, chapa, imagem, votos) VALUES ('{trName}', '{trChapa}', '{trImagem}', '{votos}');")
            self.conexao.commit()

            self.cursor.execute(f"INSERT INTO escritor(nome, chapa, imagem, votos) VALUES ('{pfizerNome}', '{pfizerChapa}', '{pfizerImagem}', '{votos}');")
            self.conexao.commit()

            self.cursor.execute(f"INSERT INTO branco(nome, votos) VALUES ('brancoo', '0');")
            self.conexao.commit()

            self.cursor.execute(f"INSERT INTO nulo(nome, votos) VALUES ('nuloo', '0');")
            self.conexao.commit()

        except:
            pass

    def cancelar(self):

        if self.branco == 1 or self.branco == 2 or self.branco == 3:
            
            self.lbl4['text'] = ''
            self.img['image'] = ''
            self.lbl3['text'] = ''
            self.lblroda['text'] = ''
            self.branco = 0
            self.ponteiro = 0
            self.foto('cinza.png')
            self.lbl5['text'] = ''
            
        else:

            self.lbl4['text'] = ''
            self.img['image'] = ''
            self.lbl3['text'] = ''
            self.lblroda['text'] = ''
            self.ponteiro = 0
            self.lbl5['text'] = ''
            self.foto('cinza.png')
            
    def brancro(self):

        self.cancelar()
        
        self.lblroda['text'] = '''
Aperte a tecla
CONFIRMA - Para votar em branco
CORRIGE - Para cancelar
                    '''
        self.branco = 1

    def scannerCandidato(self):
        nome = self.lbl3['text']

        try:
            self.cursor.execute(f'SELECT * FROM escritor WHERE chapa = "{nome}"')
            resultado = self.cursor.fetchall()
                    
            if len(resultado) != 0:
                self.cursor.execute(f'SELECT imagem FROM escritor WHERE chapa = "{nome}"')

                listemp = []
                for i in self.cursor:
                    listemp.append(i[0])
                
                self.foto(listemp[0])
                

                self.cursor.execute(f'SELECT nome FROM escritor WHERE chapa = "{nome}"')

                listemp = []
                for i in self.cursor:
                    listemp.append(i[0])
                
                self.lbl4['text'] = listemp[0]

                self.lblroda['text'] = '''
Candidato selecionado. Aperte a tecla:
CONFIRMA - Para votar 
CORRIGE - Para cancelar
                                '''
                
                self.branco = 3
                

                    

            else:
                self.cancelar()
                self.lblroda['text'] = '''
Candidato não existente. Aperte a tecla:
CONFIRMA - Para votar nulo
CORRIGE - Para cancelar
                                '''
                self.branco = 2
        except Error as er:
            print(er)

    def confirmar(self):
        nome = self.lbl3['text']

        if self.branco == 0:
            pass

        if self.branco == 1:
            votos = 0
            brancoo = 'brancoo'
            
            self.cursor.execute(f'SELECT * FROM branco WHERE nome = "{brancoo}"')
            resultado = self.cursor.fetchall()
                
            if len(resultado) != 0:
                self.cursor.execute(f'SELECT votos FROM branco WHERE nome = "{brancoo}"')

                listemp = []
                for i in self.cursor:
                    listemp.append(i[0])
                
                votos = listemp[0]

                votos = votos + 1

                self.cursor.execute(f'UPDATE branco SET votos = "{votos}" WHERE nome = "{brancoo}"')
                self.conexao.commit()
                
            pygame.mixer.init()
            pygame.mixer.music.load("somurna.mp3")
            pygame.mixer.music.play(loops = 0)

            self.cancelar()

            self.lbl5['text'] = 'FIM'

            t = Timer(1, self.cancelar)
            t.start()

        if self.branco == 2:
            votos = 0
            nulo = 'nuloo'
            
            self.cursor.execute(f'SELECT * FROM nulo WHERE nome = "{nulo}"')
            resultado = self.cursor.fetchall()
                
            if len(resultado) != 0:
                self.cursor.execute(f'SELECT votos FROM nulo WHERE nome = "{nulo}"')

                listemp = []
                for i in self.cursor:
                    listemp.append(i[0])

                votos = listemp[0]
                votos = votos + 1

                self.cursor.execute(f'UPDATE nulo SET votos = "{votos}" WHERE nome = "{nulo}"')
                self.conexao.commit()
            pygame.mixer.init()
            pygame.mixer.music.load("somurna.mp3")
            pygame.mixer.music.play(loops = 0)

            self.cancelar()

            self.lbl5['text'] = 'FIM'

            t = Timer(1, self.cancelar)
            t.start()


        if self.branco == 3:
            votos = 0
            
            self.cursor.execute(f'SELECT * FROM escritor WHERE chapa = "{nome}"')
            resultado = self.cursor.fetchall()
            
            if len(resultado) != 0:
                self.cursor.execute(f'SELECT votos FROM escritor WHERE chapa = "{nome}"')

                listemp = []
                for i in self.cursor:
                    listemp.append(i[0])

                votos = listemp[0]
                votos = votos + 1

                self.cursor.execute(f'UPDATE escritor SET votos = "{votos}" WHERE chapa = "{nome}"')
                self.conexao.commit()

            pygame.mixer.init()
            pygame.mixer.music.load("somurna.mp3")
            pygame.mixer.music.play(loops = 0)

            self.cancelar()

            self.lbl5['text'] = 'FIM'

            t = Timer(1, self.cancelar)
            t.start()

        



    def criaBtn(self, nomeBtn,lbl, texto, linha, coluna, event):
        nomeBtn = Button(lbl, bg="black", relief=RAISED, text=texto,font="Helvetica 30",activebackground="black", activeforeground="grey", fg="white", width="7", command=lambda: self.chapa(event))
        nomeBtn.grid(row=linha,column=coluna)

    def chapa(self, numero):
        try:
            if self.ponteiro == 0:
                self.lbl3['text'] += numero
                self.ponteiro = 1
            elif self.ponteiro == 1:
                self.lbl3['text'] += numero
                self.ponteiro = 2
                self.scannerCandidato()
                
            else:
                pass
        except:
            pass
        


    def bloqueio(self, evento):
        lista = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for valor in lista:
            if str(evento.char) == valor:
                self.chapa(valor)

    def foto(self, event):

        self.amostra = ImageTk.PhotoImage(Image.open(event))

        self.img = Label(self.root, image = self.amostra, bg = 'light grey')
        self.img.place(relx=0.1 ,rely=0.2, relwidth = 0.4, relheight = 0.3 )


if __name__ == "__main__":
    janela = Tk()
    app = Urna(janela)
    janela.mainloop()
