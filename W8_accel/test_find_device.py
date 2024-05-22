import machine
i2c = machine.SoftI2C(scl=machine.Pin(14), sda=machine.Pin(4)) #for SocBot
#i2c = machine.SoftI2C(scl=machine.Pin(18), sda=machine.Pin(19)) #for TigoRoverBox

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))