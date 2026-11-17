import pygame as pg
from professorvsaluno.Config import *

class Status(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.vidas = 3
        self.notas = 0
        self.fim_de_jogo = False
        
        self.sprites = []
        
        for i in range(4):
            self.sprites.append(pg.image.load(caminho_recursos(f"Imagens/Outros/Coracao_{i}.png")))
            
        self.image = self.sprites[self.vidas]
        
        self.image = pg.transform.scale(self.image, (24*4, 8*4))
        self.rect = self.image.get_rect(center=(LARGURA_VIRTUAL//2, 70))
        
        self.fonte_score = pg.font.Font(caminho_recursos("Fonte/PressStart2P-Regular.ttf"), 24)
        self.fonte_END = pg.font.Font(caminho_recursos("Fonte/PressStart2P-Regular.ttf"), 48)
        
    def mostrarVida(self):
        self.image = self.sprites[self.vidas]
        self.image = pg.transform.scale(self.image, (24*4, 8*4))