from datetime import datetime
import RPi.GPIO as GPIO
import socket

# Pin number constants
FORWARD_LEFT_PIN = 17
FORWARD_RIGHT_PIN = 27
BACKWARD_LEFT_PIN = 23
BACKWARD_RIGHT_PIN = 24

conn_info = "", 50002


def log(msg) -> None:
    """
    Write to log file with current time
    :param msg: Message to log
    """
    with open("log.txt", 'a') as log_file:
        log_file.write(f"[{datetime.now().strftime('%H:%M')}] {msg}")


def set_pin(pin: int, high: bool = True) -> None:
    """
    Sets pin to given value. Default High.
    :param pin: Pin to set
    :param high: Set to high?
    """
    if high:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)


def set_left(value: bool = True) -> None:
    """
    Set left
    :param value: Value to set
    """
    set_pin(FORWARD_LEFT_PIN, value)


def set_right(value: bool = True) -> None:
    """
    Set right
    :param value: Value to set
    """
    set_pin(FORWARD_RIGHT_PIN, value)


def set_forward(value: bool = True) -> None:
    """
    Set forward
    :param value: Value to set
    """
    set_pin(FORWARD_LEFT_PIN, value)
    set_pin(FORWARD_RIGHT_PIN, value)


def set_backward(value: bool = True) -> None:
    """
    Set backward
    :param value: Value to set
    """
    set_pin(BACKWARD_LEFT_PIN, value)
    set_pin(BACKWARD_RIGHT_PIN, value)


def init_GPIO() -> None:
    """
    Initialize GPIO pins.
    :return: None
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FORWARD_LEFT_PIN, GPIO.OUT)
    GPIO.setup(FORWARD_RIGHT_PIN, GPIO.OUT)
    GPIO.setup(BACKWARD_LEFT_PIN, GPIO.OUT)
    GPIO.setup(BACKWARD_RIGHT_PIN, GPIO.OUT)


def run() -> None:
    """
    Wait for messages from sockets, and execute accordingly.
    """
    init_GPIO()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(conn_info)

    while True:
        msg = s.recv(2)
        log(f"Received {msg}")
        direction, value = msg.decode("utf-8")

        if direction in bindings:
            bindings[direction](value)
        else:
            s.send(bytes("?"))


# Bindings from socket messages to functions
bindings = {
    'f': set_forward,
    'b': set_backward,
    'l': set_left,
    'r': set_right,
}
run()
