avaliacoesUsuario = {'Ana': 
		{'Freddy x Jason': 2.5, 
		 'O Ultimato Bourne': 3.5,
		 'Star Trek': 3.0, 
		 'Exterminador do Futuro': 3.5, 
		 'Norbit': 2.5, 
		 'Star Wars': 3.0},
	 
	  'Marcos': 
		{'Freddy x Jason': 3.0,
		 'O Ultimato Bourne': 3.5, 
		 'Star Trek': 1.5, 
		 'Exterminador do Futuro': 5.0, 
		 'Star Wars': 3.0, 
		 'Norbit': 3.5}, 

	  'Pedro': 
	    {'Freddy x Jason': 2.5, 
		 'O Ultimato Bourne': 3.0,
		 'Exterminador do Futuro': 3.5, 
		 'Star Wars': 4.0},
			 
	  'Claudia': 
		{'O Ultimato Bourne': 3.5, 
		 'Star Trek': 3.0,
		 'Star Wars': 4.5, 
		 'Exterminador do Futuro': 4.0, 
		 'Norbit': 2.5},
				 
	  'Adriano': 
		{'Freddy x Jason': 3.0, 
		 'O Ultimato Bourne': 4.0, 
		 'Star Trek': 2.0, 
		 'Exterminador do Futuro': 3.0, 
		 'Star Wars': 3.0,
		 'Norbit': 2.0}, 

	  'Janaina': 
	     {'Freddy x Jason': 3.0, 
	      'O Ultimato Bourne': 4.0,
	      'Star Wars': 3.0, 
	      'Exterminador do Futuro': 5.0, 
	      'Norbit': 3.5},
			  
	  'Leonardo': 
	    {'O Ultimato Bourne':4.5,
             'Norbit':1.0,
	     'Exterminador do Futuro':4.0}
}
        
    
from math import sqrt
#distancia = √(sum(x1 - x2)²)

#Função euclidiana que calcula a distância entre dois pontos
def euclidiana(base, usuario1, usuario2):
    si = {}
    for item in base[usuario1]:
       if item in base[usuario2]: si[item] = 1

    if len(si) == 0: return 0

    soma = sum([pow(base[usuario1][item] - base[usuario2][item], 2)
                for item in base[usuario1] if item in base[usuario2]])
    return 1/(1 + sqrt(soma))

#Função para pegar usuários similares com base no parâmetro usuário
def getSimilares(base, usuario):
    similaridade = [(euclidiana(base, usuario, outro), outro)
                    for outro in base if outro != usuario]
    similaridade.sort()
    similaridade.reverse()
    return similaridade
    
#Função para recomendar filmes com base no parâmetro usuário
def getRecomendacoesUsuario(base, usuario):
    totais = {}
    somaSimilaridade = {}
    for outro in base:
        if outro == usuario: continue
        similaridade = euclidiana(base, usuario, outro)

        if similaridade <= 0: continue

        for item in base[outro]:
            if item not in base[usuario]:
                totais.setdefault(item, 0)
                totais[item] += base[outro][item] * similaridade
                somaSimilaridade.setdefault(item, 0)
                somaSimilaridade[item] += similaridade
    rankings = [(total / somaSimilaridade[item], item) for item, total in totais.items()]
    rankings.sort()
    rankings.reverse()
    return rankings
                
#Função para carregar base de dados 
#Deve-se alterar o path para o caminho certo da maquina
def carregaMovieLens(path = '/home/eduviictor/Documentos/Inteligência Artificial/Sistema de Recomendação/Final/ml-latest-small'):
    filmes = {}
    for linha in open(path + '/movies.txt'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo
    # print(filmes)
    base = {}
    for linha in open(path + '/ratings.txt'):
        (usuario, idfilme, nota, tempo) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idfilme]] = float(nota)
    return base            

def printLista(lista):
    for item in lista:
        print(item)

print("Bem vindo ao sistema de recomendação de filmes - Euclidiana")
print("O que deseja fazer?\n")
print("1 - Busca por usuários similares")
print("2 - Pedir recomendação de itens para usuário")
escMenu = int(input("\nInforme sua escolha: "))

if escMenu == 1:
    base = carregaMovieLens()
    user = input("Informe o id do usuário que deseja pegar como base: ")
    result = getSimilares(base, user)
    printLista(result)
elif escMenu == 2:
    base = carregaMovieLens()
    user = input("Informe o id do usuário que deseja recomendar os filmes: ")
    result = getRecomendacoesUsuario(base, user)
    printLista(result)