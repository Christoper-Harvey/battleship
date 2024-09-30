import pygame

pygame.mixer.init()

hit_sound = pygame.mixer.Sound("sound/hit.mp3")
miss_sound = pygame.mixer.Sound("sound/miss.mp3")
sink_sound = pygame.mixer.Sound("sound/sink.mp3")
pickup_sound = pygame.mixer.Sound("sound/pickup.mp3")
use_sound = pygame.mixer.Sound("sound/use.mp3")
error_sound = pygame.mixer.Sound("sound/error.mp3")

hit_channel = pygame.mixer.Channel(0)
miss_channel = pygame.mixer.Channel(1)
powerup_channel = pygame.mixer.Channel(2)
error_channel = pygame.mixer.Channel(3)

class Audio:
    @staticmethod
    def play_hit():
        hit_channel.play(hit_sound)

    @staticmethod
    def play_miss():
        miss_channel.play(miss_sound)

    def play_sink():
        hit_channel.play(sink_sound)

    @staticmethod 
    def play_pickup():
        powerup_channel.play(pickup_sound)

    def play_use():
        powerup_channel.play(use_sound)
    
    @staticmethod
    def play_error():
        error_channel.play(error_sound)
        