from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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



# Testando animação
def busca_largura_com_historico(estado_inicial):
    tempo_inicial = time.time()
    fila = deque([[estado_inicial]])
    visitados = []
    
    # Estrutura para armazenar o histórico da busca
    historico = []
    contador_estados = 0
    estado_inicial.id = contador_estados
    
    # Registra o estado inicial
    historico.append({
        'tipo': 'inicial',
        'estado': estado_inicial,
        'id': contador_estados
    })
    
    while fila:
        caminho = fila.popleft()
        estado_atual = caminho[-1]
        
        # Registra o estado sendo explorado
        historico.append({
            'tipo': 'explorando',
            'estado': estado_atual,
            'id': estado_atual.id
        })

        estado_tuple = (tuple(sorted(estado_atual.lado_esquerdo)),
                       tuple(sorted(estado_atual.lado_direito)), 
                       estado_atual.lanterna)
        
        if estado_tuple in visitados:
            # Registra estado rejeitado (já visitado)
            historico.append({
                'tipo': 'rejeitado',
                'estado': estado_atual,
                'id': estado_atual.id,
                'motivo': 'já visitado'
            })
            continue
            
        visitados.append(estado_tuple)

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca em Largura):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            
            # Registra o caminho da solução
            for i, estado in enumerate(caminho):
                historico.append({
                    'tipo': 'solucao',
                    'estado': estado,
                    'id': estado.id,
                    'posicao_caminho': i
                })
                
            return caminho, historico

        for prox_estado in estado_atual.gerar_proximos_estados():
            contador_estados += 1
            prox_estado.id = contador_estados
            
            # Registra novo estado gerado
            historico.append({
                'tipo': 'gerado',
                'estado': prox_estado,
                'id': prox_estado.id,
                'pai': estado_atual.id
            })
            
            if prox_estado.tempo > 17:
                # Registra estado rejeitado (tempo excedido)
                historico.append({
                    'tipo': 'rejeitado',
                    'estado': prox_estado,
                    'id': prox_estado.id,
                    'motivo': 'tempo excedido'
                })
                continue
                
            fila.append(caminho + [prox_estado])

    tempo_final = time.time()
    tempoTotal = tempo_final - tempo_inicial
    print("Nenhuma solução encontrada!")
    print(f"Tempo de execução: {tempoTotal:.6f} segundos")
    return None, historico

def busca_profundidade_com_historico(estado_inicial):
    tempo_inicial = time.time()
    pilha = [[estado_inicial]]
    visitados = set()
    
    # Estrutura para armazenar o histórico da busca
    historico = []
    contador_estados = 0
    estado_inicial.id = contador_estados
    
    # Registra o estado inicial
    historico.append({
        'tipo': 'inicial',
        'estado': estado_inicial,
        'id': contador_estados
    })
    
    while pilha:
        caminho = pilha.pop()
        estado_atual = caminho[-1]
        
        # Registra o estado sendo explorado
        historico.append({
            'tipo': 'explorando',
            'estado': estado_atual,
            'id': estado_atual.id
        })

        estado_tuple = (tuple(sorted(estado_atual.lado_esquerdo)),
                       tuple(sorted(estado_atual.lado_direito)), 
                       estado_atual.lanterna)
        
        if estado_tuple in visitados:
            # Registra estado rejeitado (já visitado)
            historico.append({
                'tipo': 'rejeitado',
                'estado': estado_atual,
                'id': estado_atual.id,
                'motivo': 'já visitado'
            })
            continue
            
        visitados.add(estado_tuple)

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca em Profundidade):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            
            # Registra o caminho da solução
            for i, estado in enumerate(caminho):
                historico.append({
                    'tipo': 'solucao',
                    'estado': estado,
                    'id': estado.id,
                    'posicao_caminho': i
                })
                
            return caminho, historico

        for prox_estado in reversed(estado_atual.gerar_proximos_estados()):
            contador_estados += 1
            prox_estado.id = contador_estados
            
            # Registra novo estado gerado
            historico.append({
                'tipo': 'gerado',
                'estado': prox_estado,
                'id': prox_estado.id,
                'pai': estado_atual.id
            })
            
            if prox_estado.tempo > 17:
                # Registra estado rejeitado (tempo excedido)
                historico.append({
                    'tipo': 'rejeitado',
                    'estado': prox_estado,
                    'id': prox_estado.id,
                    'motivo': 'tempo excedido'
                })
                continue
                
            pilha.append(caminho + [prox_estado])

    tempo_final = time.time()
    tempoTotal = tempo_final - tempo_inicial
    print("Nenhuma solução encontrada!")
    print(f"Tempo de execução: {tempoTotal:.6f} segundos")
    return None, historico

