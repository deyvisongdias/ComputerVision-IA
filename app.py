from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq
import time
import graphviz

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
    def __init__(self, lado_esquerdo, lado_direito, lanterna, tempo, movimento=None, pai=None):
        self.lado_esquerdo = lado_esquerdo  # Usar tuple para imutabilidade
        self.lado_direito = lado_direito  # Usar tuple para imutabilidade
        self.lanterna = lanterna
        self.tempo = tempo
        self.movimento = movimento  # Guarda quem atravessou
        self.pai = pai  # Guarda referência ao estado pai
        self.id = None  # Será usado para identificar o estado no grafo

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
    
    def estado_tuple(self):
        # Representação única do estado para comparações
        return (tuple(sorted(self.lado_esquerdo)), tuple(sorted(self.lado_direito)), self.lanterna, self.tempo)

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
                    novo_lado_esquerdo, novo_lado_direito, lanterna, tempo, movimento, self)

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
                    novo_lado_esquerdo, novo_lado_direito, lanterna, tempo, movimento, self)

                proximos_estados.append(novo_estado)

        return proximos_estados


def todos_no_lado_direito(estado):
    if len(estado.lado_esquerdo) == 0:
        return True
    return False


def imprimir_caminho(caminho):
    for estado in caminho:
        print(estado)


# Funções de busca modificadas para registrar todos os nós visitados
def busca_largura_com_visualizacao(estado_inicial):
    tempo_inicial = time.time()
    fila = deque([estado_inicial])
    visitados = {}  # Dicionário para manter o mapeamento estado -> pai
    todos_estados = set()  # Conjunto para armazenar todos os estados visitados
    solucao = None  # Para armazenar o estado final da solução

    contador_id = 0
    estado_inicial.id = contador_id
    contador_id += 1
    todos_estados.add(estado_inicial)

    while fila:
        estado_atual = fila.popleft()
        estado_tuple = estado_atual.estado_tuple()

        if estado_tuple in visitados:
            continue
        visitados[estado_tuple] = estado_atual.pai

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca em Largura):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            print(f"Tempo total da travessia: {estado_atual.tempo} minutos")
            solucao = estado_atual
            break

        for prox_estado in estado_atual.gerar_proximos_estados():
            prox_estado.pai = estado_atual
            prox_estado.id = contador_id
            contador_id += 1
            todos_estados.add(prox_estado)
            fila.append(prox_estado)

    if solucao is None:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        print("Nenhuma solução encontrada!")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
        return None, todos_estados
    
    # Reconstruir o caminho solução
    caminho_solucao = []
    atual = solucao
    while atual:
        caminho_solucao.append(atual)
        atual = atual.pai
    caminho_solucao.reverse()
    
    print("Caminho solução:")
    imprimir_caminho(caminho_solucao)
    
    return caminho_solucao, todos_estados


def busca_profundidade_com_visualizacao(estado_inicial):
    tempo_inicial = time.time()
    pilha = [estado_inicial]
    visitados = {}  # Dicionário para manter o mapeamento estado -> pai
    todos_estados = set()  # Conjunto para armazenar todos os estados visitados
    solucao = None  # Para armazenar o estado final da solução

    contador_id = 0
    estado_inicial.id = contador_id
    contador_id += 1
    todos_estados.add(estado_inicial)

    while pilha:
        estado_atual = pilha.pop()
        estado_tuple = estado_atual.estado_tuple()

        if estado_tuple in visitados:
            continue
        visitados[estado_tuple] = estado_atual.pai

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca em Profundidade):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            print(f"Tempo total da travessia: {estado_atual.tempo} minutos")
            solucao = estado_atual
            break

        for prox_estado in reversed(estado_atual.gerar_proximos_estados()):
            prox_estado.pai = estado_atual
            prox_estado.id = contador_id
            contador_id += 1
            todos_estados.add(prox_estado)
            pilha.append(prox_estado)

    if solucao is None:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        print("Nenhuma solução encontrada!")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
        return None, todos_estados
    
    # Reconstruir o caminho solução
    caminho_solucao = []
    atual = solucao
    while atual:
        caminho_solucao.append(atual)
        atual = atual.pai
    caminho_solucao.reverse()
    
    print("Caminho solução:")
    imprimir_caminho(caminho_solucao)
    
    return caminho_solucao, todos_estados


