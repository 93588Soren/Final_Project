import numpy as np
import pandas as pd 
from math import sqrt



class Rock:
    # Add composition to the constructor, defaulting to an empty dict
    def __init__(self, id, color, composition=None):
        self.id = id
        self.color = color
        self.composition = composition if composition is not None else {}

# Training Data
training_data = [
    Rock(id=1, color="Pink", composition={"Quartz": 75, "Feldspar": 15, "Mafic": 10}),
    Rock(id=2, color="Pink", composition={"Quartz": 68, "Feldspar": 22, "Mafic": 10}),
    Rock(id=3, color="Gray", composition={"Quartz": 35, "Feldspar": 50, "Mafic": 15}),
    Rock(id=4, color="Gray", composition={"Quartz": 40, "Feldspar": 45, "Mafic": 15}),
    Rock(id=5, color="Gray", composition={"Quartz": 40, "Feldspar": 45, "Mafic": 15}),
    Rock(id=6, color="Black", composition={"Quartz": 5, "Feldspar": 55, "Mafic": 40}),
    Rock(id=7, color="Black", composition={"Quartz": 0, "Feldspar": 15, "Mafic": 85}),
    Rock(id=8, color="Black", composition={"Quartz": 2, "Feldspar": 8, "Mafic": 90}),
]



def calculate_distance():
    for rock in training_data:
       
       
