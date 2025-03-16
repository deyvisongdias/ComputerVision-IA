from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import time

# Tempos de travessia de cada membro da banda
info = [
    {"nome": "Bono", "tempo": 1},
    {"nome": "Edge", "tempo": 2},
    {"nome": "Adam", "tempo": 5},
    {"nome": "Larry", "tempo": 10}
]

transicoes_esquerda = [
    ["Bono", "Edge"],
    ["Bono", "Adam"],
    ["Bono", "Larry"],
    ["Edge", "Adam"],
    ["Edge", "Larry"],
    ["Adam", "Larry"]
]

transicoes_direita = [
    ["Bono"],
    ["Edge"],
    ["Adam"],
    ["Larry"]
]


class Estado:
    def __init__(self, lado_esquerdo, lado_direito, lanterna, tempo, movimento=None):
        self.lado_esquerdo = lado_esquerdo  # Usar tuple para imutabilidade
        self.lado_direito = lado_direito  # Usar tuple para imutabilidade
        self.lanterna = lanterna
        self.tempo = tempo
        self.movimento = movimento  # Guarda quem atravessou

    def __lt__(self, outro):
        return self.tempo < outro.tempo  # Para comparação na busca

    def __repr__(self):
        movimento_str = ""
        if self.movimento:
            if (self.lanterna == "esquerda"):
                movimento_str = f" <- {' e '.join(self.movimento)} voltou"
            else:
                movimento_str = f" -> {' e '.join(self.movimento)} foram"
        else:
            movimento_str = "\n - Início do problema"

        tabulations = "\t\t\t\t\t"
        for i in range(len(self.lado_esquerdo)):
            tabulations = tabulations[:-1]

        return f"{movimento_str} \t| Tempo: {self.tempo} \t| Lado esquerdo: {self.lado_esquerdo} {tabulations}| Lado direito: {self.lado_direito}\n"

    def gerar_proximos_estados(self):
        proximos_estados = []
        lado_atual = []
        transicoes = []

        if (self.lanterna == "esquerda"):
            for transicao in transicoes_esquerda:
                lado_atual = self.lado_esquerdo.copy()

                for membro in lado_atual:
                    if (membro in transicao):
                        lado_atual.remove(membro)
                        for outro_membro in lado_atual:
                            if (outro_membro in transicao):
                                if (transicao not in transicoes):
                                    transicoes.append(transicao)

            for transicao in transicoes:
                novo_lado_esquerdo = self.lado_esquerdo.copy()
                novo_lado_esquerdo.remove(transicao[0])
                novo_lado_esquerdo.remove(transicao[1])

                novo_lado_direito = self.lado_direito.copy()
                novo_lado_direito.append(transicao[0])
                novo_lado_direito.append(transicao[1])

                lanterna = "direita"

                tempo = self.tempo
                tempo_gasto = 0

                movimento = []

                for membro in info:
                    if (membro.get("nome") == transicao[0] or membro.get("nome") == transicao[1]):
                        tempo_gasto = max(tempo_gasto, membro.get("tempo"))
                        movimento.append(membro.get("nome"))

                tempo = tempo + tempo_gasto

                novo_estado = Estado(
                    novo_lado_esquerdo, novo_lado_direito, lanterna, tempo, movimento)

                proximos_estados.append(novo_estado)

        if (self.lanterna == "direita"):
            lado_atual = self.lado_direito.copy()

            for transicao in transicoes_direita:
                for membro in lado_atual:
                    if (membro in transicao):
                        transicoes.append(transicao)

            for transicao in transicoes:
                novo_lado_esquerdo = self.lado_esquerdo.copy()
                novo_lado_esquerdo.append(transicao[0])

                novo_lado_direito = self.lado_direito.copy()
                novo_lado_direito.remove(transicao[0])

                lanterna = "esquerda"

                tempo = self.tempo

                movimento = []

                for membro in info:
                    if (membro.get("nome") == transicao[0]):
                        tempo = tempo + membro.get("tempo")
                        movimento.append(membro.get("nome"))

                novo_estado = Estado(
                    novo_lado_esquerdo, novo_lado_direito, lanterna, tempo, movimento)

                proximos_estados.append(novo_estado)

        return proximos_estados


