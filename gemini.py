import google.generativeai as genai
import os
import dotenv
import whisper
import warnings
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
from time import sleep
from gtts import gTTS
from playsound import playsound

warnings.filterwarnings("ignore")
dotenv.load_dotenv()

#Tranformando audio em texto

fs = 44100 
seconds = 5  


print("Gravando...")
audio_data = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()
print("Gravação finalizada.")

wav_file = "meu_audio.wav"
write(wav_file, fs, audio_data)

mp3_file = "meu_audio.mp3"
audio = AudioSegment.from_wav(wav_file)
audio.export(mp3_file, format="mp3")

sleep(5)

audio = "meu_audio.mp3"

model = whisper.load_model("base")
result = model.transcribe(audio)
resultado = (result["text"])

with open('log.txt', 'a') as log_file:  
    log_file.write(f'Pergunta:{resultado}' + '\n')  # Log da pergunta

# API do Gemini

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content(f'{resultado} mas em formato de texto sem nada de formatção como bold, *, nem nada, só a resposta ')
with open('log.txt', 'a') as log_file:  
    log_file.write(f'Resposta: {response.text}' + '\n')  # Log da resposta
texto = response.text

#Tranformando texto em audio

tts = gTTS(text=texto, lang='pt', slow=False)

arquivo_mp3 = "texto_para_audio.mp3"
tts.save(arquivo_mp3)

print(f"Arquivo de áudio salvo como '{arquivo_mp3}'.")

sleep(3)
playsound(arquivo_mp3)