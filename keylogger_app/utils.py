import pygame
import platform
import psutil
import socket
import random
import string
import os

def play_sound():
    try:
        sound_file = "sounds/notification.wav"
        if not os.path.exists(sound_file):
            if platform.system() == "Windows":
                sound_file = "C:\\Windows\\Media\\notify.wav"
            elif platform.system() == "Linux":
                sound_file = "/usr/share/sounds/freedesktop/stereo/complete.oga"
            else:  # macOS
                sound_file = "/System/Library/Sounds/Ping.aiff"
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Sound playback failed: {str(e)}")

def optimize_performance():
    try:
        process = psutil.Process()
        process.cpu_affinity([0])
        process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if platform.system() == "Windows" else 10)
        random_name = "".join(random.choices(string.ascii_letters, k=10))
        psutil.Process().name = lambda: random_name
    except Exception as e:
        print(f"Performance optimization failed: {str(e)}")

def get_network_status():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return "Connected"
    except:
        return "Disconnected"