def todos_no_lado_direito(estado):
    if (len(estado.lado_esquerdo) == 0):
        return True
    return False


def imprimir_caminho(caminho):
    for estado in caminho:
        print(estado)


def busca_largura(estado_inicial):
    tempo_inicial = time.time()
    fila = deque([[estado_inicial]])
    visitados = []

    while fila:
        caminho = fila.popleft()
        estado_atual = caminho[-1]

        estado_tuple = (estado_atual.lado_esquerdo,
                        estado_atual.lado_direito, estado_atual.lanterna)
        if estado_tuple in visitados:
            continue
        visitados.append(estado_tuple)

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca em Largura):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            imprimir_caminho(caminho)
            return caminho

        for prox_estado in estado_atual.gerar_proximos_estados():
            fila.append(caminho + [prox_estado])

    tempo_final = time.time()
    tempoTotal = tempo_final - tempo_inicial
    print("Nenhuma solução encontrada!")
    print(f"Tempo de execução: {tempoTotal:.6f} segundos")
    return None


def busca_backtracking(estado_atual, caminho, visitados, tempo_inicial=None):
    if tempo_inicial is None:
        tempo_inicial = time.time()

    if estado_atual.tempo > 17:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        return None

    estado_tuple = (estado_atual.lado_esquerdo, estado_atual.lanterna)
    if estado_tuple in visitados:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        return None
    visitados.append(estado_tuple)

    if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        print("Solução encontrada (Backtracking):")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
        imprimir_caminho(caminho)
        return caminho

    for prox_estado in estado_atual.gerar_proximos_estados():
        resultado = busca_backtracking(
            prox_estado, caminho + [prox_estado], visitados, tempo_inicial)
        if resultado:
            return resultado

    visitados.remove(estado_tuple)
    return None


def busca_profundidade(estado_inicial):
    tempo_inicial = time.time()
    pilha = [[estado_inicial]]
    visitados = set()

    while pilha:
        caminho = pilha.pop()
        estado_atual = caminho[-1]

        estado_tuple = (tuple(estado_atual.lado_esquerdo), tuple(
            estado_atual.lado_direito), estado_atual.lanterna)
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca em Profundidade):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            imprimir_caminho(caminho)
            return caminho

        for prox_estado in reversed(estado_atual.gerar_proximos_estados()):
            pilha.append(caminho + [prox_estado])

    tempo_final = time.time()
    tempoTotal = tempo_final - tempo_inicial
    print("Nenhuma solução encontrada!")
    print(f"Tempo de execução: {tempoTotal:.6f} segundos")
    return None


def custo_real(estado):
    return estado.tempo


