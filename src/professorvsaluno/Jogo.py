import pygame as pg
from pygame.locals import *
import sys
import random

from professorvsaluno.Config import *
from professorvsaluno.Aluno import Aluno
from professorvsaluno.Professor import Professor
from professorvsaluno.Prova import Prova
from professorvsaluno.Status import Status

class Jogo:

    def __init__(self):
        pg.init()
                        
        self.todas_sprites = pg.sprite.Group()
        self.provas = pg.sprite.Group()
        self.estado = Status()
        self.aluno = Aluno()
        self.prof = Professor()

        self.todas_sprites.add(self.aluno, self.prof, self.estado)
        
    def Reiniciar(self):
        # Limpa os grupos de sprites
        self.todas_sprites.empty()
        self.provas.empty()

        # Recria todos os objetos
        self.estado = Status()
        self.aluno = Aluno()
        self.prof = Professor()

        # Adiciona os novos objetos ao grupo
        self.todas_sprites.add(self.aluno, self.prof, self.estado)
    
    def Jogar(self):
        
        while True:
            
            Menu = True
            
            while Menu:
                for event in pg.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pg.quit()
                        sys.exit()

                    if event.type == KEYDOWN and event.key in (K_RETURN, K_KP_ENTER):
                        Menu = False
                
                delta = 0 #Responsável por variar a velocidade dos ataques com o tempo
                
                # Desenha a capa na superfície virtual (1500x1000)
                superficie_jogo.blit(capa, (0, 0))
                MENSAGEM = self.estado.fonte_END.render("PROFESSOR VS ALUNO 2.0", False, (5, 5, 10))
                MENSAGEM_rect = MENSAGEM.get_rect(center=(LARGURA_VIRTUAL // 2, 180))
                
                texto = self.estado.fonte_score.render("Enter para Jogar...", False, (5, 5, 10))
                texto_rect = texto.get_rect(center=(LARGURA_VIRTUAL // 2, ALTURA_VIRTUAL // 2 + 350))
                
                texto2 = self.estado.fonte_score.render("Esc para Sair", False, (55, 55, 55))
                texto2_rect = texto2.get_rect(center=(LARGURA_VIRTUAL // 2, ALTURA_VIRTUAL // 2 + 400))
                
                superficie_jogo.blit(MENSAGEM, MENSAGEM_rect)
                superficie_jogo.blit(texto, texto_rect)
                superficie_jogo.blit(texto2, texto2_rect)

                tela.fill((0, 0, 0))
                jogo_escalado = pg.transform.scale(superficie_jogo, (LARGURA_JOGO, ALTURA_JOGO))
                tela.blit(jogo_escalado, (POS_X, POS_Y))

                pg.display.flip()
            
            tempo_atual = pg.time.get_ticks()
            self.prof.ultimo_tiro = tempo_atual
            self.prof.ultima_direção = tempo_atual
            
            while not self.estado.fim_de_jogo:
                
                
                # Desenha o fundo na superfície virtual (1500x1000)
                superficie_jogo.blit(fundo, (0, 0))
                
                enable = True #Caso seja False, vai direto para o menu, sem ativar as telas de Fim de Jogo
                
                for event in pg.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        self.estado.fim_de_jogo = True
                        enable = False

                # Movimentação Aluno
                teclas = pg.key.get_pressed()

                if teclas[pg.K_RIGHT] or teclas[pg.K_d]:
                    self.aluno.andar("D")
                if teclas[pg.K_LEFT] or teclas[pg.K_a]:
                    self.aluno.andar("E")
                if (not teclas[pg.K_RIGHT] and not teclas[pg.K_d]
                 and not teclas[pg.K_LEFT] and not teclas[pg.K_a]):
                    self.aluno.image = self.aluno.sprites[0]
                    self.aluno.image = pg.transform.scale(self.aluno.image, (32*4, 32*4))
                if ((teclas[pg.K_RIGHT] or teclas[pg.K_d])
                 and (teclas[pg.K_LEFT] or teclas[pg.K_a])):
                    self.aluno.image = self.aluno.sprites[0]
                    self.aluno.image = pg.transform.scale(self.aluno.image, (32*4, 32*4))
                
                # Movimentação Professor
                tempo_atual = pg.time.get_ticks()
                
                if tempo_atual - self.prof.ultima_direção > self.prof.intervalo_troca:
                    self.prof.ultima_direção = tempo_atual
                    self.prof.intervalo_troca = random.randint(600, 1800)
                    
                    self.prof.direcao = random.choice(["D", "P", "E", "D", "E"])
                                    
                if self.prof.direcao == "D":
                    self.prof.d += 0.10
                    self.prof.image = self.prof.sprites[int(self.prof.d)]
                    if self.prof.rect.x < LARGURA_VIRTUAL - 428:
                        self.prof.rect.x += 5
                    else:
                        self.prof.image = self.prof.sprites[0]
                        self.prof.direcao = "E"
                        
                    if self.prof.d > 1.90:
                        self.prof.d = 0

                if self.prof.direcao == "E":
                    self.prof.e += 0.10
                    self.prof.image = self.prof.sprites[int(self.prof.e)]
                    if self.prof.rect.x > 300:
                        self.prof.rect.x -= 5
                    else:
                        self.prof.image = self.prof.sprites[0]
                        self.prof.direcao = "D"
                        
                    if self.prof.e > 3.90:
                        self.prof.e = 2
                    
                if self.prof.direcao == "P":
                    self.prof.image = self.prof.sprites[0]
                        
                self.prof.image = pg.transform.scale(self.prof.image, (32*4, 32*4))
                
                # Ataque do Professor
                tempo_atual = pg.time.get_ticks()

                if tempo_atual - self.prof.ultimo_tiro > self.prof.intervalo_tiro:
                    self.prof.ultimo_tiro = tempo_atual
                    self.prof.intervalo_tiro = random.randint(600, 1600)

                    delta += 0.0015
                    
                    velocidade = random.choice([1, 3, 6, 8]) * (1+ delta)
                    nota = random.choice(["0,5","1","2"])

                    prova = Prova(self.prof.rect.centerx, self.prof.rect.bottom, velocidade, nota)
                    self.todas_sprites.add(prova)
                    self.provas.add(prova)

                    self.prof.atacando = True
                    self.prof.inicio_ataque = tempo_atual
                
                #Ataque Parado    
                if self.prof.atacando and self.prof.direcao == "P":
                    if tempo_atual - self.prof.inicio_ataque < self.prof.duracao_ataque:
                        self.prof.image = self.prof.sprites[4]
                    else:
                        self.prof.atacando = False
                #Ataque Direita
                if self.prof.atacando and self.prof.direcao == "D":
                    if tempo_atual - self.prof.inicio_ataque < self.prof.duracao_ataque:
                        self.prof.image = self.prof.sprites[5]
                    else:
                        self.prof.atacando = False
                #Ataque Esquerda        
                if self.prof.atacando and self.prof.direcao == "E":
                    if tempo_atual - self.prof.inicio_ataque < self.prof.duracao_ataque:
                        self.prof.image = self.prof.sprites[6]
                    else:
                        self.prof.atacando = False

                self.prof.image = pg.transform.scale(self.prof.image, (32*4, 32*4))
                
                # Sombras
                pos_sombraAluno_x = self.aluno.rect.centerx - 32
                pos_sombraAluno_y = self.aluno.rect.bottom - 6
                pos_sombraProf_x  = self.prof.rect.centerx - 32
                pos_sombraProf_y  = self.prof.rect.bottom - 6

                superficie_jogo.blit(self.aluno.sombra, (pos_sombraAluno_x, pos_sombraAluno_y))
                superficie_jogo.blit(self.prof.sombra, (pos_sombraProf_x, pos_sombraProf_y))

                if not self.estado.fim_de_jogo:
                    self.todas_sprites.update()

                    colisoes = pg.sprite.spritecollide(self.aluno, self.provas, True)
                    for prova in colisoes:
                        self.estado.notas += prova.nota
                    
                    for prova in self.provas:
                        if prova.rect.top >= ALTURA_VIRTUAL:
                            prova.kill()
                            self.estado.vidas -= 1
                            self.estado.notas -= prova.nota
                            self.estado.mostrarVida()

                    if self.estado.vidas <= 0 or self.estado.notas >= 100:
                        self.estado.fim_de_jogo = True
                        
                self.todas_sprites.draw(superficie_jogo)
                
                texto_notas = self.estado.fonte_score.render(f"Notas", True, (5, 5, 10))
                texto_notas_rect = texto_notas.get_rect(center=(LARGURA_VIRTUAL // 2, 140))
                N_notas = self.estado.fonte_score.render(f"{self.estado.notas}/100", True, (5, 5, 10))
                N_notas_rect = N_notas.get_rect(center=(LARGURA_VIRTUAL // 2, 180))
                
                superficie_jogo.blit(texto_notas, texto_notas_rect)
                superficie_jogo.blit(N_notas, N_notas_rect)
                
                # Renderização na Janela Real com Letterboxing (Barras Pretas Lateral/Superior)
                tela.fill((0, 0, 0)) # Fundo preto total da tela
                jogo_escalado = pg.transform.scale(superficie_jogo, (LARGURA_JOGO, ALTURA_JOGO))
                tela.blit(jogo_escalado, (POS_X, POS_Y)) # Desenha o jogo centralizado
                
                relogio.tick(fps)
                pg.display.flip()

            # --- TELA DE GAME OVER / VITÓRIA ---
            if self.estado.vidas <= 0:
                mensagem = "GAME OVER"
                cor = (255, 0, 0)
            else:
                mensagem = "VICTORY!"
                cor = (0, 255, 0)

            if enable:
                Voltar = False
            else:
                Voltar = True
            
            while not Voltar:
                for event in pg.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pg.quit()
                        sys.exit()

                    if event.type == KEYDOWN and event.key in (K_RETURN, K_KP_ENTER):
                        Voltar = True
                        self.estado.fim_de_jogo = False
                    
                superficie_jogo.fill((0, 0, 0))
                MENSAGEM = self.estado.fonte_END.render(mensagem, False, cor)
                MENSAGEM_rect = MENSAGEM.get_rect(center=(LARGURA_VIRTUAL // 2, ALTURA_VIRTUAL // 2))
                
                if mensagem == "GAME OVER":
                    Nota = self.estado.fonte_END.render(f"Nota: {self.estado.notas}/100", False, cor)
                    Nota_rect = Nota.get_rect(center=(LARGURA_VIRTUAL // 2, ALTURA_VIRTUAL // 2 - 100))
                    superficie_jogo.blit(Nota, Nota_rect)
                
                texto = self.estado.fonte_score.render("Enter para continuar...", False, (255, 255, 255))
                texto_rect = texto.get_rect(center=(LARGURA_VIRTUAL // 2, ALTURA_VIRTUAL // 2 + 100))
                texto2 = self.estado.fonte_score.render("Esc para Sair", False, (55, 55, 55))
                texto2_rect = texto2.get_rect(center=(LARGURA_VIRTUAL // 2, ALTURA_VIRTUAL // 2 + 400))
                
                superficie_jogo.blit(MENSAGEM, MENSAGEM_rect)
                superficie_jogo.blit(texto, texto_rect)
                superficie_jogo.blit(texto2, texto2_rect)

                tela.fill((0, 0, 0))
                jogo_escalado = pg.transform.scale(superficie_jogo, (LARGURA_JOGO, ALTURA_JOGO))
                tela.blit(jogo_escalado, (POS_X, POS_Y))

                pg.display.flip()
            
            self.Reiniciar()