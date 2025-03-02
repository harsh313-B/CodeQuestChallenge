import pygame
import os

def load_sounds():
    sounds = {}
    try:
        pygame.mixer.init()

        # Create a simple sound using wav format
        duration = 100  # milliseconds
        sample_rate = 44100
        bits = -16

        # Create a simple beep sound
        sound_array = bytearray()
        for i in range(int(duration * sample_rate / 1000)):
            sound_array.append(128 if i % 2 == 0 else 0)

        sound_buffer = pygame.mixer.Sound(buffer=bytes(sound_array))
        sounds['click'] = sound_buffer
    except:
        # If sound initialization fails, create a dummy sound object
        class DummySound:
            def play(self): pass
        sounds['click'] = DummySound()

    return sounds