def busca_ordenada(estado_inicial):
    tempo_inicial = time.time()
    # Inicializa a fila com o caminho inicial contendo apenas o estado inicial
    fila = [(custo_real(estado_inicial), [estado_inicial])]
    visitados = set()

    while fila:
        # Obtém o caminho com menor custo
        _, caminho = heapq.heappop(fila)
        estado_atual = caminho[-1]

        # Cria uma representação única do estado para verificar se já foi visitado
        estado_tuple = (tuple(sorted(estado_atual.lado_esquerdo)),
                        tuple(sorted(estado_atual.lado_direito)),
                        estado_atual.lanterna)

        if estado_tuple in visitados:
            continue

        visitados.add(estado_tuple)

        # Verifica se chegou ao objetivo
        if todos_no_lado_direito(estado_atual):
            if estado_atual.tempo <= 17:  # Adiciona verificação do tempo máximo
                tempo_final = time.time()
                tempoTotal = tempo_final - tempo_inicial
                print("Solução encontrada (Busca Ordenada):")
                print(f"Tempo de execução: {tempoTotal:.6f} segundos")
                imprimir_caminho(caminho)
                return caminho
            continue  # Pula este estado se exceder 17 minutos

        # Gera os próximos estados
        proximos_estados = estado_atual.gerar_proximos_estados()

        for prox_estado in proximos_estados:
            # Cria um novo caminho adicionando o próximo estado
            novo_caminho = caminho + [prox_estado]

            # Adiciona o novo caminho à fila, com prioridade baseada no custo real
            heapq.heappush(fila, (custo_real(prox_estado), novo_caminho))

    tempo_final = time.time()
    tempoTotal = tempo_final - tempo_inicial
    print("Nenhuma solução encontrada!")
    print(f"Tempo de execução: {tempoTotal:.6f} segundos")
    return None


def heuristicaAestrela(estado):
    soma = 0
    for nome in estado.lado_esquerdo:
        # Encontra o tempo de travessia de cada membro ainda no lado esquerdo
        for membro in info:
            if membro["nome"] == nome:
                soma += membro["tempo"]
                break
    return soma


def heuristica(estado):
    # Heurística: tempo máximo de travessia dos membros no lado esquerdo + tempo de retorno da lanterna
    max_tempo = 0
    for nome in estado.lado_esquerdo:
        for membro in info:
            if membro["nome"] == nome:
                max_tempo = max(max_tempo, membro["tempo"])
                break
    # Adiciona o tempo de retorno da lanterna (membro mais rápido no lado direito)
    if estado.lado_direito:
        min_tempo_direito = min(
            [membro["tempo"] for membro in info if membro["nome"] in estado.lado_direito])
        max_tempo += min_tempo_direito
    return max_tempo


def busca_gulosa(estado_inicial):
    tempo_inicial = time.time()
    # Inicializa a fila de prioridade com o estado inicial
    # (heurística, caminho)
    fila = [(heuristica(estado_inicial), [estado_inicial])]
    visitados = set()

    while fila:
        # Obtém o caminho com menor valor heurístico
        h, caminho = heapq.heappop(fila)  # Desempacota corretamente
        estado_atual = caminho[-1]

        # Cria uma representação única do estado para verificar se já foi visitado
        estado_tuple = (tuple(sorted(estado_atual.lado_esquerdo)),
                        tuple(sorted(estado_atual.lado_direito)),
                        estado_atual.lanterna)

        if estado_tuple in visitados:
            continue

        visitados.add(estado_tuple)

        # Verifica se chegou ao objetivo
        if todos_no_lado_direito(estado_atual):
            if estado_atual.tempo <= 17:  # Verifica tempo máximo
                tempo_final = time.time()
                tempoTotal = tempo_final - tempo_inicial
                print("Solução encontrada (Busca Gulosa):")
                print(f"Tempo de execução: {tempoTotal:.6f} segundos")
                imprimir_caminho(caminho)
                return caminho
            continue  # Pula este estado se exceder 17 minutos

        # Gera os próximos estados
        proximos_estados = estado_atual.gerar_proximos_estados()

        for prox_estado in proximos_estados:
            # Verifica se o próximo estado não excede o tempo limite
            if prox_estado.tempo > 17:
                continue

            # Cria um novo caminho adicionando o próximo estado
            novo_caminho = caminho + [prox_estado]

            # Adiciona o novo caminho à fila, com prioridade baseada na heurística
            h = heuristica(prox_estado)
            heapq.heappush(fila, (h, novo_caminho))

    tempo_final = time.time()
    tempoTotal = tempo_final - tempo_inicial
    print("Nenhuma solução encontrada (Busca Gulosa)!")
    print(f"Tempo de execução: {tempoTotal:.6f} segundos")
    return None


