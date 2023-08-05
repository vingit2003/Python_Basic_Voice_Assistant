import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning, Vini")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon, Vini")
    else:
        speak("Good evening, Vini")
    speak("I am Alpha. Your basic voice assistant. How may I help you?")

def time():
    hour = int(datetime.datetime.now().hour)
    speak("It is" + str(hour) + "hours")
    minutes = int(datetime.datetime.now().minute)
    speak(str(minutes) + "minutes")
    seconds = int(datetime.datetime.now().hour)
    speak(str(seconds) + "seconds")

def start_VA():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Listening . . . ")
        r.pause_threshold = 1 # Waits for 1 second before it completes listening
        r.energy_threshold = 200
        audio = r.listen(source)
    try:
        # print("Recognizing . . . ")
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e)
        # speak("Say that again please . . . ")
        return "None"
    return query

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening . . . ")
        r.pause_threshold = 1 # Waits for 1 second before it comletes listening
        r.energy_threshold = 200
        audio = r.listen(source)
    try:
        print("Recognizing . . . ")
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e)
        speak("Say that again please . . . ")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('vini.trial@gmail.com', 'abc')
    server.sendmail('vini.trial@gmail.com', to, content)
    server.close()

def transcribe_audio_to_text_and_save(filename):
    # Speech recognition using Google Speech Recognition
    try:
        transcription = takeCommand()
        print("You said: " + transcription)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return

    # Write the transcription to a file
    with open(filename, "w") as file:
        file.write(transcription)
        file.close()

if __name__ == "__main__":
    wishMe()
    while True:
        query2 = ""
        query1 = start_VA().lower()
        if 'hey alpha' in query1:
            speak("Hi, what can I do?")
            while(query2 != 'yes'):
                query = takeCommand().lower()
                # if 'exit' in query:
                #     exit()
                if 'wikipedia' in query:
                    speak('Searching Wikipedia . . . ')
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences = 2)
                    print(results)
                    speak("According to wikipedia" + results)

                elif 'open' in query:
                    url = query.replace("open ", "")
                    url = url.replace(" ", "")
                    webbrowser.open(url + ".com")

                elif 'play music' in query:
                    dir = 'C:\\Users\\vinee\\Desktop\\Music'
                    songs = os.listdir(dir)
                    print(songs)
                    os.startfile(os.path.join(dir, songs[0]))

                elif 'time' in query:
                    time()

                elif 'send mail' in query:
                    try:
                        speak("What should I send in the mail?")
                        content = takeCommand()
                        to = 'cvineetha2003@gmail.com'
                        sendEmail(to, content)
                        speak("Email has been sent!")
                    except Exception as e:
                        speak("Sorry, but Google no longer supports the use of third-party apps or devices which ask you to sign in to your Google Account using only your username and password.")

                elif 'take notes' in query:
                    try:
                        speak("Provide a file name")
                        f_name = takeCommand()
                        speak("Provide the text")
                        transcribe_audio_to_text_and_save(f_name)
                    except Exception as e:
                        speak("Can you repeat that again please")

                if 'exit' in query:
                    speak("Shall I exit?")
                    query2 = takeCommand()
                    if "yes" in query2:
                        break
        if 'yes' in query2:
            speak("Have a nice day!")
            speak("Goodbye!")
            exit()