def busca_gulosa_com_visualizacao(estado_inicial):
    tempo_inicial = time.time()
    fila = [(heuristica(estado_inicial), estado_inicial)]
    visitados = {}  # Dicionário para manter o mapeamento estado -> pai
    todos_estados = set()  # Conjunto para armazenar todos os estados visitados
    solucao = None  # Para armazenar o estado final da solução

    contador_id = 0
    estado_inicial.id = contador_id
    contador_id += 1
    todos_estados.add(estado_inicial)

    while fila:
        _, estado_atual = heapq.heappop(fila)
        estado_tuple = estado_atual.estado_tuple()

        if estado_tuple in visitados:
            continue
        visitados[estado_tuple] = estado_atual.pai

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca Gulosa):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            print(f"Tempo total da travessia: {estado_atual.tempo} minutos")
            solucao = estado_atual
            break

        for prox_estado in estado_atual.gerar_proximos_estados():
            if prox_estado.tempo > 17:
                continue
                
            prox_estado.pai = estado_atual
            prox_estado.id = contador_id
            contador_id += 1
            todos_estados.add(prox_estado)
            
            h = heuristica(prox_estado)
            heapq.heappush(fila, (h, prox_estado))

    if solucao is None:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        print("Nenhuma solução encontrada!")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
        return None, todos_estados
    
    # Reconstruir o caminho solução
    caminho_solucao = []
    atual = solucao
    while atual:
        caminho_solucao.append(atual)
        atual = atual.pai
    caminho_solucao.reverse()
    
    print("Caminho solução:")
    imprimir_caminho(caminho_solucao)
    
    return caminho_solucao, todos_estados


def busca_aestrela_com_visualizacao(estado_inicial):
    tempo_inicial = time.time()
    fila = [(custo_real(estado_inicial) + heuristicaAestrela(estado_inicial), estado_inicial)]
    visitados = {}  # Dicionário para manter o mapeamento estado -> pai
    todos_estados = set()  # Conjunto para armazenar todos os estados visitados
    solucao = None  # Para armazenar o estado final da solução

    contador_id = 0
    estado_inicial.id = contador_id
    contador_id += 1
    todos_estados.add(estado_inicial)

    while fila:
        _, estado_atual = heapq.heappop(fila)
        estado_tuple = estado_atual.estado_tuple()

        if estado_tuple in visitados:
            continue
        visitados[estado_tuple] = estado_atual.pai

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca A*):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            print(f"Tempo total da travessia: {estado_atual.tempo} minutos")
            solucao = estado_atual
            break

        for prox_estado in estado_atual.gerar_proximos_estados():
            prox_estado.pai = estado_atual
            prox_estado.id = contador_id
            contador_id += 1
            todos_estados.add(prox_estado)
            
            f = custo_real(prox_estado) + heuristicaAestrela(prox_estado)
            heapq.heappush(fila, (f, prox_estado))

    if solucao is None:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        print("Nenhuma solução encontrada!")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
        return None, todos_estados
    
    # Reconstruir o caminho solução
    caminho_solucao = []
    atual = solucao
    while atual:
        caminho_solucao.append(atual)
        atual = atual.pai
    caminho_solucao.reverse()
    
    print("Caminho solução:")
    imprimir_caminho(caminho_solucao)
    
    return caminho_solucao, todos_estados


def custo_real(estado):
    return estado.tempo


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


