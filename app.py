from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# Tempos de travessia de cada membro da banda
tempos = [1, 2, 5, 10]  # Bono: 1, Edge: 2, Adam: 5, Larry: 10
nomes = ["Bono", "Edge", "Adam", "Larry"]

class Estado:
    def __init__(self, lado_a, lanterna, tempo, movimento=None, voltou=False):
        self.lado_a = tuple(lado_a)  # Usar tuple para imutabilidade
        self.lanterna = lanterna
        self.tempo = tempo
        self.movimento = movimento  # Guarda quem atravessou
        self.voltou = voltou  # Indica se foi um retorno

    def __lt__(self, outro):
        return self.tempo < outro.tempo  # Para comparação na busca

    def __repr__(self):
        movimento_str = ""
        if self.movimento:
            if self.voltou:
                movimento_str = f" <- {' e '.join(self.movimento)} voltou"
            else:
                movimento_str = f" -> {' e '.join(self.movimento)} foram"
        
        return f"Tempo: {self.tempo}, Lanterna no lado {'A' if self.lanterna else 'B'}, " \
               f"Membros no lado A: {self.lado_a}{movimento_str}"

    def gerar_proximos_estados(self):
        proximos_estados = []
        lado_atual = [i for i, presente in enumerate(self.lado_a) if presente == self.lanterna]
        
        # Duas pessoas atravessam para o outro lado
        for i in range(len(lado_atual)):
            for j in range(i + 1, len(lado_atual)):
                novo_lado_a = list(self.lado_a)
                novo_lado_a[lado_atual[i]] = not novo_lado_a[lado_atual[i]]
                novo_lado_a[lado_atual[j]] = not novo_lado_a[lado_atual[j]]
                novo_tempo = self.tempo + max(tempos[lado_atual[i]], tempos[lado_atual[j]])
                
                if novo_tempo <= 17:  # Garante que não ultrapassa o tempo limite
                    movimento = [nomes[lado_atual[i]], nomes[lado_atual[j]]]
                    novo_estado = Estado(novo_lado_a, not self.lanterna, novo_tempo, movimento, voltou=False)
                    proximos_estados.append(novo_estado)
                    
                    # Agora, uma pessoa deve voltar com a lanterna, se necessário
                    lado_b = [k for k in range(4) if not novo_lado_a[k]]
                    if not novo_estado.lanterna and lado_b:  # A lanterna está no lado B e há pessoas para voltar
                        for k in lado_b:
                            if tempos[k] + novo_tempo <= 17:  # Garante que o retorno não ultrapasse o tempo limite
                                lado_retorno = list(novo_lado_a)
                                lado_retorno[k] = True  # Volta para o lado A
                                tempo_retorno = novo_tempo + tempos[k]
                                movimento_retorno = [nomes[k]]
                                proximos_estados.append(Estado(lado_retorno, True, tempo_retorno, movimento_retorno, voltou=True))
        
        return proximos_estados

def todos_no_lado_b(estado):
    return all(not membro for membro in estado.lado_a)

def imprimir_caminho(caminho):
    for estado in caminho:
        print(estado)

def busca_largura(estado_inicial):
    fila = deque([[estado_inicial]])
    visitados = set()
    
    while fila:
        caminho = fila.popleft()
        estado_atual = caminho[-1]
        
        estado_tuple = (estado_atual.lado_a, estado_atual.lanterna)
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)
        
        if todos_no_lado_b(estado_atual) and estado_atual.tempo == 17:
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
    
    estado_tuple = (estado_atual.lado_a, estado_atual.lanterna)
    if estado_tuple in visitados:
        return None
    visitados.add(estado_tuple)
    
    if todos_no_lado_b(estado_atual) and estado_atual.tempo == 17:
        print("Solução encontrada (Backtracking):")
        imprimir_caminho(caminho)
        return caminho
    
    for prox_estado in estado_atual.gerar_proximos_estados():
        resultado = busca_backtracking(prox_estado, caminho + [prox_estado], visitados)
        if resultado:
            return resultado
    
    visitados.remove(estado_tuple)
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
estado_inicial = Estado([True, True, True, True], True, 0)
modo = input("Escolha o método de busca (largura ou backtracking): ").strip().lower()
if modo == "largura":
    caminho_solucao = busca_largura(estado_inicial)
elif modo == "backtracking":
    caminho_solucao = busca_backtracking(estado_inicial, [estado_inicial], set())
else:
    print("Método inválido!")
    caminho_solucao = None

if caminho_solucao:
    desenhar_grafo(caminho_solucao)
print("Busca finalizada.")