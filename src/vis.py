import numpy as np
import pygame
import time

PRETO = (0, 0, 0)
CINZA = (180, 180, 180)
AZUL = (0, 100, 255)
VERDE = (0, 255, 0)

# TAMANHO_CELULA agora será calculado dinamicamente, então não precisa ser uma constante global.
# Mas podemos definir um tamanho máximo razoável para a célula, caso o mapa seja muito pequeno.
CELULA_MAX_SIZE = 60 # Tamanho máximo que uma célula pode ter, em pixels

class Visualizador:
    def __init__(self, ambiente):
        pygame.init()
        self.ambiente = ambiente
        self.mapa = ambiente.mapa
        self.altura, self.largura = self.mapa.shape

        # --- NOVO: Cálculo dinâmico do tamanho da célula e da tela ---
        info = pygame.display.Info() # Obtém informações sobre a tela atual
        largura_tela_max = info.current_w * 0.9 # Usa 90% da largura da tela para margem
        altura_tela_max = info.current_h * 0.9 # Usa 90% da altura da tela para margem

        # Calcula o tamanho da célula baseado na largura e altura do mapa
        # Garante que o mapa caiba na tela, limitando a CELL_MAX_SIZE
        self.tamanho_celula = min(
            CELULA_MAX_SIZE,
            int(largura_tela_max / self.largura),
            int(altura_tela_max / self.altura)
        )

        self.largura_janela = self.largura * self.tamanho_celula
        self.altura_janela = self.altura * self.tamanho_celula

        self.tela = pygame.display.set_mode((self.largura_janela, self.altura_janela))
        pygame.display.set_caption("Visualização do Agente")
        # --- FIM DO NOVO ---

        self.clock = pygame.time.Clock()

    def desenhar(self, estado_agente):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.fechar()
                raise SystemExit("Fechando visualização")

        self.tela.fill(PRETO)

        for y in range(self.altura):
            for x in range(self.largura):
                valor = self.mapa[y, x]
                # Usa self.tamanho_celula calculado dinamicamente
                rect = pygame.Rect(x * self.tamanho_celula, y * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)

                if valor == 1:
                    pygame.draw.rect(self.tela, CINZA, rect)

        # Desenha o destino final (em verde)
        fim = self.ambiente._encontrar_fim()
        # Usa self.tamanho_celula calculado dinamicamente
        rect_fim = pygame.Rect(fim[1] * self.tamanho_celula, fim[0] * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)
        pygame.draw.rect(self.tela, VERDE, rect_fim)

        # Desenha o agente (em azul)
        y, x = estado_agente
        # Usa self.tamanho_celula calculado dinamicamente
        rect_agente = pygame.Rect(x * self.tamanho_celula, y * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)
        pygame.draw.rect(self.tela, AZUL, rect_agente)

        pygame.display.flip()
        self.clock.tick(30)

    def change_map(self, mapa):
        self.ambiente.change_map(mapa)
        self.mapa = self.ambiente.mapa
        self.altura, self.largura = self.mapa.shape

        # --- NOVO: Recalcular o tamanho da célula e da tela ao mudar o mapa ---
        info = pygame.display.Info()
        largura_tela_max = info.current_w * 0.9
        altura_tela_max = info.current_h * 0.9

        self.tamanho_celula = min(
            CELULA_MAX_SIZE,
            int(largura_tela_max / self.largura),
            int(altura_tela_max / self.altura)
        )

        self.largura_janela = self.largura * self.tamanho_celula
        self.altura_janela = self.altura * self.tamanho_celula

        # Redimensiona a janela do Pygame
        self.tela = pygame.display.set_mode((self.largura_janela, self.altura_janela))
        # --- FIM DO NOVO ---

        self.ambiente.reset()

    def fechar(self):
        pygame.quit()