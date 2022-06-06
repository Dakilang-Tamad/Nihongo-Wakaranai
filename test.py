from gtts import gTTS
from pygame import mixer, time

mytext = "日本語上手ですよ俺"

language = 'ja'

myobj = gTTS(text=mytext, lang=language, slow=False)

myobj.save("welcome.mp3")

mixer.init()

mixer.music.load("welcome.mp3")

mixer.music.play()

while mixer.music.get_busy():
    time.wait(100)