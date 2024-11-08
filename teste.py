import win32com.client

# Inicializa o motor de fala
engine = win32com.client.Dispatch("SAPI.SpVoice")

# Obtém a lista de vozes disponíveis
voices = engine.GetVoices()

# Exibe as vozes
for voice in voices:
    print(f"Voice: {voice.GetDescription()}")

# Seleciona uma voz específica (pode ser necessário ajustar conforme a descrição das vozes)
engine.Voice = voices.Item(1)  # Seleciona a primeira voz na lista
engine.Speak("Olá, como você está?")
