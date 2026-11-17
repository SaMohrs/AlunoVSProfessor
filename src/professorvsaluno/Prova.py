import pygame as pg
from professorvsaluno.Config import *

class Prova(pg.sprite.Sprite):          
    def __init__(self, x, y, velocidade, nota):
        pg.sprite.Sprite.__init__(self)
        self.sprites = []
        
        for i in range(2):
            self.sprites.append(pg.image.load(caminho_recursos(f"Imagens/Provas/Nota_{nota}_{i}.png")))
        
        self.image = self.sprites[0]
        self.delta = 0
        self.image = pg.transform.scale(self.image, (16*4, 16*4))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.velocidade = velocidade
        if nota == "0,5":
            self.nota = 0.5
        elif nota == "1":
            self.nota = 1
        else:
            self.nota = 2
        
        self.pos_y = float(self.rect.y)
        
    def update(self):
        self.delta += 0.10
        self.image = self.sprites[int(self.delta)]
        self.image = pg.transform.scale(self.image, (16*4, 16*4))
        self.pos_y += self.velocidade
        self.rect.y = int(self.pos_y)
        
        if self.delta > 1.9:
            self.delta = 0