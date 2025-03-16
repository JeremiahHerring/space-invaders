import pygame as pg 
import time
import numpy as np

class Sound:
    def __init__(self): 
        self.pickup = pg.mixer.Sound('sounds/pickup.wav')
        self.gameover = pg.mixer.Sound('sounds/gameover.wav')
        self.bg = pg.mixer.Sound('sounds/ride_of_the_valkyries.mp3')
        pg.mixer.music.set_volume(0.2)
        self.music_playing = False
        self.bg_playing = False  # Track if the background music is already playing
                                             
    def play_background(self, speed=1.0):
        if not self.bg_playing:
            self.music_playing = True
            self.current_bg = self.adjust_speed(self.bg, speed)  # Store reference
            if self.current_bg:
                self.current_bg.play(-1)  # Loop indefinitely
                self.bg_playing = True


        
    def play_pickup(self): 
        if self.music_playing: 
            self.pickup.play()
        

    def play_gameover(self):
        # First ensure background is stopped properly
        pg.mixer.stop()  # Stop all sound channels
        self.bg_playing = False
        self.music_playing = False
        
        # Then play game over sound
        self.gameover.play()
        
    def toggle_background(self):
        if self.music_playing: 
            self.stop_background()
        else:
            self.play_background()
        self.music_playing = not self.music_playing
        
    def stop_background(self): 
        pg.mixer.music.stop()
        self.music_playing = False
        self.bg_playing = False  # Reset background music flag

    def adjust_speed(self, sound, speed=1.0):
        """Adjust the speed of a sound by manipulating samples."""
        array = pg.sndarray.array(sound)  # Convert sound to NumPy array
        
        # Speed up: take every nth sample (downsampling)
        indices = np.round(np.arange(0, len(array), speed)).astype(int)
        indices = indices[indices < len(array)]  # Ensure indices stay in range
        
        new_array = array[indices]  # Apply speed change
        new_sound = pg.sndarray.make_sound(new_array)  # Convert back to Sound object
        
        return new_sound
