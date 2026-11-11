
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

    def distribuir_feromonios_iniciais(self):
        for i in range(len(self.grafo.lista_adj.lista)):
            for destino, peso, feromonio in self.grafo.lista_adj.lista[i]:
                self.grafo.lista_adj.alterar_feromonio_aresta(i, destino, self.feromonios_iniciais)
            
    def distribuir_Formigas(self):
        for i in range(len(self.formigas)):
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
    
    def main_loop(self):
        self.distribuir_feromonios_iniciais()
        self.distribuir_Formigas()
        
        for _ in range(self.qntd_iter):
            for formiga in self.formigas:
                
                
                
    
        