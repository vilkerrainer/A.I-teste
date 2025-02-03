import os
import dotenv
import sounddevice as sd
from scipy.io.wavfile import write
from time import sleep
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound


dotenv.load_dotenv()
recognizer = sr.Recognizer()

def main():
    try:
        # Gravar áudio
        print("Gravando...")
        fs = 44100
        audio_data = sd.rec(int(5 * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        write("meu_audio.wav", fs, audio_data)
        print("Gravação finalizada.")

        # Transcrever áudio
        sleep(2)
        with sr.AudioFile("meu_audio.wav") as source:
            audio = recognizer.record(source)
        pergunta = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Pergunta: {pergunta}")

        # Gerar resposta com Gemini
        import google.generativeai as genai
        genai.configure(api_key=os.environ["API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        with open('prompt.txt', 'r', encoding='utf-8') as f:
            prompt = f.read()
        resposta = model.generate_content(f'{prompt} {pergunta}').text
        print(f"Resposta: {resposta}")
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(f'Pergunta: {pergunta} \nResposta: {resposta}')
            

        # Converter resposta em áudio e reproduzir
        tts = gTTS(text=resposta, lang='pt', slow=False)
        tts.save("resposta.mp3")
        playsound("resposta.mp3")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")