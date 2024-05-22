from machine import I2C, Pin
import time
# LIS2DH12 device address
LIS2DH12_ADDRESS = 0x19

# LIS2DH12 register addresses
LIS2DH12_WHO_AM_I = 0x0F
LIS2DH12_CTRL_REG1 = 0x20
LIS2DH12_OUT_X_L = 0x28

# Initialize I2C bus
i2c = I2C(scl=Pin(14), sda=Pin(4))

# Check if LIS2DH12 is connected
def detect_LIS2DH12():
    devices = i2c.scan()
    return LIS2DH12_ADDRESS in devices

def read_acceleration():
    # Read WHO_AM_I register to verify communication with the sensor
    who_am_i = i2c.readfrom_mem(LIS2DH12_ADDRESS, LIS2DH12_WHO_AM_I, 1)[0]
    if who_am_i == 0x33:  # Check if WHO_AM_I value matches expected value
        # Configure CTRL_REG1 to enable the sensor
        i2c.writeto_mem(LIS2DH12_ADDRESS, LIS2DH12_CTRL_REG1, b'\x47')
        time.sleep_ms(100)  # Allow some time for sensor to stabilize

        # Read acceleration data from X-axis
        x_acc_bytes = i2c.readfrom_mem(LIS2DH12_ADDRESS, LIS2DH12_OUT_X_L | 0x80, 2)
        x_acc = (x_acc_bytes[1] << 8) | x_acc_bytes[0]  # Combine low and high bytes for X-axis acceleration
        # Convert raw data to acceleration in g (assuming full-scale range of +/-2g)
        acceleration_x = x_acc / 16384.0
        return acceleration_x
    else:
        return None

# Main code
if detect_LIS2DH12():
    while True:
        acceleration_x = read_acceleration()
        if acceleration_x is not None:
            print("Acceleration X:", acceleration_x)
        else:
            print("Error: Unable to communicate with LIS2DH12")
        time.sleep(1)  # Delay before next reading
else:
    print("LIS2DH12 not found")
