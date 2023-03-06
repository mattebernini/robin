import json
import openai
import pyttsx3
import datetime
import speech_recognition as sr

def ascolta():
    # deve diventare un thread background
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parla ora...")
        audio = r.listen(source)
    try:
        print("elaborando...")
        testo = r.recognize_google(audio, language="it-IT")
        print("Hai detto: " + testo)
        return testo
    except Exception as e:
        print("Errore: " + str(e))
    return None

def chiedi_a_gpt(messages:list, configs):
    api_key_openai = configs["OPEN_AI_API_KEY"]
    openai.api_key = api_key_openai
    try:
        response = openai.ChatCompletion.create(
            model = configs["model-gpt"],
            temperature = 0.0, # da 0 a 2 (randomicità)
            messages = messages
        )
        return response.choices[0].message
    except openai.error.Timeout as e:
        #Handle timeout error, e.g. retry or log
        print(f"OpenAI API request timed out: {e}")
        return None
    except openai.error.APIError as e:
        #Handle API error, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        return None
    except openai.error.APIConnectionError as e:
        #Handle connection error, e.g. check network or log
        print(f"OpenAI API request failed to connect: {e}")
        return None
    except openai.error.InvalidRequestError as e:
        #Handle invalid request error, e.g. validate parameters or log
        print(f"OpenAI API request was invalid: {e}")
        return None
    except openai.error.AuthenticationError as e:
        #Handle authentication error, e.g. check credentials or log
        print(f"OpenAI API request was not authorized: {e}")
        return None
    except openai.error.PermissionError as e:
        #Handle permission error, e.g. check scope or log
        print(f"OpenAI API request was not permitted: {e}")
        return None
    except openai.error.RateLimitError as e:
        #Handle rate limit error, e.g. wait or log
        print(f"OpenAI API request exceeded rate limit: {e}")
        return None

def parla(text, configs):
    engine = pyttsx3.init()
    engine.setProperty('voice', configs["voce"]["nome"])
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+configs["voce"]["rate-delta"])
    engine.say(text)
    engine.runAndWait()

def carica_contesto(frase):
    try:
        f = open("contesto/"+frase[1]+".md", "r")
    except:
        print("contesto non esistente")
        return False
    c = f.read()
    messages.append({"role": "system", "content": c})
    print("contesto "+frase[1]+" caricato")
    return True

def salva_chat(frase):
    f = open("chat/"+frase[1]+".md", "a")
    for m in messages:
        if m["role"] != "system":
            f.write("*"+m["role"]+"*: "+m["content"]+"\n")
    print("chat "+frase[1]+" salvata")

def impostazioni(comando, configs, messages):
    frase = comando.split(" ")
    match frase[0]:
        case "\\m":
            print(open("config/menu.md").read())
        case "\\l":
            if not carica_contesto(frase):
                return configs, messages
        case "\\s":
            salva_chat(frase)
        case _:
            print("comando non valido")
    return configs, messages

def aggiorna_log(comando, risposta):
    with open("log/chat.log", "a") as f:
        f.write(f"MATTE: {comando}\nROBIN: {risposta}\n")
    with open("log/comandi.log", "a") as f:
        f.write(comando+"\n")

def inizializza():
    # carico le configurazioni
    with open("config/config.json") as f:
        config = json.load(f)
        configs = dict(config)
    # inizializzo log
    oggi = str(datetime.datetime.now())
    with open("log/chat.log", "a") as f:
        f.write(oggi+"\n")
    with open("log/comandi.log", "a") as f:
        f.write(oggi+"\n")
    # carico il contesto iniziale
    f = open("config/contesto_iniziale.md", "r")
    contesto = f.read()
    messages = [
        {"role": "system", "content": contesto}
    ]
    # restituisco contesto e configs
    return messages, configs

if __name__ == "__main__":
    messages, configs = inizializza()
    try:
        while True:
            # input
            if configs["ascolta"] == 1:
                comando = ascolta()
            else:
                comando = input("Tu: ")
            # impostazioni
            if comando.startswith("\\"):
                configs, messages = impostazioni(comando, configs, messages)
                continue
            # elaborazione
            if comando:
                messages.append({"role": "user", "content": comando})
                new_message = chiedi_a_gpt(messages, configs)
                if new_message:
                    messages.append(new_message)
                    risposta = new_message["content"]
                    # output
                    print("ROBIN: " + risposta)
                    if configs["parla"] == 1 and len(risposta) < configs["limite-parole"]:
                        parla(risposta, configs)
                    # conclusione
                    aggiorna_log(comando, risposta)
                print("\n")
    except KeyboardInterrupt:
        pass