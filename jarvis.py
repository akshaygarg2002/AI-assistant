import pyttsx3
import ssl
import speech_recognition as sr
import datetime
import os
import cv2
from requests import get
import random
import wikipedia
import webbrowser
import pywhatkit
import smtplib
import sys
import time

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
print(voices[0].id)
engine.setProperty("voices",voices[1].id)
volume = engine.getProperty("volume")
#engine.setProperty("rate",150)
c = 0
#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# voice to text
def takecommand(c):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold = 1
        r.adjust_for_ambient_noise(source) # to improve quality of listening based on background added on 17-08-22
        print("listening ..........")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=660,phrase_time_limit=5)
    try:
        print("recognising.......")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        if c==1 and ("jarvis" not in query.lower()):
            return "none"

    except Exception as e:
        if c==0:
            speak("Sorry, say that again Please......")
        return "none"

    return query

#wish you good morning or good afternoon
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour <=12:
        speak("Good Morning Sir")
    elif hour>12 and hour <= 18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    speak("I am Jarvis, Sir Please tell me How can I help You?")



# to send email
def sendEmail(to,content):
    smtp_port = 587
    smtp_server = "smtp.gmail.com"

    simple_email_context = ssl.create_default_context()

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls(context=simple_email_context)
    server.login("akshaygargbaghpat@gmail.com", "kxypoanxtayflpik")
    server.sendmail("akshaygargbaghpat@gmail.com", to, content)
    server.quit()
    #print("email sent")
if __name__=="__main__":
    wish()
    while True:
        query = takecommand(c).lower()
        while query == "none":
            c = 1
            query = takecommand(c).lower()
        if c==1:
            query = query.replace("jarvis ","")
        c = 0
        # logics to perform tasks
        if "open notepad" in query:
            npath = "C:\\windows\\system32\\notepad.exe"
            os.startfile(npath)

        #for time
        elif "what is the time" in query:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            h, m, s = map(int, current_time.split(":"))
            if h>11:
                speak(f"Sir, the current time is {h} : {m} PM")
            else:
                speak(f"Sir, the currentt time is {h} : {m} AM")

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            cv2.namedWindow("Python webcam app")
            img_counter = 0
            while True:
                ret,img = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                cv2.imshow("webcamUsingPython",img)
                k = cv2.waitKey(1)

                # to check if escape key is pressed if yes then application (camera) should be closed
                if k%256==27:
                    print("escape hit, closing the app")
                    break

                # to check if space bar is pressed if yes then it will click the picture
                elif k%256 == 32:
                    img_name = 'opencv_frame_{}.png'.format(img_counter)
                    cv2.imwrite(img_name,img)
                    speak("Sir, Picture has been taken.")
                    img_counter +=1

            cap.release()
            #cap.destroyAllWindows()


        elif "play music" in query:
            path = "C:\\Users\\HP\\Desktop\\music"
            songs = os.listdir(path)
            rd = random.choice(songs)
            for song in songs:
                os.startfile(os.path.join(path,song))

        elif "ip address" in query:
            ip = get("https://api.ipify.org").text
            speak(f"Your IP adress is : {ip}")

            """elif "wikipedia" in query:
            speak("searching wikipedia.......")
            query = query.replace("according to wikipedia","")
            results = wikipedia.summary(query,sentences= 2)
            speak("According to wikipedia : ")
            speak(results)"""

        elif "stackoverflow" in query:
            webbrowser.open("www.stackoverflow.com")

        elif "quora" in query:
            webbrowser.open("www.quora.com")

        elif "google search" in query:
            import wikipedia as googlescrap
            query = query.replace("google search","")
            speak("Sir this is what I found on Google!")
            pywhatkit.search(query)
            try:
                result = googlescrap.summary(query,3)
                speak(result)
            except:
                speak("No, Speakable data avialable")

        elif "send message" in query:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            h,m,s = map(int,current_time.split(":"))
            speak("TO whom, should I send Message")
            name = takecommand(c).lower()
            speak("What should I say?")
            message = takecommand(c)
            dir = {"vinay":"+918218709999","akshay":"+917464899999","sachin":"+919756399999","avinash":"+919335599992","aditya":"+917310689999"}
            if name in dir.keys():
                pywhatkit.sendwhatmsg(dir[name],message,h,m+1)
            else:
                speak("Sorry sir, this contact is not in the directory Please provide me the number")
                no = "+91"+(takecommand(c))
                dir[name]=no
                pywhatkit.sendwhatmsg(dir[name], message, h, m + 1)

        elif "play songs on youtube" in query:
            speak("Which song do you wanna listen?")
            search = takecommand(c).lower()
            pywhatkit.playonyt(search)

        elif "email" in query:
            try:
                speak("what should i say?")
                content = takecommand(c).lower()
                to = "vinayskb2@gmail.com"
                sendEmail(to,content)
                speak(f"Email has been sent to {to}")

            except Exception as e:
                print(e)
                speak("Sorry sir, I am not able to send this email.")

        elif "no thanks" in query:
            speak("Thanks for using me sir, have a good day.")
            sys.exit()

        # 17-08-22.


        elif "speak loudly" in query:
            volume = engine.getProperty("volume")
            if volume == 1.0:
                speak("Sorry sir, I can't speak more loudly")
            else:
                engine.setProperty("volume",volume+0.1)

        elif "lower your voice" in query:
            volume = engine.getProperty("volume")
            if volume==0.0:
                speak("I can't speak below this voice")

            else:
                engine.setProperty("volume",volume-.1)

        elif "go faster" in query:
            rate = engine.getProperty("rate")
            if rate >=251:
                speak(f"Sir, current speech rate is {rate}")
                speak("Above this speech rate it will ge difficult for you to listen my words properly.")
            else:
                speak(f"Sir, current speech rate is {rate}")
                engine.setProperty("rate",rate+17)

        elif "speak slowly" in query:
            rate = engine.getPropery("rate")
            if rate<= 149:
                speak(f"Sir, current speech rate is {rate}")
                speak("Sir, this speec rate is too slow to understand.")
            else:
                speak(f"Sir, current speech rate is {rate}")
                engine.setProperty("rate",rate-17)


        # first day

        speak("Sir, do you have any other work")
