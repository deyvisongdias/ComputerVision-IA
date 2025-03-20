from collections import deque
import heapq
import time
import graphviz
from graphviz import Digraph

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
        self.lado_esquerdo = lado_esquerdo  # Lista de membros no lado esquerdo
        self.lado_direito = lado_direito  # Lista de membros no lado direito
        self.lanterna = lanterna  # Posição da lanterna ("esquerda" ou "direita")
        self.tempo = tempo  # Tempo acumulado
        self.movimento = movimento  # Guarda quem atravessou
        self.pai = pai  # Guarda referência ao estado pai
        self.id = None  # Identificador único para o estado

    def __lt__(self, outro):
        return self.tempo < outro.tempo  # Para comparação na busca

    def __repr__(self):
        movimento_str = ""
        if self.movimento:
            if self.lanterna == "esquerda":
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
        if self.lanterna == "esquerda":
            for transicao in transicoes_esquerda:
                if all(membro in self.lado_esquerdo for membro in transicao):
                    novo_lado_esquerdo = [m for m in self.lado_esquerdo if m not in transicao]
                    novo_lado_direito = self.lado_direito + list(transicao)
                    
                    # Calcular o tempo gasto para a travessia
                    tempo_gasto = 0
                    for membro in transicao:
                        for item in info:
                            if item["nome"] == membro:
                                tempo_gasto = max(tempo_gasto, item["tempo"])
                                break
                    
                    novo_estado = Estado(
                        novo_lado_esquerdo, novo_lado_direito, "direita", self.tempo + tempo_gasto, transicao, self
                    )
                    proximos_estados.append(novo_estado)
        else:
            for transicao in transicoes_direita:
                if transicao[0] in self.lado_direito:
                    novo_lado_esquerdo = self.lado_esquerdo + [transicao[0]]
                    novo_lado_direito = [m for m in self.lado_direito if m != transicao[0]]
                    
                    # Calcular o tempo gasto para o retorno
                    tempo_gasto = 0
                    for item in info:
                        if item["nome"] == transicao[0]:
                            tempo_gasto = item["tempo"]
                            break
                    
                    novo_estado = Estado(
                        novo_lado_esquerdo, novo_lado_direito, "esquerda", self.tempo + tempo_gasto, transicao, self
                    )
                    proximos_estados.append(novo_estado)
        return proximos_estados


def todos_no_lado_direito(estado):
    return len(estado.lado_esquerdo) == 0


def imprimir_caminho(caminho):
    for estado in caminho:
        print(estado)


def busca_largura_com_visualizacao(estado_inicial):
    tempo_inicial = time.time()
    fila = deque([estado_inicial])
    visitados = {}
    todos_estados = set()
    solucao = None

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

        # for prox_estado in estado_atual.gerar_proximos_estados(): -> caso não queira restringir
        for prox_estado in estado_atual.gerar_proximos_estados():
            if prox_estado.tempo > 17:
                continue
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
    visitados = {}
    todos_estados = set()
    solucao = None

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
            if prox_estado.tempo > 17:
                continue
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
    fila = [(heuristica_gulosa(estado_inicial), estado_inicial)]
    visitados = {}
    todos_estados = set()
    solucao = None

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
            heapq.heappush(fila, (heuristica_gulosa(prox_estado), prox_estado))

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
    fila = [(custo_real(estado_inicial) + heuristica_aestrela(estado_inicial), estado_inicial)]
    visitados = {}
    todos_estados = set()
    solucao = None

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
            if prox_estado.tempo > 17:
                continue
            prox_estado.pai = estado_atual
            prox_estado.id = contador_id
            contador_id += 1
            todos_estados.add(prox_estado)
            heapq.heappush(fila, (custo_real(prox_estado) + heuristica_aestrela(prox_estado), prox_estado))

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


def busca_ordenada_com_visualizacao(estado_inicial):
    tempo_inicial = time.time()
    fila = [(custo_real(estado_inicial), estado_inicial)]
    visitados = {}
    todos_estados = set()
    solucao = None

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
            if prox_estado.tempo > 17:
                continue
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


def custo_real(estado):
    return estado.tempo


def heuristica_gulosa(estado):
    # Tempo máximo de travessia dos membros no lado esquerdo
    if not estado.lado_esquerdo:
        return 0  # Todos já estão no lado direito
    max_tempo = max(membro["tempo"] for membro in info if membro["nome"] in estado.lado_esquerdo)
    return max_tempo