def busca_gulosa_com_historico(estado_inicial):
    tempo_inicial = time.time()
    fila = [(heuristica(estado_inicial), [estado_inicial])]
    visitados = set()
    
    # Estrutura para armazenar o histórico da busca
    historico = []
    contador_estados = 0
    estado_inicial.id = contador_estados
    
    # Registra o estado inicial
    historico.append({
        'tipo': 'inicial',
        'estado': estado_inicial,
        'id': contador_estados
    })
    
    while fila:
        h, caminho = heapq.heappop(fila)
        estado_atual = caminho[-1]
        
        # Registra o estado sendo explorado
        historico.append({
            'tipo': 'explorando',
            'estado': estado_atual,
            'id': estado_atual.id
        })

        estado_tuple = (tuple(sorted(estado_atual.lado_esquerdo)),
                       tuple(sorted(estado_atual.lado_direito)), 
                       estado_atual.lanterna)
        
        if estado_tuple in visitados:
            # Registra estado rejeitado (já visitado)
            historico.append({
                'tipo': 'rejeitado',
                'estado': estado_atual,
                'id': estado_atual.id,
                'motivo': 'já visitado'
            })
            continue
            
        visitados.add(estado_tuple)

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca Gulosa):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            
            # Registra o caminho da solução
            for i, estado in enumerate(caminho):
                historico.append({
                    'tipo': 'solucao',
                    'estado': estado,
                    'id': estado.id,
                    'posicao_caminho': i
                })
                
            return caminho, historico

        for prox_estado in estado_atual.gerar_proximos_estados():
            contador_estados += 1
            prox_estado.id = contador_estados
            
            # Registra novo estado gerado
            historico.append({
                'tipo': 'gerado',
                'estado': prox_estado,
                'id': prox_estado.id,
                'pai': estado_atual.id
            })
            
            if prox_estado.tempo > 17:
                # Registra estado rejeitado (tempo excedido)
                historico.append({
                    'tipo': 'rejeitado',
                    'estado': prox_estado,
                    'id': prox_estado.id,
                    'motivo': 'tempo excedido'
                })
                continue
                
            heapq.heappush(fila, (heuristica(prox_estado), caminho + [prox_estado]))

    tempo_final = time.time()
    tempoTotal = tempo_final - tempo_inicial
    print("Nenhuma solução encontrada!")
    print(f"Tempo de execução: {tempoTotal:.6f} segundos")
    return None, historico

