import pygame as pg
from pygame.locals import *

from professorvsaluno.Config import *

class Professor(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sprites = []

        for i in range(7):
            self.sprites.append(pg.image.load(caminho_recursos(f"Imagens/Professor/Prof_{i}.png")))

        self.atual = 0
        self.d = 1
        self.e = 3

        self.image = self.sprites[self.atual]
        self.image = pg.transform.scale(self.image, (32*4, 32*4))
        self.rect = self.image.get_rect()
        self.rect.topleft = (LARGURA_VIRTUAL/2) - 64, 304
        
        self.sombra = pg.Surface((64, 16), pg.SRCALPHA)
        pg.draw.ellipse(self.sombra, (0, 0, 10, 55), (0, 0, 22, 6))
        self.sombra = pg.transform.scale(self.sombra, (256, 64))
        
        self.ultima_direção = 0
        self.intervalo_troca = 600
        self.direcao = "P"
        
        # Controle de tempo para os tiros
        self.ultimo_tiro = 0
        self.intervalo_tiro = 2000
        
        self.atacando = False
        self.inicio_ataque = 0
        self.duracao_ataque = 200