import numpy as np
import random

class Agente:
    def __init__(self, ambiente, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.ambiente = ambiente
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.acoes = [0, 1, 2, 3]
        self.q_table = {}

    def _estado_para_str(self, estado):
        return str(estado)

    def escolher_acao(self, estado):
        estado_str = self._estado_para_str(estado)
        if random.uniform(0, 1) < self.epsilon or estado_str not in self.q_table:
            return random.choice(self.acoes)
        return int(np.argmax(self.q_table[estado_str]))

    def atualizar_q(self, estado, acao, recompensa, proximo_estado):
        s = self._estado_para_str(estado)
        s_prime = self._estado_para_str(proximo_estado)

        if s not in self.q_table:
            self.q_table[s] = np.zeros(len(self.acoes))
        if s_prime not in self.q_table:
            self.q_table[s_prime] = np.zeros(len(self.acoes))

        q_atual = self.q_table[s][acao]
        q_max_prox = np.max(self.q_table[s_prime])

        self.q_table[s][acao] = q_atual + self.alpha * (recompensa + self.gamma * q_max_prox - q_atual)

    def treinar(self, episodios=1000):
        for ep in range(episodios):
            estado = self.ambiente.reset()
            terminado = False
            total_recompensa = 0

            while not terminado:
                acao = self.escolher_acao(estado)
                novo_estado, recompensa, terminado = self.ambiente.step(acao)
                self.atualizar_q(estado, acao, recompensa, novo_estado)
                estado = novo_estado
                total_recompensa += recompensa
            # self.epsilon = max(0.15, self.epsilon * 0.995)

            # if (ep + 1) % 100 == 0:
            #     print(f"Episódio {ep + 1}: recompensa total = {total_recompensa}")
    print('Treinamento finalizado')
    def reset(self):
        self.q_table = {}