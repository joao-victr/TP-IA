import numpy as np


class Ambiente:
    def __init__(self, mapa):
        self.mapa = np.array(mapa)
        self.altura, self.largura = self.mapa.shape
        self.estado_inicial = self._encontrar_inicio()
        self.estado_atual = self.estado_inicial
        self.passo_atual = 0
        self.max_passos = 100

    def _encontrar_inicio(self):
        for y in range(self.altura):
            for x in range(self.largura):
                if self.mapa[y][x] == 1:
                    return y, x

    def reset(self):
        self.estado_inicial = self._encontrar_inicio()
        self.estado_atual = self.estado_inicial
        self.passo_atual = 0
        return self.estado_atual

    def step(self, acao):
        # 0 = cima, 1 = baixo, 2 = esquerda, 3 = direita
        y, x = self.estado_atual
        self.passo_atual += 1
        if acao == 0:
            y -= 1
        elif acao == 1:
            y += 1
        elif acao == 2:
            x -= 1
        elif acao == 3:
            x += 1
        if y < 0 or y >= self.altura or x < 0 or x >= self.largura:
            return self.estado_atual, -10, self._verifica_objetivo()

        if self.mapa[y, x] == 1:
            self.estado_atual = (y, x)
            terminou = self._verifica_objetivo()
            recompensa = 10 if terminou else -0.1
            return self.estado_atual, recompensa, terminou
        else:
            return self.estado_atual, -5, self._verifica_objetivo()

    def _verifica_objetivo(self):
        return self.estado_atual == self._encontrar_fim()

    def _encontrar_fim(self):
        for y in reversed(range(self.altura)):
            for x in reversed(range(self.largura)):
                if self.mapa[y, x] == 1:
                    return y, x

    def change_map(self, mapa):
        self.mapa = np.array(mapa)
        self.altura, self.largura = self.mapa.shape