def visualizar_arvore_busca(caminho_solucao, todos_estados):
    """
    Cria uma visualização da árvore de busca usando Graphviz, com o caminho solução destacado em vermelho.
    """
    dot = graphviz.Digraph(
        format='png',
        engine='dot',
        graph_attr={'rankdir': 'TB', 'concentrate': 'true', 'overlap': 'false', 'splines': 'true'}
    )
    
    # Dicionário para armazenar os estados por nível
    estados_por_nivel = {}
    
    # Primeiro, atribuir níveis aos estados
    for estado in todos_estados:
        nivel = 0
        atual = estado
        while atual.pai:
            nivel += 1
            atual = atual.pai
        
        if nivel not in estados_por_nivel:
            estados_por_nivel[nivel] = []
        estados_por_nivel[nivel].append(estado)
    
    # Adicionar todos os nós agrupados por nível para melhor visualização
    for nivel, estados in estados_por_nivel.items():
        with dot.subgraph(name=f"cluster_{nivel}") as c:
            c.attr(label=f"Nível {nivel}", color="lightgrey")
            for estado in estados:
                label = f"ID: {estado.id}\nTempo: {estado.tempo}\nEsq: {', '.join(estado.lado_esquerdo)}\nDir: {', '.join(estado.lado_direito)}"
                
                # Definir cor e estilo do nó
                if estado in caminho_solucao:
                    c.node(str(estado.id), label=label, shape="box", style="filled", fillcolor="lightgreen")
                else:
                    c.node(str(estado.id), label=label, shape="box", style="filled", fillcolor="lightblue" if estado.lanterna == "direita" else "lightyellow")
    
    # Adicionar as arestas
    for estado in todos_estados:
        if estado.pai:
            # Verificar se a aresta pertence ao caminho solução
            if estado in caminho_solucao and estado.pai in caminho_solucao:
                dot.edge(str(estado.pai.id), str(estado.id), color="red", penwidth="2.0")
            else:
                dot.edge(str(estado.pai.id), str(estado.id), color="gray")
    
    # Render e salvar o gráfico
    dot.render('arvore_busca', view=True)
    print("Visualização da árvore de busca gerada com sucesso!")
    return dot


def busca_ordenada_com_visualizacao(estado_inicial):
    tempo_inicial = time.time()
    fila = [(custo_real(estado_inicial), estado_inicial)]
    visitados = {}  # Dicionário para manter o mapeamento estado -> pai
    todos_estados = set()  # Conjunto para armazenar todos os estados visitados
    solucao = None  # Para armazenar o estado final da solução

    contador_id = 0
    estado_inicial.id = contador_id
    contador_id += 1
    todos_estados.add(estado_inicial)

    while fila:
        _, estado_atual = heapq.heappop(fila)
        estado_tuple = estado_atual.estado_tuple()

        if estado_tuple in visitados:
            continue
        visitados[estado_tuple] = estado_atual.pai

        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            tempo_final = time.time()
            tempoTotal = tempo_final - tempo_inicial
            print("Solução encontrada (Busca Ordenada):")
            print(f"Tempo de execução: {tempoTotal:.6f} segundos")
            print(f"Tempo total da travessia: {estado_atual.tempo} minutos")
            solucao = estado_atual
            break

        for prox_estado in estado_atual.gerar_proximos_estados():
            prox_estado.pai = estado_atual
            prox_estado.id = contador_id
            contador_id += 1
            todos_estados.add(prox_estado)
            
            heapq.heappush(fila, (custo_real(prox_estado), prox_estado))

    if solucao is None:
        tempo_final = time.time()
        tempoTotal = tempo_final - tempo_inicial
        print("Nenhuma solução encontrada!")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
        return None, todos_estados
    
    # Reconstruir o caminho solução
    caminho_solucao = []
    atual = solucao
    while atual:
        caminho_solucao.append(atual)
        atual = atual.pai
    caminho_solucao.reverse()
    
    print("Caminho solução:")
    imprimir_caminho(caminho_solucao)
    
    return caminho_solucao, todos_estados


