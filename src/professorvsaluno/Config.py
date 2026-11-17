import pygame as pg
import sys
import os

def caminho_recursos(caminho_relativo):
    try:
        caminho_base = sys._MEIPASS
    except AttributeError:
        caminho_base = os.path.abspath(".")

    return os.path.join(caminho_base, caminho_relativo)

pg.init()

# 1. Resolução INTERNA do jogo (lógica, posições e velocidades continuam em 1500x1000)
LARGURA_VIRTUAL = 1500
ALTURA_VIRTUAL = 1000

# Pega a resolução real da tela do notebook
info_tela = pg.display.Info()
LARGURA_MONITOR = info_tela.current_w
ALTURA_MONITOR = info_tela.current_h

# Calcula o tamanho do jogo para ocupar 100% da ALTURA da tela mantendo a proporção (15:10)
ALTURA_JOGO = ALTURA_MONITOR
LARGURA_JOGO = int(ALTURA_JOGO * (LARGURA_VIRTUAL / ALTURA_VIRTUAL))

# Se a largura proporcional ultrapassar a largura do monitor, ajusta pela largura
if LARGURA_JOGO > LARGURA_MONITOR:
    LARGURA_JOGO = LARGURA_MONITOR
    ALTURA_JOGO = int(LARGURA_JOGO * (ALTURA_VIRTUAL / LARGURA_VIRTUAL))

# Posição X e Y para centralizar o jogo na tela (gerando as barras pretas laterais/superiores)
POS_X = (LARGURA_MONITOR - LARGURA_JOGO) // 2
POS_Y = (ALTURA_MONITOR - ALTURA_JOGO) // 2

# Configuração do Display em Tela Cheia (FULLSCREEN) e Superfície Virtual
tela = pg.display.set_mode((LARGURA_MONITOR, ALTURA_MONITOR), pg.FULLSCREEN)
superficie_jogo = pg.Surface((LARGURA_VIRTUAL, ALTURA_VIRTUAL))

pg.display.set_caption("Aluno VS Professor 2.0")

relogio = pg.time.Clock()

fps = 60

fundo = pg.image.load(caminho_recursos("Imagens/Outros/background.png")).convert()
fundo = pg.transform.scale(fundo, (LARGURA_VIRTUAL, ALTURA_VIRTUAL))

capa = pg.image.load(caminho_recursos("Imagens/Outros/capa.png")).convert()
capa = pg.transform.scale(capa, (LARGURA_VIRTUAL, ALTURA_VIRTUAL))