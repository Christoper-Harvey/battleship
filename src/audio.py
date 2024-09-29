import pygame

pygame.mixer.init()

hit_sound = pygame.mixer.Sound("sound/hit.mp3")
miss_sound = pygame.mixer.Sound("sound/miss.mp3")
sink_sound = pygame.mixer.Sound("sound/sink.mp3")

hit_channel = pygame.mixer.Channel(0)
miss_channel = pygame.mixer.Channel(1)

class Audio:
    @staticmethod
    def play_hit():
        #print("Playing hit sound")
        hit_channel.play(hit_sound)

    @staticmethod
    def play_miss():
        #print("Playing miss sound")
        miss_channel.play(miss_sound)

    def play_sink():
        #print("Playing sink sound")
        hit_channel.play(sink_sound)
