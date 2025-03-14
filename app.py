from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

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

        if(self.lanterna == "esquerda"):
            for transicao in transicoes_esquerda:
                lado_atual = self.lado_esquerdo.copy()

                for membro in lado_atual:
                    if(membro in transicao):
                        lado_atual.remove(membro)
                        for outro_membro in lado_atual:
                            if(outro_membro in transicao):
                                if(transicao not in transicoes):
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
                    if(membro.get("nome") == transicao[0] or membro.get("nome") == transicao[1]):
                        tempo_gasto = max(tempo_gasto, membro.get("tempo"))
                        movimento.append(membro.get("nome"))
                
                tempo = tempo + tempo_gasto
                
                novo_estado = Estado(novo_lado_esquerdo, novo_lado_direito, lanterna, tempo, movimento)

                proximos_estados.append(novo_estado)

        if(self.lanterna == "direita"):
            lado_atual = self.lado_direito.copy()

            for transicao in transicoes_direita:
                for membro in lado_atual:
                    if(membro in transicao):
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
                    if(membro.get("nome") == transicao[0]):
                        tempo = tempo + membro.get("tempo")
                        movimento.append(membro.get("nome"))
                
                novo_estado = Estado(novo_lado_esquerdo, novo_lado_direito, lanterna, tempo, movimento)

                proximos_estados.append(novo_estado)
        
        return proximos_estados

def todos_no_lado_direito(estado):
    if(len(estado.lado_esquerdo) == 0):
        return True    
    return False

def imprimir_caminho(caminho):
    for estado in caminho:
        print(estado)

def busca_largura(estado_inicial):
    fila = deque([[estado_inicial]])
    visitados = []
    
    while fila:
        caminho = fila.popleft()
        estado_atual = caminho[-1]
        
        estado_tuple = (estado_atual.lado_esquerdo, estado_atual.lado_direito, estado_atual.lanterna)
        if estado_tuple in visitados:
            continue
        visitados.append(estado_tuple)
        
        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            print("Solução encontrada (Busca em Largura):")
            imprimir_caminho(caminho)
            return caminho
        
        for prox_estado in estado_atual.gerar_proximos_estados():
            fila.append(caminho + [prox_estado])
    
    print("Nenhuma solução encontrada!")
    return None

def busca_backtracking(estado_atual, caminho, visitados):
    if estado_atual.tempo > 17:
        return None
    
    estado_tuple = (estado_atual.lado_esquerdo, estado_atual.lanterna)
    if estado_tuple in visitados:
        return None
    visitados.append(estado_tuple)
    
    if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
        print("Solução encontrada (Backtracking):")
        imprimir_caminho(caminho)
        return caminho
    
    for prox_estado in estado_atual.gerar_proximos_estados():
        resultado = busca_backtracking(prox_estado, caminho + [prox_estado], visitados)
        if resultado:
            return resultado
    
    visitados.remove(estado_tuple)
    return None


def busca_profundidade(estado_inicial):
    pilha = [[estado_inicial]]
    visitados = set()
    
    while pilha:
        caminho = pilha.pop()
        estado_atual = caminho[-1]
        
        estado_tuple = (tuple(estado_atual.lado_esquerdo), tuple(estado_atual.lado_direito), estado_atual.lanterna)
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)
        
        if todos_no_lado_direito(estado_atual) and estado_atual.tempo <= 17:
            print("Solução encontrada (Busca em Profundidade):")
            imprimir_caminho(caminho)
            return caminho
        
        for prox_estado in reversed(estado_atual.gerar_proximos_estados()):
            pilha.append(caminho + [prox_estado])
    
    print("Nenhuma solução encontrada!")
    return None


def desenhar_grafo(caminho):
    G = nx.DiGraph()
    labels = {}
    cores = []
    
    for i, estado in enumerate(caminho):
        lado_a = [nomes[j] for j, presente in enumerate(estado.lado_a) if presente]
        lado_b = [nomes[j] for j, presente in enumerate(estado.lado_a) if not presente]
        labels[i] = f"Tempo: {estado.tempo}m\nLado A: {', '.join(lado_a)}\nLado B: {', '.join(lado_b)}"
        
        G.add_node(i, label=labels[i])
        cores.append("lightgreen" if estado.voltou else "lightblue")
        
        if i > 0:
            G.add_edge(i - 1, i)
    
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color=cores, edge_color="gray", font_size=10, font_weight="bold")
    plt.title("Grafo da solução da travessia da banda U2")
    plt.show()

# Execução
estado_inicial = Estado(["Bono", "Edge", "Adam", "Larry"], [], "esquerda", 0)

modo = input("Escolha o método de busca (largura (l), backtracking (b) ou profundidade (p)): ").strip().lower()
if modo == "l":
    caminho_solucao = busca_largura(estado_inicial)
elif modo == "b":
    caminho_solucao = busca_backtracking(estado_inicial, [estado_inicial], [])
elif modo == "p":
    caminho_solucao = busca_profundidade(estado_inicial)
else:
    print("Método inválido!")
    caminho_solucao = None

if caminho_solucao:
    desenhar_grafo(caminho_solucao)
print("Busca finalizada.")