import pyttsx3

def createVoiceOver(text, filePath):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    rate = engine.getProperty("rate")
    volume = engine.getProperty("volume")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", rate * 1.1)
    engine.setProperty("volume", volume * 1.1)
    engine.save_to_file(text, filePath)
    engine.runAndWait()
