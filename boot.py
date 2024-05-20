# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import os, machine
#os.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
webrepl.start()
import network

gc.collect()

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='TIGO_m3_01',password='12345678', authmode=network.AUTH_WPA_WPA2_PSK)