def busca_aestrela(estado_inicial):
    fila = [(custo_real(estado_inicial) + heuristicaAestrela(estado_inicial),
             [estado_inicial])]  # (f, caminho)
    visitados = set()

    while fila:
        # Obtém o caminho com menor f = g + h
        f, caminho = heapq.heappop(fila)
        estado_atual = caminho[-1]

        # Cria uma representação única do estado para verificar se já foi visitado
        estado_tuple = (tuple(sorted(estado_atual.lado_esquerdo)),
                        tuple(sorted(estado_atual.lado_direito)),
                        estado_atual.lanterna)

        if estado_tuple in visitados:
            continue

        visitados.add(estado_tuple)

        # Verifica se chegou ao objetivo
        if todos_no_lado_direito(estado_atual):
            if estado_atual.tempo <= 17:  # Verifica tempo máximo
                print("Solução encontrada (Busca A*):")
                imprimir_caminho(caminho)
                return caminho
            continue  # Pula este estado se exceder 17 minutos
#
# if todos_no_lado_direito(estado_atual):
 #           print(f"Solução encontrad#a (Busca A*) com tempo total: {estado_atual.tempo} minutos:")
 #           imprimir_caminho(caminho)#
#
 #           if estado_atual.tempo <= 17:
 #               print("Esta é uma solução viável (dentro do limite de 17 minutos).")
 #           else:
 #               print("Esta solução excede o limite de 17 minutos.")
#
 #           return caminho

        # Gera os próximos estados
        proximos_estados = estado_atual.gerar_proximos_estados()

        for prox_estado in proximos_estados:
            # Cria um novo caminho adicionando o próximo estado
            novo_caminho = caminho + [prox_estado]

            # Adiciona o novo caminho à fila, com prioridade f = g + h
            f = custo_real(prox_estado) + heuristicaAestrela(prox_estado)
            heapq.heappush(fila, (f, novo_caminho))

    print("Nenhuma solução encontrada (Busca A*)!")
    return None


def desenhar_grafo(caminho):
    G = nx.DiGraph()
    labels = {}
    cores = []

    for i, estado in enumerate(caminho):
        lado_esq = estado.lado_esquerdo
        lado_dir = estado.lado_direito
        labels[i] = f"Tempo: {estado.tempo}m\nEsquerdo: {', '.join(lado_esq)}\nDireito: {', '.join(lado_dir)}"

        G.add_node(i, label=labels[i])
        # Define a cor com base na posição da lanterna
        cores.append("lightgreen" if estado.lanterna ==
                     "esquerda" else "lightblue")

        if i > 0:
            G.add_edge(i - 1, i)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000,
            node_color=cores, edge_color="gray", font_size=10, font_weight="bold")
    plt.title("Grafo da solução da travessia da banda U2")
    plt.show()


# Execução
estado_inicial = Estado(["Bono", "Edge", "Adam", "Larry"], [], "esquerda", 0)

modo = input("Escolha o método de busca (largura (l), backtracking (b), profundidade (p), ordenada (o), gulosa (g) ou A* (a)): ").strip().lower()
if modo == "l":
    caminho_solucao = busca_largura(estado_inicial)
elif modo == "b":
    tempo_inicial = time.time()
    caminho_solucao = busca_backtracking(estado_inicial, [estado_inicial], [])
    if not caminho_solucao:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        print("Nenhuma solução encontrada (Backtracking)!")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
elif modo == "p":
    caminho_solucao = busca_profundidade(estado_inicial)
elif modo == "o":
    caminho_solucao = busca_ordenada(estado_inicial)
elif modo == "g":
    caminho_solucao = busca_gulosa(estado_inicial)
elif modo == "a":
    caminho_solucao = busca_aestrela(estado_inicial)
else:
    print("Método inválido!")
    caminho_solucao = None

if caminho_solucao:
    desenhar_grafo(caminho_solucao)
print("Busca finalizada.")
