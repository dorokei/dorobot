# -*- coding: utf-8 -*-
import webiopi
import time
import wiringpi2 as wiringpi
import os

# import pygame
# import pygame.midi
from time import sleep

import subprocess
import picamera

# camera setting
shutter_numb = 0
home_dir = '/home/pi/photo'

# port setting
#PWM1  = 25
#PWM2  = 24
#PWM3  = 23
#PWM4  = 22
PWM1  = 24
PWM2  = 23
PWM3  = 22
PWM4  = 27
CAMERA_SERVO = 18
TAIL_SERVO = 4


# pokemiku setting
# instrument = 0 # miku
# port = 2 # NSX-39
 
# pygame.init()
# pygame.midi.init()

# for python3
#for id in range(pygame.midi.get_count()):
#	print (id)
#	print (pygame.midi.get_device_info(id))
 
# midiOutput = pygame.midi.Output(port)
# midiOutput.set_instrument(instrument)
 
def getServoDutyForWebIOPi(val):
    val_min = 0.0
    val_max = 1.0
    servo_min = 48
    servo_max = 90

    duty = int((servo_max-servo_min)*(val-val_min)/(val_max-val_min) + servo_min)
    return duty

wiringpi.wiringPiSetupGpio() # GPIO名で番号指定
wiringpi.pinMode(CAMERA_SERVO, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS) # 周波数固定
wiringpi.pwmSetClock(375) # 50 Hz
wiringpi.pwmWrite(CAMERA_SERVO, getServoDutyForWebIOPi(0.5))


# デバッグ出力を有効に
webiopi.setDebug()

# GPIOライブラリの取得
GPIO = webiopi.GPIO

# WebIOPiの起動時に呼ばれる関数
def setup():
    webiopi.debug("Script with macros - Setup")
    # GPIOのセットアップ
    GPIO.setFunction(PWM1, GPIO.PWM)
    GPIO.setFunction(PWM2, GPIO.PWM)
    GPIO.setFunction(PWM3, GPIO.PWM)
    GPIO.setFunction(PWM4, GPIO.PWM)
    GPIO.setFunction(TAIL_SERVO, GPIO.PWM)
    # 初期のデューティー比を0%に（静止状態）
    GPIO.pwmWrite(PWM1, 0)
    GPIO.pwmWrite(PWM2, 0)
    GPIO.pwmWrite(PWM3, 0)
    GPIO.pwmWrite(PWM4, 0)
    GPIO.pwmWrite(TAIL_SERVO, 0)

    # volume setting 7F(Max)
    # midiOutput.write_short(0xB0, 7, 127) 


# WebIOPiにより繰り返される関数
def loop():
    webiopi.sleep(5)        

# WebIOPi終了時に呼ばれる関数
def destroy():
    webiopi.debug("Script with macros - Destroy")
    # GPIO関数のリセット（入力にセットすることで行う）
    GPIO.setFunction(PWM1, GPIO.IN)
    GPIO.setFunction(PWM2, GPIO.IN)
    GPIO.setFunction(PWM3, GPIO.IN)
    GPIO.setFunction(PWM4, GPIO.IN)

# 4つのPWMにデューティー比をまとめてセットするためのマクロ
# commandIDは、iOSのSafariでPOSTがキャッシュされることへの対策
@webiopi.macro
def pwm4Write(duty1, duty2, duty3, duty4, commandID):
    GPIO.pwmWrite(PWM1, float(duty1))
    GPIO.pwmWrite(PWM2, float(duty2))
    GPIO.pwmWrite(PWM3, float(duty3))
    GPIO.pwmWrite(PWM4, float(duty4))

@webiopi.macro
def setHwPWM(duty, commandID):
    wiringpi.pwmWrite(18, getServoDutyForWebIOPi(float(duty)))

"""
@webiopi.macro
def sayHello(tmp):
    # setting lyric by sending SysEx for python3
    midiOutput.write_sys_ex(0, b'\xF0\x43\x79\x09\x11\x0A\x00\x09\x7B\x40\x36\x77\xF7')

    # say hello and action
    midiOutput.note_on(79, 80)
    GPIO.pulseAngle(TAIL_SERVO, 0)
    sleep(.160)
    midiOutput.note_on(79, 80)
    GPIO.pulseAngle(TAIL_SERVO, 40)
    sleep(.200)
    midiOutput.note_on(79, 80)
    sleep(.180)
    midiOutput.note_on(79, 80)
    GPIO.pulseAngle(TAIL_SERVO, -60)
    sleep(.170)
    midiOutput.note_on(79, 80)
    sleep(.400)
    GPIO.pulseAngle(TAIL_SERVO, 20)
    midiOutput.note_off(79,80)
    GPIO.pwmWrite(TAIL_SERVO, 0)


@webiopi.macro
def shutterCamera(tmp):
    # setting lyric by sending SysEx for python3
    midiOutput.write_sys_ex(0, b'\xF0\x43\x79\x09\x11\x0A\x00\x47\x01\x36\x01\x1c\xF7')

    # say hello and action
    midiOutput.note_on(79, 80)
    sleep(.200)
    midiOutput.note_on(79, 80)
    sleep(.200)
    midiOutput.note_on(74, 80)
    sleep(.180)
    midiOutput.note_on(74, 80)
    sleep(.500)
    midiOutput.note_on(79, 80)
    sleep(.300)
    midiOutput.note_off(79,80)

    cmd ="python3 /usr/share/webiopi/htdocs/m2/shutter.py"
    subprocess.call(cmd, shell=True)

    #cmd ="tw 写真撮れたよ〜 --file=/home/pi/photo/capture.jpg --yes"
    #subprocess.call(cmd, shell=True)

@webiopi.macro
def singSong(tmp):

    # setting lyric by sending SysEx
    midiOutput.write_sys_ex(0, b'\xF0\x43\x79\x09\x11\x0A\x00\x00\x70\x43\x64\x64\x43\x25\x4E\x7B\x65\x18\x71\x43\x6E\x04\x04\xF7')
    midiOutput.write_short(0xB0, 0x5B, 0x6F) # reverb

    # sing a song
    midiOutput.note_on(69, 80)
    sleep(.200)
    midiOutput.note_on(71, 80)
    sleep(.200)
    midiOutput.note_on(72, 80)
    sleep(1.00)
    midiOutput.note_off(72, 80)
    sleep(.200)
    midiOutput.note_on(67, 80)
    sleep(.200)
    midiOutput.note_on(67, 80)
    sleep(.200)
    midiOutput.note_on(74, 80)
    sleep(1.00)
    midiOutput.note_off(74, 80)
    sleep(.200)
    midiOutput.note_off(74, 80)
    sleep(.200)
    midiOutput.note_on(72, 80)
    sleep(.200)
    midiOutput.note_on(69, 80)
    sleep(.200)
    midiOutput.note_on(69, 80)
    sleep(.400)
    midiOutput.note_on(69, 80)
    sleep(.200)
    midiOutput.note_on(69, 80)
    sleep(.200)
    midiOutput.note_on(69, 80)
    sleep(.400)
    midiOutput.note_on(71, 80)
    sleep(.400)
    midiOutput.note_on(72, 80)
    sleep(.400)
    midiOutput.note_on(74, 80)
    sleep(.200)
    midiOutput.note_on(72, 80)
    sleep(.400)
    midiOutput.note_off(72,80)
    midiOutput.write_short(0xB0, 0x5B, 0x10)
"""