def heuristica_aestrela(estado):
    membros_esquerda = estado.lado_esquerdo.copy()
    tempos = [membro["tempo"] for membro in info if membro["nome"] in membros_esquerda]
    tempos.sort()  # Ordena os tempos para otimizar a travessia

    tempo_total = 0
    while len(tempos) > 1:
        # Dois membros mais rápidos atravessam
        tempo_total += max(tempos[0], tempos[1])
        # Membro mais rápido retorna
        tempo_total += tempos[0]
        # Remove os dois membros que já atravessaram
        tempos = tempos[2:]
    
    # Se sobrou um membro, ele atravessa sozinho
    if len(tempos) == 1:
        tempo_total += tempos[0]
    
    return tempo_total

def visualizar_arvore_busca(caminho_solucao, todos_estados):
    """
    Cria uma visualização da árvore de busca usando Graphviz, com o caminho solução destacado em vermelho.
    A legenda é posicionada no canto inferior direito, com o texto colorido de acordo com o que representa.
    """
    dot = graphviz.Digraph(
        format='png',
        engine='dot',
        graph_attr={'rankdir': 'TB', 'concentrate': 'true', 'overlap': 'false', 'splines': 'true'}
    )
    
    # Adicionar todos os nós sem agrupamento por nível
    for estado in todos_estados:
        label = f"Tempo: {estado.tempo}\nEsq: {', '.join(estado.lado_esquerdo)}\nDir: {', '.join(estado.lado_direito)}"
        
        # Definir cor e estilo do nó
        if estado in caminho_solucao:
            dot.node(str(estado.id), label=label, shape="box", style="filled", fillcolor="lightgreen")
        else:
            dot.node(str(estado.id), label=label, shape="box", style="filled", fillcolor="lightblue" if estado.lanterna == "direita" else "lightyellow")
    
    # Adicionar as arestas
    for estado in todos_estados:
        if estado.pai:
            # Verificar se a aresta pertence ao caminho solução
            if estado in caminho_solucao and estado.pai in caminho_solucao:
                dot.edge(str(estado.pai.id), str(estado.id), color="red", penwidth="2.0")
            else:
                dot.edge(str(estado.pai.id), str(estado.id), color="gray")
    
    # Adicionar uma legenda no canto inferior direito
    legenda_label = (
        "<<b>Legenda:</b><br/>"
        "<font color='green'>Nós verdes</font>: Caminho solução<br/>"
        "<font color='blue'>Nós azuis</font>: Lanterna no lado direito<br/>"
        "<font color='orange'>Nós amarelos</font>: Lanterna no lado esquerdo<br/>"
        "<font color='red'>Arestas vermelhas</font>: Transições no caminho solução<br/>"
        "<font color='gray'>Arestas cinzas</font>: Transições exploradas>"
    )
    dot.node(
        "legenda",
        label=legenda_label,
        shape="plaintext",  # Remove a borda da legenda
        fontsize="10",
        pos="100,0!"  # Posiciona a legenda no canto inferior direito
    )
    
    # Render e salvar o gráfico
    dot.render(view=True, cleanup=True)
    print("Visualização da árvore de busca gerada com sucesso!")
    return dot


def gerar_imagem_explicacao(resultados, melhor_algoritmo):
    """
    Gera uma imagem com a explicação dos algoritmos e o resultado da comparação.
    """
    dot = Digraph(
        format='png',
        engine='dot',
        graph_attr={'rankdir': 'TB', 'concentrate': 'true', 'overlap': 'false', 'splines': 'true'}
    )
    
    # Título da imagem
    dot.node("titulo", label="Comparação dos Algoritmos de Busca", shape="plaintext", fontsize="20", fontname="bold")
    
    # Explicação dos algoritmos
    explicacao = (
        "Explicação dos Algoritmos:\n"
        "1. Busca em Largura (BFS): Explora todos os nós nível por nível. Não usa heurística.\n"
        "2. Busca em Profundidade (DFS): Explora o máximo possível em cada ramo antes de retroceder. Não usa heurística.\n"
        "3. Busca Gulosa: Escolhe o próximo nó com base em uma heurística (menor tempo estimado para a solução).\n"
        "4. Busca A*: Combina o custo real do caminho com uma heurística (custo real + tempo estimado).\n"
        "5. Busca Ordenada: Expande os nós com base no custo real acumulado. Não usa heurística.\n"
        "6. Busca Backtracking: Explora recursivamente os caminhos, retrocedendo quando atinge um limite.\n"
    )
    dot.node("explicacao", label=explicacao, shape="plaintext", fontsize="12")
    
    # Resultados da comparação
    resultados_label = "Resultados:\n"
    for nome, dados in resultados.items():
        resultados_label += (
            f"{nome}:\n"
            f"  Tempo de execução = {dados['tempo_execucao']:.6f} segundos\n"
            f"  Estados explorados = {dados['num_estados']}\n"
        )
    resultados_label += f"\nMelhor algoritmo: {melhor_algoritmo}"
    dot.node("resultados", label=resultados_label, shape="plaintext", fontsize="12")
    
    # Conectar os nós
    dot.edge("titulo", "explicacao")
    dot.edge("explicacao", "resultados")
    
    # Renderizar e salvar a imagem
    dot.render("comparacao_algoritmos", view=True, cleanup=True)
    print("Imagem com a explicação e resultados gerada com sucesso!")