def busca_aestrela_com_historico(estado_inicial):
    tempo_inicial = time.time()
    fila = [(custo_real(estado_inicial) + heuristicaAestrela(estado_inicial), [estado_inicial])]
    visitados = set()
    
    # Estrutura para armazenar o histórico da busca
    historico = []
    contador_estados = 0
    estado_inicial.id = contador_estados
    
    # Registra o estado inicial
    historico.append({
        'tipo': 'inicial',
        'estado': estado_inicial,
        'id': contador_estados
    })
    
    while fila:
        f, caminho = heapq.heappop(fila)
        estado_atual = caminho[-1]
        
        # Registra o estado sendo explorado
        historico.append({
            'tipo': 'explorando',
            'estado': estado_atual,
            'id': estado_atual.id
        })

        estado_tuple = (tuple(sorted(estado_atual.lado_esquerdo)),
                       tuple(sorted(estado_atual.lado_direito)), 
                       estado_atual.lanterna)
        
        if estado_tuple in visitados:
            # Registra estado rejeitado (já visitado)
            historico.append({
                'tipo': 'rejeitado',
                'estado': estado_atual,
                'id': estado_atual.id,
                'motivo': 'já visitado'
            })
            continue
            
        visitados.add(estado_tuple)

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca A*):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            
            # Registra o caminho da solução
            for i, estado in enumerate(caminho):
                historico.append({
                    'tipo': 'solucao',
                    'estado': estado,
                    'id': estado.id,
                    'posicao_caminho': i
                })
                
            return caminho, historico

        for prox_estado in estado_atual.gerar_proximos_estados():
            contador_estados += 1
            prox_estado.id = contador_estados
            
            # Registra novo estado gerado
            historico.append({
                'tipo': 'gerado',
                'estado': prox_estado,
                'id': prox_estado.id,
                'pai': estado_atual.id
            })
            
            if prox_estado.tempo > 17:
                # Registra estado rejeitado (tempo excedido)
                historico.append({
                    'tipo': 'rejeitado',
                    'estado': prox_estado,
                    'id': prox_estado.id,
                    'motivo': 'tempo excedido'
                })
                continue
                
            heapq.heappush(fila, (custo_real(prox_estado) + heuristicaAestrela(prox_estado), caminho + [prox_estado]))

    tempo_final = time.time()
    tempoTotal = tempo_final - tempo_inicial
    print("Nenhuma solução encontrada!")
    print(f"Tempo de execução: {tempoTotal:.6f} segundos")
    return None, historico

def busca_backtracking_com_historico(estado_atual, caminho, visitados, historico, tempo_inicial=None):
    if tempo_inicial is None:
        tempo_inicial = time.time()

    # Registra o estado sendo explorado
    historico.append({
        'tipo': 'explorando',
        'estado': estado_atual,
        'id': estado_atual.id
    })

    # Verifica se o tempo excedeu o limite
    if estado_atual.tempo > 17:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        print("Tempo excedido (Backtracking):")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
        
        # Registra estado rejeitado (tempo excedido)
        historico.append({
            'tipo': 'rejeitado',
            'estado': estado_atual,
            'id': estado_atual.id,
            'motivo': 'tempo excedido'
        })
        return None

    # Cria uma representação única do estado para verificar se já foi visitado
    estado_tuple = (tuple(sorted(estado_atual.lado_esquerdo)),
                    tuple(sorted(estado_atual.lado_direito)),
                    estado_atual.lanterna)

    if estado_tuple in visitados:
        # Registra estado rejeitado (já visitado)
        historico.append({
            'tipo': 'rejeitado',
            'estado': estado_atual,
            'id': estado_atual.id,
            'motivo': 'já visitado'
        })
        return None

    visitados.add(estado_tuple)

    # Verifica se chegou ao objetivo
    if todos_no_lado_direito(estado_atual):
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        print("Solução encontrada (Backtracking):")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
        
        # Registra o caminho da solução
        for i, estado in enumerate(caminho):
            historico.append({
                'tipo': 'solucao',
                'estado': estado,
                'id': estado.id,
                'posicao_caminho': i
            })
        
        return caminho

    # Gera os próximos estados
    for prox_estado in estado_atual.gerar_proximos_estados():
        # Atribui um ID único ao próximo estado
        prox_estado.id = len(historico)
        
        # Registra novo estado gerado
        historico.append({
            'tipo': 'gerado',
            'estado': prox_estado,
            'id': prox_estado.id,
            'pai': estado_atual.id
        })

        # Chama recursivamente a busca
        resultado = busca_backtracking_com_historico(
            prox_estado, caminho + [prox_estado], visitados, historico, tempo_inicial
        )
        
        if resultado:
            return resultado

    # Remove o estado atual dos visitados (backtracking)
    visitados.remove(estado_tuple)
    
    # Registra estado rejeitado (backtracking)
    historico.append({
        'tipo': 'rejeitado',
        'estado': estado_atual,
        'id': estado_atual.id,
        'motivo': 'backtracking'
    })
    
    return None

