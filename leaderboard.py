import pickle

class Jogador:
    def __init__(self, nome, score):
        self.nome = nome
        self.score = score

def salvar_score(scores, filename):
    with open(filename, 'wb') as file:
        pickle.dump(scores, file)

def carregar_score(filename):
    try:
        with open(filename, 'rb') as file:
            scores = pickle.load(file)
        return scores
    except FileNotFoundError:
        return []
    
def mostrar_leaderboard(tela, scores):
    pass