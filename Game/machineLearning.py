import torch
import random
import numpy as np 
from collections import deque
from Grille import Grille

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #random
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #popleft()
        #TODO: model, trainer
    
    def get_state(self, grille):
        pass
    
    def remember(self, state, action, reward, next_state, done):
        pass
    
    def train_long_memory(self):
        pass
    
    def train_short_memory(self, state, action, reward, next_state, done):
        pass
    
    def get_action(self, state):
        pass

def train():
    plot_scores=[]
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Grille()
    while True:
        # ancien etat
        state_old = agent.get_state(game)
        
        #recup move
        final_move = agent.get_action(state_old)
        
        #effectue move et recup nouveau state
        reward, done, score = game.TryDeplacement(final_move)
        state_new = agent.get_state(game)
        
        #train short memory
        agent.train_short_memory()


if __name__=='__main__':
    train()