import pygame
import pickle

class Jogador:
    def __init__(self, nome, score):
        self.nome = nome
        self.score = score

def salvar_score(score, filename):
    with open(filename, 'wb') as file:
        pickle.dump(score, file)

def carregar_score()