import speech_recognition as sr

def Test_recognition():
    while True:
    # Initialize recognizer
        recognizer = sr.Recognizer()

        # Use the microphone as the audio source
        with sr.Microphone() as source:
            print("Please speak something...")
            # Adjust for ambient noise and record audio
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    Test_recognition()