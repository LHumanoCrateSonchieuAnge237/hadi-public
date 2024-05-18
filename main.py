#------------------------------interface graphique de l'application-------------------------
from tkinter import *
from gtts import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
from pyttsx3 import *
from os import *
from io import *
from speech_recognition import *
from pyaudio import *
from time import *
import fuzzywuzzy as fuzz #mieux comprendre le mot cle
import openai 
from pydub import * #recomposer les segments
#from simpleaudio import*
from configparser import *
import assemblyai as aai



root= Tk()
root.geometry('880x620')
root.config(bg='#7B68EE')
root.title('Votre Assistant Personnel')
root.resizable(height=False, width=False)
icon=PhotoImage(file="icon.png")
root.iconphoto(False,icon)


#----------------------------------trancrire un fichier audio en fichier texte---------------------------

aai.settings.api_key = "07a7ea9a1dec4b158ce423ef48e63a4d"
transcriber = aai.Transcriber()
transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")


Record = Recognizer()

def fichier(file):
    global record

    with AudioFile("file") as source:
        lecture = Record.record(file)
        texte = Record.recognize_google_cloud(lecture)
        print(texte)


#--------------------------------------l'assistant vocale---------------------

def hadi():
    #root.destroy()

    #root2=Tk()

    config = ConfigParser()
    config.read('HADI.ini')

    min_ratio = 80
    reconnait = Recognizer()

    with Microphone() as source :
        reconnait.adjust_for_ambient_noise(source)
        print('Dites "HADI" pour activer l\'assistant vocal ')
        play = reconnait.listen(source)

    try:
        transcire= reconnait.recognize_assemblyai(play)
        ratio = fuzz.token_set_ratio(transcire.lower(), "HADI")
        
        if ratio>=min_ratio:
            print("En attente de votre question")
            with Microphone() as source :
                reconnait.adjust_for_ambient_noise(source)
                play = reconnait.listen(source) 
            
            try:
                prompt = reconnait. recognize_assemblyai(play)
                print("Vous avez dit:"+prompt)
                completion = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_token=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )

                response=completion.choices[0].text
                tts= gTTS(response)
                tts.save("response.mp3")
            
            except UnknownValueError:
                print("Desolee je vous suis pas")

        else:
            print("Je ne reconnait pas le mot cle")

    except UnknownValueError:
        print("Desolee je vous suis pas")


           

#-------------------------------------ma barre de menu---------------------------------


menubar=Menu(root)
premMenu=Menu(menubar)
menubar.add_cascade(label="Menu", menu=premMenu)
premMenu.add_command(label="Text-Audio")
premMenu.add_command(label="Audio-Text")
premMenu.add_command(label="Video-Audio")

deuxMenu=Menu(root)
menubar.add_cascade(label="Assistant personnel", menu=deuxMenu)
deuxMenu.add_command(label="Appelez HADI", command=hadi)

troisMenu=Menu(root)
menubar.add_cascade(label="settings",  menu=troisMenu)
troisMenu.add_command(label='Design')
troisMenu.add_command(label='Help')

root.config(menu=menubar)



#----------------------------------fonctions logiques------------------------
engine = init()

def speaker():
    texte=zoneSaisie.get(1.0, END)
    Rapide=rapidite.get()
    gender=gend.get()
    Langue=traduc.get()
    voix=engine.getProperty('voices')

    def Language():
            if (Langue=='Francais'):
               result=gTTS(zoneSaisie, lang ='fr') 
            elif (Langue=='English'):
                result=gTTS(zoneSaisie, lang ='en') 
            elif (Langue=='Espagnol'):
                result=gTTS(zoneSaisie, lang ='es') 
            else :
                result=gTTS(zoneSaisie, lang ='de') 
            
            return result

    def voices():
        if( gender=='Male'):
            engine.setProperty('voice', voix[0].id)
            engine.say(texte) 
            engine.runAndWait()
        else:
            engine.setProperty('voice', voix[1].id)
            engine.say(texte)
            engine.runAndWait()
    
    if(texte):
        if (Rapide=="Fast"):
            engine.setProperty('rate',250)
            voices()
        elif (Rapide=="Normal"):
            engine.setProperty('rate',150)
            voices()
        else:
            engine.setProperty('rate',50)
            voices()




def upload(fichier):
    pass



def save():
   
    texte=zoneSaisie.get(1.0, END)
    
    gender=gend.get()
    Rapide=rapidite.get()
    voix=engine.getProperty('voices')


    def voices():
        if( gender=='Male'):
            engine.setProperty('voice', voix[0].id)
            down=filedialog.askdirectory()
            chdir(down)
            engine.save_to_file(texte, 'text.mp3')
            engine.runAndWait()
        else:
            engine.setProperty('voice', voix[1].id)
            down=filedialog.askdirectory()
            chdir(down)
            engine.save_to_file (texte, 'text.mp3')
            engine.runAndWait()
    
    if(texte):
        if (Rapide=='Fast'):
            engine.setProperty('rate',250)
            voices()
        elif (Rapide=='Normal'):
            engine.setProperty('rate',150)
            voices()
        else:
            engine.setProperty('rate',50)
            voices()







#-------------------------------------la facade de l'entree du texte---------------------------


accueil=Frame(root, bg='white', width=880, height=200)
logo=PhotoImage(file='text.png')
logo.config(width=300, height=200)

Label(accueil,  image=logo, bg="white" ).grid(column=1, row=1)
Label(accueil, text="Convert a text file to speech", font="arial 32 italic bold", bg="white", fg="black").grid(column=3, row=1)

accueil.pack()


#-----------------------------------les composantes----------------------------------
 

zoneSaisie=Text(root,bg="black", fg='white', width=45, height=13, font=("20"))
zoneSaisie.place(x=10, y=250)



Label(root, text="Gender", font=("Century 15 bold italic"), bg='#7B68EE', fg='yellow').place(x=560, y=250)

gend=Combobox(root, values=['Female', 'Male'], font=("Ebrima 20 bold"), width=6)
gend.place(x=550, y=300)
gend.set('Female')

Label(root, text="Langue", font=("Century 15 bold italic"), bg='#7B68EE', fg='yellow').place(x=560, y=380)

traduc=Combobox(root, values=['Francais' ,'English', 'Espagnol', 'Italien', 'Deutsch'  ], font=("Ebrima 20 bold"), width=6)
traduc.place(x=550, y=420)
traduc.set('Francais')

Label(root, text="Vitesse", font=("Century 15 bold italic"), bg='#7B68EE', fg='yellow').place(x=710, y=250)

rapidite=Combobox(root, values=['Fast' ,'Normal', 'Slow' ], font=("Ebrima 20 bold"), width=6)
rapidite.place(x=700, y=300)
rapidite.set('Normal')


spIm=PhotoImage(file="speaker.png")
spIm.configure(height=50, width=50)
speak=Button(root,compound=LEFT, image=spIm, text="Speaker", font=("Century 15 bold italic"), width=130, bg="green", command=speaker)
speak.place(x=550, y=500)


upload=Button(root, text="Upload", font=("Century 15 bold italic"), width=8, bg="green", command=upload)
upload.place(x=700, y=420)

save=Button(root, text="Save", font=("Century 15 bold italic"), width=8, bg="green", command=save)
save.place(x=700, y=500)



root.mainloop()