from pybricks.iodevices import PUPDevice
from pybricks.pupdevices import Motor, Remote, Light
from pybricks.parameters import Port, Direction, Stop, Button, Color
from pybricks.hubs import TechnicHub
from pybricks.tools import wait
from uerrno import ENODEV


hub = TechnicHub()
hub.light.blink(Color.RED, [200, 200])    
try:        
    remote = Remote(timeout=15000) # Connect to the remote.
    print("Connected!")
    hub.light.on(Color.GREEN)
    remote.light.on(Color.GREEN)
except OSError:
    print("Could not find the remote.")
    hub.light.on(Color.RED)


light_connected = False
try:
    device = PUPDevice(Port.D)
    if device.info()['id'] == 8:
        light_connected = True    
except OSError as ex:
    print("No device on port D") if ex.args[0] == ENODEV else print("Another error occurred.")    

# Initialize the motors.
steer = Motor(Port.C)
front = Motor(Port.A, Direction.COUNTERCLOCKWISE)
rear = Motor(Port.B, Direction.COUNTERCLOCKWISE)

# Lower the acceleration so the car starts and stops realistically.
front.control.limits(acceleration=1000)
rear.control.limits(acceleration=1000)


# Find the steering endpoint on the left and right. The middle is in between.
left_end = steer.run_until_stalled(-200, then=Stop.HOLD)
right_end = steer.run_until_stalled(200, then=Stop.HOLD)
# We are now at the right. Reset this angle to be half the difference. That puts zero in the middle.
steer.reset_angle((right_end - left_end) / 2)
steer.run_target(speed=200, target_angle=0, wait=False)




if light_connected == True:
    light = Light(Port.D)   
    hub.light.on(Color.BLACK)
    remote.light.on(Color.BLACK)
light_on = False


# Now we can start driving!
while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Choose the steer angle based on the left controls.
    steer_angle = 0
    if Button.RIGHT_MINUS in pressed: steer_angle -= 75
    if Button.RIGHT_PLUS in pressed:  steer_angle += 75

    # Steer to the selected angle.
    steer.run_target(500, steer_angle, wait=False)

    # Choose the drive speed based on the right controls.
    drive_speed = 0
    if Button.LEFT_PLUS in pressed:  drive_speed += 1000
    if Button.LEFT_MINUS in pressed: drive_speed -= 1000

    # Apply the selected speed.
    front.run(drive_speed)
    rear.run(drive_speed)

    if light_connected == True and Button.LEFT in pressed:
        light_on = not light_on
        if light_on == True:
            light.on(100)
            hub.light.on(Color.WHITE)
            remote.light.on(Color.WHITE)
        else:
            light.off()
            hub.light.on(Color.BLACK)
            remote.light.on(Color.BLACK)
        wait(100)
    # Wait.
    wait(10)