def testar_todos_os_algoritmos():
    """
    Testa todos os algoritmos de busca, explica as diferenças, heurísticas usadas,
    compara os resultados e gera uma imagem com a explicação.
    """
    estado_inicial = Estado(["Bono", "Edge", "Adam", "Larry"], [], "esquerda", 0)
    
    # Dicionário para armazenar os resultados de cada algoritmo
    resultados = {}
    
    # Funções de busca disponíveis
    algoritmos = {
        "Busca em Largura (BFS)": busca_largura_com_visualizacao,
        "Busca em Profundidade (DFS)": busca_profundidade_com_visualizacao,
        "Busca Gulosa": busca_gulosa_com_visualizacao,
        "Busca A*": busca_aestrela_com_visualizacao,
        "Busca Ordenada": busca_ordenada_com_visualizacao,
        "Busca Backtracking": busca_backtracking_com_visualizacao
    }
    
    # Testar cada algoritmo
    for nome, algoritmo in algoritmos.items():
        print(f"\nExecutando {nome}...")
        tempo_inicial = time.time()
        caminho_solucao, todos_estados = algoritmo(estado_inicial)
        tempo_execucao = time.time() - tempo_inicial
        
        if caminho_solucao:
            num_estados = len(todos_estados)
            resultados[nome] = {
                "tempo_execucao": tempo_execucao,
                "num_estados": num_estados,
                "caminho_solucao": caminho_solucao,
                "todos_estados": todos_estados
            }
            print(f"{nome} encontrou uma solução em {tempo_execucao:.6f} segundos, explorando {num_estados} estados.")
        else:
            print(f"{nome} não encontrou uma solução.")
    
    # Determinar o melhor algoritmo (menos estados explorados e menor tempo de execução)
    if resultados:
        # Ordenar por número de estados e, em caso de empate, por tempo de execução
        melhor_algoritmo = min(
            resultados.keys(),
            key=lambda x: (resultados[x]["num_estados"], resultados[x]["tempo_execucao"])
        )
        print(f"\n--- Melhor Algoritmo ---")
        print(
            f"O melhor algoritmo foi {melhor_algoritmo}, "
            f"explorando {resultados[melhor_algoritmo]['num_estados']} estados "
            f"em {resultados[melhor_algoritmo]['tempo_execucao']:.6f} segundos."
        )
        
        # Gerar a imagem com a explicação e resultados
        gerar_imagem_explicacao(resultados, melhor_algoritmo)
    else:
        print("Nenhum algoritmo encontrou uma solução.")


# Função principal para executar a busca e visualização
def executar_busca_e_visualizacao():
    while True:
        estado_inicial = Estado(["Bono", "Edge", "Adam", "Larry"], [], "esquerda", 0)
        
        print("\nEscolha o método de busca:")
        print("1. Busca em Largura (BFS)")
        print("2. Busca em Profundidade (DFS)")
        print("3. Busca Gulosa")
        print("4. Busca A*")
        print("5. Busca Ordenada")
        print("6. Busca Backtracking")
        print("7. Testar todos os algoritmos")
        print("8. Sair")
        opcao = input("Digite o número da opção desejada: ")
        
        if opcao == "8":
            print("Saindo...")
            break
        
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
        elif opcao == "7":
            testar_todos_os_algoritmos()
            continue  # Volta ao menu após testar todos os algoritmos
        else:
            print("Opção inválida! Tente novamente.")
            continue
        
        if todos_estados:
            print(f"Total de estados explorados: {len(todos_estados)}")
            
            # Visualizar a árvore de busca com todos os estados
            visualizar_arvore_busca(caminho_solucao, todos_estados)


# Executar o programa
if __name__ == "__main__":
    executar_busca_e_visualizacao()