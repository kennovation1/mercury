# Fix this by converting mp3 to ogg first?
# I don't think current version of pygame supports mp3
import pygame

pygame.mixer.init()
pygame.mixer.music.load("./mps3/example.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy() == True:
        pass
