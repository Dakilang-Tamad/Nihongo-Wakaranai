from gtts import gTTS
from pygame import mixer, time
from jnius import autoclass

mytext = "日本語上手ですよ俺"

language = 'ja'

myobj = gTTS(text=mytext, lang=language, slow=False)

myobj.save("welcome.mp3")

mixer.init()

mixer.music.load("welcome.mp3")

mixer.music.play()

while mixer.music.get_busy():
    time.wait(100)

def to_audio():
    language = 'ja'
    speech = dh.tts
    myobj = gTTS(text=speech, lang=language, slow=False)
    myobj.save("tts.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("tts.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
    pygame.mixer.music.unload()


    PythonActivity = autoclass('org.renpy.android.PythonActivity')
    activity = PythonActivity.mActivity
    tts = autoclass('android.speech.tts')
    texttospeech = activity.getSystemService(tts.TextToSpeech)

    texttospeech.setLanguage(Locale.JAPAN)
    texttospeech.addSpeech("日本語分からない", "JP.mp3")