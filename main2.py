import time
import os
import board
import digitalio
import audiomp3
import audiopwmio
import adafruit_ili9341
import displayio
import busio
import adafruit_sdcard
import microcontroller
import storage
import fourwire
import random
import gc
sd_cs =board.GP5
sd_spi = busio.SPI(board.GP2, board.GP3, board.GP4)
cs = digitalio.DigitalInOut(sd_cs)
sdcard = adafruit_sdcard.SDCard(sd_spi,cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs,"/sd")

button_pin = board.GP16
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
pir =digitalio.DigitalInOut(board.GP28)
pir.direction = digitalio.Direction.INPUT


audio = audiopwmio.PWMAudioOut(board.GP0)
while True:
    gc.collect()
    print(button.value)
    if not button.value:
        decoder = audiomp3.MP3Decoder(open("/Sunshine.mp3", "rb"))
        audio.play(decoder)
        while audio.playing:
            pass
        time.sleep(5)
        print(gc.mem_free())
    print(pir.value)
    time.sleep(0.1)
    if pir.value:
        rand = random.randint(1,2)
        if rand == 1:
            d_1 = audiomp3.MP3Decoder(open("/sd/1.mp3", "rb"))
            audio.play(d_1)
        elif rand == 2:
            d_2 = audiomp3.MP3Decoder(open("/sd/2.mp3", "rb"))
            audio.play(d_2)
        else:
            d_3 = audiomp3.MP3Decoder(open("/sd/3.mp3", "rb"))
            audio.play(d_3)
        while audio.playing:
            pass
        print(gc.mem_free())