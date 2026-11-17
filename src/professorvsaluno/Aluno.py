import pygame as pg
from pygame.locals import *

from professorvsaluno.Config import *

class Aluno(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sprites = []
        
        for i in range(9):
            self.sprites.append(pg.image.load(caminho_recursos(f"Imagens/Aluno/Aluno_{i}.png")))

        self.atual = 0
        self.d = 1
        self.e = 5

        self.image = self.sprites[self.atual]
        self.image = pg.transform.scale(self.image, (32*4, 32*4))
        self.rect = self.image.get_rect()
        self.rect.topleft = (LARGURA_VIRTUAL/2) - 64, ALTURA_VIRTUAL - 188
        
        self.sombra = pg.Surface((64, 16), pg.SRCALPHA)
        pg.draw.ellipse(self.sombra, (0, 0, 10, 55), (0, 0, 22, 6))
        self.sombra = pg.transform.scale(self.sombra, (256, 64))

    def andar(self, direcao):
        
        if direcao == "D":

            self.d += 0.20
            
            self.image = self.sprites[int(self.d)]
            if self.rect.x < LARGURA_VIRTUAL - 428:
                self.rect.x += 10
                
            if self.d > 4.80:
                self.d = 1

        if direcao == "E":

            self.e += 0.20
            
            self.image = self.sprites[int(self.e)]
            if self.rect.x > 300:
                self.rect.x -= 10
                
            if self.e > 8.80:
                self.e = 5
            
        self.image = pg.transform.scale(self.image, (32*4, 32*4))