def busca_backtracking_com_visualizacao(estado_inicial):
    tempo_inicial = time.time()
    visitados = {}
    todos_estados = set()
    solucao = [None]  # Lista para armazenar a solução, usamos lista para que possa ser modificada dentro da função recursiva
    
    contador_id = 0
    estado_inicial.id = contador_id
    contador_id += 1
    todos_estados.add(estado_inicial)
    
    def backtracking_recursivo(estado_atual, id_count):
        if estado_atual.tempo > 17:
            return False, id_count
        
        estado_tuple = estado_atual.estado_tuple()
        if estado_tuple in visitados:
            return False, id_count
        
        visitados[estado_tuple] = estado_atual.pai
        
        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            solucao[0] = estado_atual
            return True, id_count
        
        for prox_estado in estado_atual.gerar_proximos_estados():
            prox_estado.pai = estado_atual
            prox_estado.id = id_count
            id_count += 1
            todos_estados.add(prox_estado)
            
            encontrou, new_id_count = backtracking_recursivo(prox_estado, id_count)
            id_count = new_id_count
            
            if encontrou:
                return True, id_count
        
        visitados.pop(estado_tuple)
        return False, id_count
    
    encontrou, _ = backtracking_recursivo(estado_inicial, contador_id)
    
    tempo_final = time.time()
    tempoTotal = tempo_final - tempo_inicial
    
    if not encontrou:
        print("Nenhuma solução encontrada (Backtracking)!")
        print(f"Tempo de execução: {tempoTotal:.6f} segundos")
        return None, todos_estados
    
    # Reconstruir o caminho solução
    caminho_solucao = []
    atual = solucao[0]
    while atual:
        caminho_solucao.append(atual)
        atual = atual.pai
    caminho_solucao.reverse()
    
    print("Solução encontrada (Backtracking):")
    print(f"Tempo de execução: {tempoTotal:.6f} segundos")
    print(f"Tempo total da travessia: {solucao[0].tempo} minutos")
    print("Caminho solução:")
    imprimir_caminho(caminho_solucao)
    
    return caminho_solucao, todos_estados


# Limita o número de estados para visualização
def limitar_estados_para_visualizacao(todos_estados, limite=500):
    """
    Limita o número de estados para visualização para evitar gráficos muito grandes.
    Mantém os estados de menor ID (provavelmente explorando mais próximo da raiz).
    """
    if len(todos_estados) <= limite:
        return todos_estados
    
    return sorted(todos_estados, key=lambda x: x.id)[:limite]


# Função principal para executar a busca e visualização
def executar_busca_e_visualizacao():
    estado_inicial = Estado(["Bono", "Edge", "Adam", "Larry"], [], "esquerda", 0)
    
    print("Escolha o método de busca:")
    print("1. Busca em Largura (BFS)")
    print("2. Busca em Profundidade (DFS)")
    print("3. Busca Gulosa")
    print("4. Busca A*")
    print("5. Busca Ordenada")
    print("6. Busca Backtracking")
    opcao = input("Digite o número da opção desejada: ")
    
    caminho_solucao = None
    todos_estados = None
    
    if opcao == "1":
        caminho_solucao, todos_estados = busca_largura_com_visualizacao(estado_inicial)
    elif opcao == "2":
        caminho_solucao, todos_estados = busca_profundidade_com_visualizacao(estado_inicial)
    elif opcao == "3":
        caminho_solucao, todos_estados = busca_gulosa_com_visualizacao(estado_inicial)
    elif opcao == "4":
        caminho_solucao, todos_estados = busca_aestrela_com_visualizacao(estado_inicial)
    elif opcao == "5":
        caminho_solucao, todos_estados = busca_ordenada_com_visualizacao(estado_inicial)
    elif opcao == "6":
        caminho_solucao, todos_estados = busca_backtracking_com_visualizacao(estado_inicial)
    else:
        print("Opção inválida!")
        return
    
    if todos_estados:
        print(f"Total de estados explorados: {len(todos_estados)}")
        # Limitar estados para visualização se forem muitos
        limite_estados = 500
        if len(todos_estados) > limite_estados:
            print(f"Limitando a visualização para {limite_estados} estados mais próximos da raiz.")
            estados_visualizacao = limitar_estados_para_visualizacao(todos_estados, limite_estados)
        else:
            estados_visualizacao = todos_estados
        
        # Visualizar a árvore de busca
        visualizar_arvore_busca(caminho_solucao, estados_visualizacao)


# Executar o programa
if __name__ == "__main__":
    executar_busca_e_visualizacao()