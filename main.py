from Dataset import Dataset
from DecisionTree import DecisionTree
from copy import deepcopy
import random

irisTree = DecisionTree(Dataset().readCSV('datasets/', 'iris', hasId=True))
irisTreeBinning = DecisionTree(Dataset().readCSV('datasets/', 'iris', hasId=True, binCount=3), binning=True)
connect4Tree = DecisionTree(Dataset().readCSV('datasets/', 'connect4_dataset', hasId=False, hasHeader=True))

def chooseTree():
    print("\nEscolhe uma das árvores:")
    print("[1] Iris")
    print("[2] Iris com Binning")
    print("[3] Connect 4")
    option = input("Opção: ")

    if option == '1':
        return irisTree, 'datasets/', 'iris', True
    elif option == '2':
        return irisTreeBinning, 'datasets/', 'iris', True
    elif option == '3':
        return connect4Tree, 'datasets/', 'connect4_dataset', False
    else:
        print("Opção inválida.")
        return chooseTree()

def main():
    while True:
        print("\nÁrvores de Decisão - Algoritmo ID3")
        print("1. Ver árvore")
        print("2. Classificar ficheiro CSV")
        print("3. Calcular precisão")
        print("4. Sair")

        op = input("Escolha a opção: ")

        if op == '1':
            tree, *_ = chooseTree()
            print("\nÁrvore:")
            tree.DFSPrint()

        elif op == '2':
            tree, path, file, hasId = chooseTree()
            dataset = Dataset().readCSV(path, file, hasId=hasId, hasHeader=True)

            print("\nClassificações:")
            for i in range(dataset.lines):
                predicted = tree.classifyExample(deepcopy(dataset), i)
                print(f"Linha {i + 1}: Classe prevista = {predicted}")

        elif op == '3':
            tree, path, file, hasId = chooseTree()
            dataset = Dataset().readCSV(path, file, hasId=hasId, hasHeader=True)
            random.shuffle(dataset.array)

            split_point = int(0.8 * dataset.lines)
            train_data = Dataset(deepcopy(dataset.array[:split_point]), deepcopy(dataset.header))
            test_data = Dataset(deepcopy(dataset.array[split_point:]), deepcopy(dataset.header))

            tree = DecisionTree(train_data)

            acertos = 0
            total = test_data.lines

            for i in range(total):
                previsto = tree.classifyExample(deepcopy(test_data), i)
                real = test_data.getValue(i, test_data.cols - 1)
                if previsto == real:
                    acertos += 1

            print(f"\nPrecisão no conjunto de teste: {acertos}/{total} = {acertos / total * 100:.2f}%")

        elif op == '4':
            print("Até à próxima!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
