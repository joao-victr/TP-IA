from ambiente import Ambiente
from agente import Agente
from vis import Visualizador
import time
import mapas

env = Ambiente(mapas.mapa1)
agente = Agente(env)

visualizador = Visualizador(env)
mapa_atual = 1
sucesso = False

while not sucesso:
    print(f"\n--- Mapa {mapa_atual} ---")
    mapa_resolvido = False
    while not mapa_resolvido:
        estado = env.reset()
        terminado_passo_vis = False
        recompensa_episodio_visual = 0
        while not terminado_passo_vis:
            try:
                visualizador.desenhar(estado)
                acao = agente.escolher_acao(estado)
                novo_estado, recompensa, terminado_ambiente = env.step(acao)
                agente.atualizar_q(estado, acao, recompensa, novo_estado)
                estado = novo_estado
                recompensa_episodio_visual += recompensa
                terminado_passo_vis = terminado_ambiente
                time.sleep(0.00001)
            except SystemExit:
                sucesso = True
                mapa_resolvido = True
                break
        if sucesso:
            break
        if env._verifica_objetivo():
            mapa_resolvido = True
            if mapa_atual < mapas.num_mapas:
                mapa_atual += 1
                if mapa_atual == 2:
                    visualizador.change_map(mapas.mapa2)
                elif mapa_atual == 3:
                    visualizador.change_map(mapas.mapa3)
                env.reset()
                agente.reset()
            else:
                sucesso = True
visualizador.fechar()


input("Aperte Enter para rodar o agente treinado")
env = Ambiente(mapas.mapa1)
agente = Agente(env)
visualizador = Visualizador(env)
mapa_atual = 1
visualizador.change_map(mapas.mapa1)
sucesso = False
while not sucesso:
    agente.treinar(episodios=1000)
    estado = env.reset()
    terminado_passo_vis = False
    recompensa_episodio_visual = 0
    while not terminado_passo_vis:
        try:
            visualizador.desenhar(estado)
            acao = agente.escolher_acao(estado)
            novo_estado, recompensa, terminado_ambiente = env.step(acao)
            estado = novo_estado
            recompensa_episodio_visual += recompensa
            terminado_passo_vis = terminado_ambiente
            time.sleep(0.0001)
        except SystemExit:
            sucesso = True
            mapa_resolvido = True
            break
    if sucesso:
        break
    if env._verifica_objetivo():
        mapa_resolvido = True
        if mapa_atual < mapas.num_mapas:
            mapa_atual += 1
            if mapa_atual == 2:
                visualizador.change_map(mapas.mapa2)
            elif mapa_atual == 3:
                visualizador.change_map(mapas.mapa3)
            env.reset()
        else:
            sucesso = True

visualizador.fechar()