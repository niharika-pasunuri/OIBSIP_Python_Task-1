import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import smtplib
import wikipedia
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand. Can you repeat?")
        return ""
    except sr.RequestError:
        speak("Could not connect to the internet.")
        return ""

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your Voice Assistant. How can I help you?")

def get_weather(city):
    api_key = "3f2f3a3555e0245bab6dc45fa09b572b"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    res = requests.get(url)
    data = res.json()
    if data["cod"] != 200:
        speak("City not found.")
        return
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    speak(f"The weather in {city} is {weather}.")
    speak(f"Temperature is {temp} degree Celsius, humidity is {humidity} percent, and wind speed is {wind} meters per second.")

def send_email(to, subject, body):
    sender = "pniharika1106@gmail.com"
    password = "123456789"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender, to, message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Failed to send email.")
        print(e)

def start_voice_assistant():
    greet()
    while True:
        query = listen()

        if "exit" in query or "stop" in query:
            speak("Goodbye! Have a nice day.")
            break

        elif "your name" in query:
            speak("I am your Python Voice Assistant.")

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "date" in query:
            today = datetime.datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today is {today}")

        elif "search" in query:
            speak("What should I search?")
            search_term = listen()
            url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(url)
            speak("Here are the search results.")

        elif "wikipedia" in query:
            speak("What should I search on Wikipedia?")
            topic = listen()
            try:
                result = wikipedia.summary(topic, sentences=2)
                speak(result)
            except:
                speak("Sorry, I couldn't find anything on Wikipedia.")

        elif "weather" in query:
            speak("Tell me the city name.")
            city = listen()
            get_weather(city)

        elif "email" in query:
            speak("Please enter the email address to send to:")
            to = input("Receiver Email: ")
            speak("What should be the subject?")
            subject = listen()
            speak("What is the message?")
            body = listen()
            send_email(to, subject, body)

        else:
            speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    start_voice_assistant()
