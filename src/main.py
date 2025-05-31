import gymnasium as gym
from ambiente import Ambiente
from agente import Agente
from vis import Visualizador
import time
import mapas



env = Ambiente(mapas.mapa1)
agente = Agente(env)

agente.treinar(episodios=100)

visualizador = Visualizador(env)
mapa_atual = 1
sucesso = False

print(env.obj)
while not sucesso:
    agente.treinar(episodios=100)
    estado = env.reset()
    terminado = False

    while not terminado:
        visualizador.desenhar(estado)
        acao = agente.escolher_acao(estado)
        novo_estado, recompensa, terminado = env.step(acao)
        estado = novo_estado
        time.sleep(0.0001)

    if env._verifica_objetivo():
        agente.reset()
        if mapa_atual == 1:
            visualizador.change_map(mapas.mapa2)
        if mapa_atual == 2:
            visualizador.change_map(mapas.mapa3)
        agente.treinar(episodios=100)
        mapa_atual += 1
        if mapa_atual > mapas.num_mapas:
            sucesso = True
visualizador.fechar()
