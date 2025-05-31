import pygame

PRETO = (0, 0, 0)
CINZA = (180, 180, 180)
AZUL = (0, 100, 255)
VERDE = (0, 255, 0)

CELULA_MAX_SIZE = 60

class Visualizador:
    def __init__(self, ambiente):
        pygame.init()
        self.ambiente = ambiente
        self.mapa = ambiente.mapa
        self.altura, self.largura = self.mapa.shape
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

        fim = self.ambiente._encontrar_fim()
        rect_fim = pygame.Rect(fim[1] * self.tamanho_celula, fim[0] * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)
        pygame.draw.rect(self.tela, VERDE, rect_fim)

        y, x = estado_agente
        rect_agente = pygame.Rect(x * self.tamanho_celula, y * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)
        pygame.draw.rect(self.tela, AZUL, rect_agente)

        pygame.display.flip()
        self.clock.tick(30)

    def change_map(self, mapa):
        self.ambiente.change_map(mapa)
        self.mapa = self.ambiente.mapa
        self.altura, self.largura = self.mapa.shape

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

        self.tela = pygame.display.set_mode((self.largura_janela, self.altura_janela))
        self.ambiente.reset()

    def fechar(self):
        pygame.quit()