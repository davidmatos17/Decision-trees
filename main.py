from Dataset import Dataset
from DecisionTree import DecisionTree
from copy import deepcopy

# Geração do header para Connect Four (coluna-linha)
def genHeader():
    header = []
    for col in range(7):
        for row in range(6):
            header.append(f"{col}-{row}")
    return header

# Árvores de decisão geradas a partir de datasets
irisTree = DecisionTree(Dataset().readCSV('datasets/', 'iris', hasId=True))
irisTreeBinning = DecisionTree(Dataset().readCSV('datasets/', 'iris', hasId=True, binCount=3), binning=True)
connect4Tree = DecisionTree(Dataset().readCSV('datasets/', 'connect4_dataset', hasId=False, hasHeader=True))

def chooseTree():
    print("\nEscolhe uma das árvores:")
    print("[1] Iris")
    print("[2] Iris com Binning")
    print("[3] Connect 4 (Experimental)")
    option = input("Opção: ")

    if option == '1':
        return irisTree
    elif option == '2':
        return irisTreeBinning
    elif option == '3':
        return connect4Tree
    else:
        print("❌ Opção inválida.")
        return chooseTree()

def main():
    while True:
        print("\nÁrvores de Decisão - Algoritmo ID3")
        print("1. Ver árvore")
        print("2. Classificar ficheiro CSV")
        print("3. Sair")

        op = input("Escolha a opção: ")

        if op == '1':
            tree = chooseTree()
            print("\nÁrvore:")
            tree.DFSPrint()

        elif op == '2':
            tree = chooseTree()
            path = input("Caminho para o ficheiro (ex: 'datasets/'): ")
            file = input("Nome do ficheiro (sem .csv): ")
            dataset = Dataset().readCSV(path, file, hasId=False, hasHeader=True)

            print("\n Classificações:")
            for i in range(dataset.lines):
                predicted = tree.classifyExample(deepcopy(dataset), i)
                print(f"Linha {i + 1}: Classe prevista = {predicted}")

        elif op == '3':
            print("Até à próxima!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
