
import random

class vertice:
    def __init__(self, nome) -> None:
        self.nome = nome
        
class lista_adj:
    def __init__(self, numero_vertices) -> None:
        self.lista = [[] for _ in range(numero_vertices)]
        
    def adicionar_aresta(self,saida, destino, peso):
        self.lista[saida].append((destino, peso, 0)) # (destino, peso, feromonio)
        self.lista[destino].append((saida, peso, 0))
        
    def alterar_feromonio_aresta(self, saida, destino, delta_alteracao):
        for i, (v, peso, feromonio) in enumerate(self.lista[saida]):
            if v == destino:
                self.lista[saida][i] = (v, peso, feromonio + delta_alteracao)
                break

        for i, (v, peso, feromonio) in enumerate(self.lista[destino]):
            if v == saida:
                self.lista[destino][i] = (v, peso, feromonio + delta_alteracao)
                break

class Formiga:
    def __init__(self, vertice_atual) -> None:
        self.vertice_atual = vertice_atual
        self.percurso = []
        self.visitados = set()
        self.distancia_percorrida = 0

class Grafo:
    def __init__(self, vertices, lista_adj : lista_adj, origem) -> None:
        self.vertices = vertices
        self.lista_adj = lista_adj
        self.origem = origem
        
class colonia_Formigas:
    def __init__(self, grafo : Grafo, quantidade_Formigas, quantidade_iteracoes, feromonios_iniciais, alfa, beta, tx_evaporacao, constate_atualizacao, maxIter) -> None:
        self.grafo = grafo
        self.formigas = [Formiga(0) for _ in range(quantidade_Formigas)]
        self.qntd_iter = quantidade_iteracoes
        self.feromonios_iniciais = feromonios_iniciais 
        self.alfa = alfa
        self.beta = beta
        self.taxa_evaporacao = tx_evaporacao
        self.Q = constate_atualizacao

    def distribuir_feromonios_iniciais(self):
        for i in range(len(self.grafo.lista_adj.lista)):
            for destino, peso, feromonio in self.grafo.lista_adj.lista[i]:
                if i < destino:
                    self.grafo.lista_adj.alterar_feromonio_aresta(i, destino, self.feromonios_iniciais)
            
    def distribuir_Formigas(self):
        for i in range(len(self.formigas)):
            self.formigas[i].percurso.clear()
            self.formigas[i].visitados.clear()
            self.formigas[i].distancia_percorrida = 0

            idx_aleatorio = random.randrange(0, len(self.grafo.vertices))
            self.formigas[i].vertice_atual = idx_aleatorio
            self.formigas[i].visitados.add(idx_aleatorio)
            self.formigas[i].percurso.append(idx_aleatorio)
    
    def calcular_heuristica(self, distancia): #inverso da distancia, isto é, distancia menores resultam numa maior preferencia
        if distancia == 0:
            return 0
        return 1 / distancia
    
    def calcular_probabilidade(self, lista_adj_r, peso_rs, feromonio_rs):
        numerador = (feromonio_rs ** self.alfa) * (
            self.calcular_heuristica(peso_rs) ** self.beta
        )
        denominador = sum(
            (fer ** self.alfa) * (self.calcular_heuristica(dist) ** self.beta)
            for _, dist, fer in lista_adj_r
        )
        if denominador == 0:
            return 0
        return numerador / denominador

    def atualizar_feromonios(self):
        # EVAPORACAO
        for i in range(len(self.grafo.lista_adj.lista)):
            for j, (destino, peso, feromonio) in enumerate(self.grafo.lista_adj.lista[i]):
                novo_feromonio = feromonio * (1 - self.taxa_evaporacao)
                self.grafo.lista_adj.lista[i][j] = (destino, peso, novo_feromonio)

        # DEPOSITO
        for formiga in self.formigas:
            if len(formiga.percurso) != len(self.grafo.vertices) or formiga.distancia_percorrida <= 0:
                # percurso invalido
                continue
            delta_feromonio = self.Q / formiga.distancia_percorrida

            for i in range(len(formiga.percurso) - 1):
                saida = formiga.percurso[i]
                destino = formiga.percurso[i + 1]

                self.grafo.lista_adj.alterar_feromonio_aresta(saida, destino, delta_feromonio)
    
    def main_loop(self):
        melhor_distancia_global = float('inf')
        melhor_caminho_global = []
        self.distribuir_feromonios_iniciais()
        
        for _ in range(self.qntd_iter):
            self.distribuir_Formigas()
            for formiga in self.formigas:
                while(len(formiga.visitados) < len(self.grafo.vertices)):
                    v_atual = formiga.percurso[-1]

                    vizinhos_validos = [
                        (viz, dist, fer) 
                        for viz, dist, fer in self.grafo.lista_adj.lista[v_atual] 
                        if viz not in formiga.visitados
                    ]

                    if not vizinhos_validos:
                        break

                    cidades_candidatas = []
                    probabilidades = []
                    for cidade, peso, feromonio in vizinhos_validos:
                        prob = self.calcular_probabilidade(vizinhos_validos, peso, feromonio)
                        cidades_candidatas.append(cidade)
                        probabilidades.append(prob)

                    proxima_cidade = random.choices(cidades_candidatas, weights=probabilidades, k=1)[0]

                    formiga.percurso.append(proxima_cidade)
                    formiga.visitados.add(proxima_cidade)

                if len(formiga.visitados) != len(self.grafo.vertices):
                    continue

                formiga.percurso.append(formiga.percurso[0])
                
                dist = 0
                for i in range(len(formiga.percurso) - 1):
                    saida = formiga.percurso[i]
                    destino = formiga.percurso[i + 1]

                    for vizinho, peso, feromonio in self.grafo.lista_adj.lista[saida]:
                        if vizinho == destino:
                            dist += peso
                            break

                formiga.distancia_percorrida = dist
                
                if dist < melhor_distancia_global:
                    melhor_distancia_global = dist
                    melhor_caminho_global = formiga.percurso.copy()

            self.atualizar_feromonios()

        return melhor_caminho_global, melhor_distancia_global

if __name__ == "__main__":

    vertices = [vertice(i) for i in range(8)]
    estrutura_adj = lista_adj(len(vertices))

    arestas = [
        (0, 1, 4),
        (0, 2, 2),
        (0, 3, 7),
        (0, 4, 3),
        (0, 5, 8),
        (0, 6, 6),
        (0, 7, 5),
        (1, 2, 1),
        (1, 3, 5),
        (1, 4, 6),
        (1, 5, 7),
        (1, 6, 4),
        (1, 7, 8),
        (2, 3, 3),
        (2, 4, 6),
        (2, 5, 4),
        (2, 6, 7),
        (2, 7, 5),
        (3, 4, 2),
        (3, 5, 2),
        (3, 6, 6),
        (3, 7, 4),
        (4, 5, 3),
        (4, 6, 5),
        (4, 7, 7),
        (5, 6, 1),
        (5, 7, 5),
        (6, 7, 2),
    ]

    for origem, destino, distancia in arestas:
        estrutura_adj.adicionar_aresta(origem, destino, distancia)

    grafo = Grafo(vertices, estrutura_adj, origem=0)


    aco = colonia_Formigas(
        grafo=grafo,
        quantidade_Formigas=20,
        quantidade_iteracoes=100,
        feromonios_iniciais=1.0,
        alfa=1.0,
        beta=2.0,
        tx_evaporacao=0.5,
        constate_atualizacao=100,
        maxIter=100
    )

    melhor_caminho, melhor_distancia = aco.main_loop()

    print("Melhor caminho:", melhor_caminho)
    print("Distancia total:", melhor_distancia)