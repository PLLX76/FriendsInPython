import speech_recognition as sr
import pyttsx3 as ttx
import os
import datetime
import BlaguesApi
import openai

engine=ttx.init()

voice=engine.getProperty('voices')

engine.setProperty('voice','french')
engine.setProperty("volume", 1)

blagues = BlaguesApi.Jokes("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiODExOTc4NTY5NTA4NTg1NDkzIiwibGltaXQiOjEwMCwia2V5IjoiZUpWWEdldVpKY210Z3JhYjduUjFHRGFiQW9xY2gwT0VVTG0yOXlCTWdhWHBnUTNhbFoiLCJjcmVhdGVkX2F0IjoiMjAyMi0xMC0wN1QxOTowODo0NSswMDowMCIsImlhdCI6MTY2NTE2OTcyNX0.OXaRwmR_wEVOpq8pwls50emJGSjItVVaN4mEDyQOWgY")
openai.api_key = "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"

class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name: str = name
    def speech_to_text(self):
        r = sr.Recognizer()

        micro = sr.Microphone()
        try:
            with micro as source:
                print("Parler...")
                audio_data = r.listen(source)
            self.text = ""
            self.text = r.recognize_google(audio_data, language="fr-FR")
            print ("Me  --> ", self.text)
        except:
            print("Me  -->  erreur")
            
    @staticmethod
    def text_to_speech(text):
        print("Dave --> ", text)
        
        engine.say(text)
        engine.runAndWait()

    def wake_up(self, text):
        return True if self.name in text.lower() else False
    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')
    
if __name__ == "__main__":
    debug = True
    
    ai = ChatBot(name="Dave")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    ex=True
    
    prompt = ""
    
    while ex:
        ai.speech_to_text()
        
        if "fermer" in ai.text:
            ex = False
        if ai.text != "":
            prompt += "\nHumain:" + ai.text + "\nAI:"

            #Ce qui suit est une conversation avec Dave. Dave est serviable, créatif, intelligent et très sympathique
            
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt="Ce qui suit est une conversation entre toi et quelqu'un dont tu ignore le nom. Tu es serviable, créatif, intelligent et très sympathique. Ton nom est Dave.\n\n"+prompt,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=["Humain:", " AI:"]
            )

            if "Human" in response["choices"][0]["text"]:
                pass
            else:
              ai.text_to_speech(response["choices"][0]["text"]) 
              prompt += response["choices"][0]["text"]
    print("----- Closing down Dev -----")