def animar_busca(historico):
    G = nx.DiGraph()
    fig, ax = plt.subplots(figsize=(18, 12))
    
    # Dicionário para armazenar informações dos nós
    nos_info = {}
    
    # Manter registro dos nós que fazem parte da solução
    nos_solucao = set()
    arestas_solucao = set()
    
    # Preparar dados para a animação
    for evento in historico:
        estado = evento['estado']
        estado_id = evento['id']
        
        # Marcar nós que fazem parte da solução
        if evento['tipo'] == 'solucao':
            nos_solucao.add(estado_id)
            if 'posicao_caminho' in evento and evento['posicao_caminho'] > 0:
                # Tentar encontrar o nó pai na solução
                for outro_evento in historico:
                    if outro_evento['tipo'] == 'solucao' and \
                       'posicao_caminho' in outro_evento and \
                       outro_evento['posicao_caminho'] == evento['posicao_caminho'] - 1:
                        arestas_solucao.add((outro_evento['id'], estado_id))
                        break
        
        if estado_id not in nos_info:
            # Criar representação do nó
            lado_esq = estado.lado_esquerdo
            lado_dir = estado.lado_direito
            label = f"ID: {estado_id}\nTempo: {estado.tempo}m\nEsq: {', '.join(lado_esq)}\nDir: {', '.join(lado_dir)}"
            
            # Armazenar informações
            nos_info[estado_id] = {
                'label': label,
                'estado': estado,
                'tipo': evento['tipo']
            }
            
            # Adicionar conexão com o pai se existir
            if 'pai' in evento:
                nos_info[estado_id]['pai'] = evento['pai']
                G.add_edge(evento['pai'], estado_id)
            else:
                G.add_node(estado_id)  # Nó raiz
    
    # Criar um layout hierárquico usando direcionamento 'top-to-bottom'
    pos = {}
    
    # Encontrar nó raiz (inicial)
    raiz = None
    for evento in historico:
        if evento['tipo'] == 'inicial':
            raiz = evento['id']
            break
    
    if raiz is None and G.nodes():
        raiz = list(G.nodes())[0]
    
    # Função para calcular a profundidade de cada nó
    niveis = {}
    filhos_por_nivel = {}
    
    def calcular_nivel(node, nivel=0):
        niveis[node] = nivel
        if nivel not in filhos_por_nivel:
            filhos_por_nivel[nivel] = []
        filhos_por_nivel[nivel].append(node)
        
        # Recursivamente para todos os filhos
        for filho in G.successors(node):
            calcular_nivel(filho, nivel + 1)
    
    # Chamar função para calcular níveis
    try:
        if raiz is not None:
            calcular_nivel(raiz)
        else:
            raise nx.NetworkXError("Raiz não encontrada")
    except nx.NetworkXError:
        # Fallback se o grafo estiver vazio ou desconectado
        print("Aviso: Grafo desconectado ou vazio, usando layout spring como fallback")
        pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
    else:
        # Determinar largura e altura do layout
        max_nivel = max(niveis.values()) if niveis else 0
        altura_total = max_nivel + 1
        
        # Posicionar cada nó
        for nivel in range(altura_total):
            nodos_nivel = filhos_por_nivel.get(nivel, [])
            quantidade = len(nodos_nivel)
            
            # Distribuir os nós horizontalmente no nível
            for i, node in enumerate(sorted(nodos_nivel)):
                # Coordenada x espaçada uniformemente
                largura = max(1, len(nodos_nivel))
                x = (i - largura/2) / (largura * 0.8)
                
                # Coordenada y diretamente relacionada ao nível
                y = 1.0 - (nivel * 0.2)
                
                pos[node] = (x, y)
    
    # Variável para rastrear se é o último frame
    is_last_frame = [False]
    
    def update(num):
        ax.clear()
        
        # Verificar se é o último frame
        is_last_frame[0] = (num == min(len(historico), 100) - 1)
        
        # Subgrafo até o frame atual
        eventos_ate_agora = historico[:num+1]
        nos_mostrados = set()
        arestas_mostradas = set()
        
        # Cores dos nós
        node_colors = []
        edge_colors = []
        node_sizes = []
        
        # Construir grafo para o frame atual
        G_atual = nx.DiGraph()
        
        # Para o último frame, mostrar todos os nós da solução
        if is_last_frame[0]:
            # Se é o último frame, adicionar todos os nós e arestas da solução
            for node in nos_solucao:
                G_atual.add_node(node)
                nos_mostrados.add(node)
            
            for pai, filho in arestas_solucao:
                G_atual.add_edge(pai, filho)
                arestas_mostradas.add((pai, filho))
        
        # Adicionar nós e arestas conforme o histórico
        for evento in eventos_ate_agora:
            estado_id = evento['id']
            tipo = evento['tipo']
            
            # Adicionar nó se ainda não existe
            if estado_id not in nos_mostrados:
                G_atual.add_node(estado_id)
                nos_mostrados.add(estado_id)
                
                # Definir cor baseada no tipo de evento
                if is_last_frame[0] and estado_id in nos_solucao:
                    cor = 'red'  # Destacar nós da solução no último frame
                    tamanho = 900
                elif tipo == 'inicial':
                    cor = 'yellow'
                    tamanho = 800
                elif tipo == 'explorando':
                    cor = 'lightgreen'
                    tamanho = 700
                elif tipo == 'gerado':
                    cor = 'lightblue'
                    tamanho = 600
                elif tipo == 'rejeitado':
                    cor = 'lightgray'
                    tamanho = 500
                elif tipo == 'solucao':
                    cor = 'red'
                    tamanho = 900
                else:
                    cor = 'white'
                    tamanho = 600
                
                node_colors.append(cor)
                node_sizes.append(tamanho)
            
            # Adicionar aresta se existe pai
            if 'pai' in evento and evento['pai'] in nos_mostrados:
                pai = evento['pai']
                if (pai, estado_id) not in arestas_mostradas:
                    G_atual.add_edge(pai, estado_id)
                    arestas_mostradas.add((pai, estado_id))
                    
                    # Cor da aresta
                    if is_last_frame[0] and (pai, estado_id) in arestas_solucao:
                        edge_colors.append('red')  # Destacar arestas da solução no último frame
                    elif tipo == 'solucao':
                        edge_colors.append('red')
                    else:
                        edge_colors.append('black')
        
        # Obtendo nós e arestas do grafo atual
        nodes = list(G_atual.nodes())
        edges = list(G_atual.edges())
        
        # Configurar tamanhos dos nós garantindo que correspondam aos nós do grafo
        node_sizes_dict = {node: 600 for node in nodes}  # Tamanho padrão
        
        # Atualizar tamanhos específicos
        for i, node in enumerate(nodes):
            if i < len(node_sizes):
                node_sizes_dict[node] = node_sizes[i]
        
        # Converter para lista na ordem correta
        node_sizes_list = [node_sizes_dict[node] for node in nodes]
        
        # Configurar cores dos nós garantindo que correspondam aos nós do grafo
        node_colors_dict = {node: 'blue' for node in nodes}  # Cor padrão
        
        # Atualizar cores específicas
        for i, node in enumerate(nodes):
            if i < len(node_colors):
                node_colors_dict[node] = node_colors[i]
        
        # Converter para lista na ordem correta
        node_colors_list = [node_colors_dict[node] for node in nodes]
        
        # Configurar cores das arestas garantindo que correspondam às arestas do grafo
        edge_colors_dict = {edge: 'black' for edge in edges}  # Cor padrão
        
        # Atualizar cores específicas
        for i, edge in enumerate(edges):
            if i < len(edge_colors):
                edge_colors_dict[edge] = edge_colors[i]
        
        # Converter para lista na ordem correta
        edge_colors_list = [edge_colors_dict[edge] for edge in edges]
        
        # Configurar larguras das arestas
        edge_width = [3 if (is_last_frame[0] and edge in arestas_solucao) else 1 for edge in edges]
        
        # Desenhar grafo
        if nodes:  # Só desenhar se houver nós
            # Desenhar nós
            nx.draw_networkx_nodes(
                G_atual, 
                pos={node: pos.get(node, (0, 0)) for node in nodes},
                ax=ax,
                nodelist=nodes,
                node_color=node_colors_list,
                node_size=node_sizes_list
            )
            
            # Desenhar arestas
            if edges:  # Só desenhar se houver arestas
                nx.draw_networkx_edges(
                    G_atual, 
                    pos={node: pos.get(node, (0, 0)) for node in nodes},
                    ax=ax,
                    edgelist=edges,
                    edge_color=edge_colors_list,
                    width=edge_width
                )
            
            # Desenhar rótulos
            nx.draw_networkx_labels(
                G_atual, 
                pos={node: pos.get(node, (0, 0)) for node in nodes},
                ax=ax,
                labels={node: nos_info[node]['label'] for node in nodes},
                font_size=8,
                font_weight='bold'
            )
        
        # Título e legenda
        if is_last_frame[0]:
            ax.set_title(f"Caminho da Solução Destacado - Busca em Largura", fontsize=16)
        else:    
            ax.set_title(f"Animação da Busca em Largura - Frame {num+1}/{min(len(historico), 100)}", fontsize=16)
        ax.set_axis_off()
        
    # Criar animação sem repetição
    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=min(len(historico), 100),
        interval=500,  # 500ms entre frames
        repeat=False  # Desativar repetição
    )
    
    plt.tight_layout()
    plt.show()
    return ani

