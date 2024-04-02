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

#button
button_pin = board.GP16
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
'''
#motion detector
pir =digitalio.DigitalInOut(board.GP1)
pir.direction = digitalio.Direction.INPUT

#speaker

audio = audiopwmio.PWMAudioOut(board.GP0)
decoder = audiomp3.MP3Decoder(open("/sd/Sunshine.mp3", "rb"))
'''
#tft display
mosi_pin, clk_pin, reset_pin, cs_pin, dc_pin = board.GP15, board.GP14, board.GP7, board.GP17, board.GP6
displayio.release_displays()
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
display_bus = fourwire.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)
display = adafruit_ili9341.ILI9341(display_bus, width=240, height=320, rotation=270)
bitmap = displayio.OnDiskBitmap("/Rainbow.bmp")
group = displayio.Group()
display.root_group = group
while True:
    if not button.value:
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        group.append(tile_grid)
        time.sleep(8)
    else:
        print("No press down")
        time.sleep(0.1)
'''
button_pin = board.GP10
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.Input
button.pull = digitalio.Pull.Up
    if not button.value: -> meaning button is press

# motion detector
pir = digitalio.DigitalInOut(board.GP__)
pir.direction = digitalio.Direction.INPUT
    if pir.value: ==true if there is movement, false if no movement
# speaker
audio = audiopwmio.PWMAudioOut(board.GP0__)
decoder = audiomp3.MP3Decoder(open("___", "rb"))
audio.play(decoder) #play function
    audio.playing ->true if song is continue false if not
# tft display
mosi_pin, clk_pin, reset_pin, cs_pin, dc_pin = board.GP11, board.GP10, board.GP17, board.GP18, board.GP16
displayio.release_displays()

spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)

display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

display = adafruit_ili9341.ILI9341(display_bus, width=240, height=320, rotation=270)

bitmap = displayio.OnDiskBitmap("/0.bmp")
bitmap1 = displayio.OnDiskBitmap("/1.bmp")
bitmap2 = displayio.OnDiskBitmap("/2.bmp")
group = displayio.Group()
display.show(group)

while True:
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    group.append(tile_grid)
    sleep(8)
    tile_grid = displayio.TileGrid(bitmap1, pixel_shader=bitmap1.pixel_shader)
    group.append(tile_grid)
    sleep(8)
    tile_grid = displayio.TileGrid(bitmap2, pixel_shader=bitmap2.pixel_shader)
    group.pop()
    group.append(tile_grid)
    sleep(8)
# sd card reader
sd_cs =board.GP__
sd_spi = busio.SPI(board.GP10, board.GP11, board.GP12)
cs = digitalio.DigitalInOut(sd_cs)
sdcard = adafruit_sdcard.SDCard(sd_spi,cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs,"/sd")
def print_directory(path, tabs=0):
    for file in os.listdir(path):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000

        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)

        prettyprintname = ""
        for _ in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

        # recursively print directory contents
        if isdir:
            print_directory(path + "/" + file, tabs + 1)


print("Files on filesystem:")
print("====================")
print_directory("/sd")

'''