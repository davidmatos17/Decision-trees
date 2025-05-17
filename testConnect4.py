# Usa 80% para "construir" a àrvore e 20% para testes 
from Dataset import Dataset
from DecisionTree import DecisionTree
from copy import deepcopy
import random

# Lê o dataset (sem binning e sem ID)
dataset = Dataset().readCSV('./datasets/', 'connect4_dataset', hasId=False, hasHeader=True)
random.shuffle(dataset.array)
# Divide em treino e teste 
split_point = int(0.8 * dataset.lines)
train_data = Dataset(deepcopy(dataset.array[:split_point]), deepcopy(dataset.header))
test_data = Dataset(deepcopy(dataset.array[split_point:]), deepcopy(dataset.header))

# Cria a árvore de decisão
tree = DecisionTree(train_data)

print('\nAvaliação no conjunto de teste:\n')

acertos = 0
total = test_data.lines

for i in range(total):
    previsto = tree.classifyExample(deepcopy(test_data), i)
    real = test_data.getValue(i, test_data.cols - 1)
    print(f"Linha {i+1}: Previsto = {previsto} | Real = {real}")
    if previsto == real:
        acertos += 1

print(f"\nPrecisão do conjunto de teste: {acertos}/{total} = {acertos/total*100:.2f}%")
