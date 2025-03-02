import pygame
import os

def load_sounds():
    sounds = {}
    pygame.mixer.init()
    
    # Create button click sound using pygame's built-in sound synthesis
    duration = 100  # milliseconds
    frequency = 1000  # Hz
    sample_rate = 44100
    bits = -16
    
    # Generate a simple "click" sound
    num_samples = int(duration * sample_rate / 1000)
    sound_buffer = pygame.sndarray.make_sound(
        pygame.sndarray.array([4096 * pygame.math.sine(2.0 * 3.14159 * frequency * x / sample_rate)
                             for x in range(num_samples)]))
    
    sounds['click'] = sound_buffer
    return sounds
