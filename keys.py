
from sshkeyboard import listen_keyboard
def press(key):
    if key == "up":
        print("up pressed")
    elif key == "down":
        print("down pressed")
    elif key == "left":
        print("left pressed")
    elif key == "right":
        print("right pressed")

res = listen_keyboard(on_press=press)