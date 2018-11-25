from math import sqrt

def euclidiana(base, usuario1, usuario2):
    si = {}
    for item in base[usuario1]:
       if item in base[usuario2]: si[item] = 1

    if len(si) == 0: return 0

    soma = sum([pow(base[usuario1][item] - base[usuario2][item], 2)
                for item in base[usuario1] if item in base[usuario2]])
    return 1/(1 + sqrt(soma))

def getSimilares(base, usuario):
    similaridade = [(euclidiana(base, usuario, outro), outro)
                    for outro in base if outro != usuario]
    similaridade.sort()
    similaridade.reverse()
    return similaridade[0:30]
    
def getRecomendacoesUsuario(base, usuario):
    totais={}
    somaSimilaridade={}
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
    rankings=[(total / somaSimilaridade[item], item) for item, total in totais.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[0:30]
                
def carregaMovieLens(path='/home/eduviictor/Documentos/Inteligência Artificial/Sistema de Recomendação/ml-100k'):
    filmes = {}
    for linha in open(path + '/u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo
    # print(filmes)

    base = {}
    for linha in open(path + '/u.data'):
        (usuario, idfilme, nota, tempo) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idfilme]] = float(nota)
    return base            

def calculaItensSimilares(base):
    result = {}
    for item in base:
        notas = getSimilares(base, item)
        result[item] = notas
    return result

def getRecomendacoesItens(baseUsuario, similaridadeItens, usuario):
    notasUsuario = baseUsuario[usuario]
    notas={}
    totalSimilaridade={}
    for (item, nota) in notasUsuario.items():
        for (similaridade, item2) in similaridadeItens[item]:
            if item2 in notasUsuario: continue
            notas.setdefault(item2, 0)
            notas[item2] += similaridade * nota
            totalSimilaridade.setdefault(item2,0)
            totalSimilaridade[item2] += similaridade
    rankings=[(score/totalSimilaridade[item], item) for item, score in notas.items()]
    rankings.sort()
    rankings.reverse()
    return rankings
        




print("Bem vindo ao sistema de recomendação de filmes")
print("O que deseja fazer?\n")
print("1 - Busca por usuários similares")
print("2 - Busca por itens similares")
print("3 - Pedir recomendação de itens por usuário")
print("4 - Pedir recomendação por item")
escMenu = int(input("\nInforme sua escolha: "))

if escMenu == 1:
    base = carregaMovieLens()
    user = input("Informe o id do usuário que deseja pegar como base: ")
    result = getSimilares(base, user)
    print(result)
elif escMenu == 2:
    base = carregaMovieLens()
    result = calculaItensSimilares(base)
    print(result)    
elif escMenu == 3:
    base = carregaMovieLens()
    user = input("Informe o id do usuário que deseja recomendar os filmes: ")
    result = getRecomendacoesUsuario(base, user)
    print(result)
