import pyttsx3
engine = pyttsx3.init()
engine.setProperty('voice', "mb-it3")
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)
engine.say('Che bella giornata per fare l\'assistente vocale.')
engine.runAndWait()
