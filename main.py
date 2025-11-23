import sys
import termios
import tty
import os

def getch():
    """Read a single character from stdin without Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    print("Press LEFT or RIGHT arrow keys. Press 'q' to quit.")
    print("Left arrow → runs: accelerate command")
    print("Right arrow → runs: brake command")

    while True:
        key = getch()

        if key == 'q':
            print("\nExiting...")
            break

        # Arrow keys send 3-byte sequences: \x1b [ A/B/C/D
        if key == '\x1b':  # ESC
            key += getch()
            if key == '\x1b[':
                key += getch()
                if key == '\x1b[A':
                    print("↑ Up arrow (ignored)")
                elif key == '\x1b[B':
                    print("↓ Down arrow (ignored)")
                elif key == '\x1b[C':
                    print("➡️ Right arrow pressed → Brake!")
                    os.system("adb shell input swipe 2115 850 2200 850 150")  # <-- YOUR ACCEL CMD
                elif key == '\x1b[D':
                    print("⬅️ Left arrow pressed → Accelerate!")
                    os.system("adb shell input swipe 200 850 240 850 150")  # <-- YOUR BRAKE CMD

if __name__ == "__main__":
    main()