# Função principal para executar a busca com animação
def executar_busca_largura_animada():
    estado_inicial = Estado(["Bono", "Edge", "Adam", "Larry"], [], "esquerda", 0)
    caminho_solucao, historico = busca_largura_com_historico(estado_inicial)
    
    if caminho_solucao:
        print(f"Total de eventos registrados: {len(historico)}")
        print("Iniciando animação...")
        ani = animar_busca(historico)
        return caminho_solucao, historico, ani
    else:
        print("Nenhuma solução encontrada para animar.")
        return None, historico, None

# Para executar, basta chamar:
# caminho, historico, animacao = executar_busca_largura_animada()

def executar_busca_backtracking_animada():
    estado_inicial = Estado(["Bono", "Edge", "Adam", "Larry"], [], "esquerda", 0)
    estado_inicial.id = 0  # Atribui um ID único ao estado inicial
    
    # Estrutura para armazenar o histórico da busca
    historico = []
    
    # Registra o estado inicial
    historico.append({
        'tipo': 'inicial',
        'estado': estado_inicial,
        'id': estado_inicial.id
    })
    
    # Executa a busca em backtracking
    caminho_solucao = busca_backtracking_com_historico(
        estado_inicial, [estado_inicial], set(), historico
    )
    
    if caminho_solucao:
        print(f"Total de eventos registrados: {len(historico)}")
        print("Iniciando animação...")
        animar_busca(historico)
        return caminho_solucao, historico
    else:
        print("Nenhuma solução encontrada para animar.")
        return None, historico


# Execução
if __name__ == "__main__":
    modo = input("Escolha o método de busca (largura (l), profundidade (p), gulosa (g), A* (a), backtracking (b)): ").strip().lower()
    
    estado_inicial = Estado(["Bono", "Edge", "Adam", "Larry"], [], "esquerda", 0)
    
    if modo == "l":
        caminho_solucao, historico = busca_largura_com_historico(estado_inicial)
    elif modo == "p":
        caminho_solucao, historico = busca_profundidade_com_historico(estado_inicial)
    elif modo == "g":
        caminho_solucao, historico = busca_gulosa_com_historico(estado_inicial)
    elif modo == "a":
        caminho_solucao, historico = busca_aestrela_com_historico(estado_inicial)
    elif modo == "b":
        caminho_solucao, historico = executar_busca_backtracking_animada()
    else:
        print("Método inválido!")
        caminho_solucao, historico = None, None

    if caminho_solucao:
        print("Iniciando animação...")
        animar_busca(historico)
    
    print("Busca finalizada.")

# Main antiga
""" estado_inicial = Estado(["Bono", "Edge", "Adam", "Larry"], [], "esquerda", 0)

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
print("Busca finalizada.") """
