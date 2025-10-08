from random import random

"""
Nombre de sommets
5
Sommets
0
1
2
3
4
Nombre d aretes
6
Aretes
0 1
3 2
4 1
0 3
4 2
1 2
"""


# Prend une liste de couples (u, v) et renvoie une liste d'adjacences
def couples_vers_liste_adjacences(V, couples):
    E = {v: [] for v in V}
    for u, v in couples:
        E[u].append(v)
        E[v].append(u)
    return E


# Fonction qui prend un nom de fichier et qui renvoie V, E
def lire_instance(nom_fichier):
    with open(nom_fichier, 'r') as fd:
        # On extrait le nombre de sommets
        fd.readline()
        n = int(fd.readline())
        # On extrait les sommets
        fd.readline()
        V = [int(fd.readline()) for i in range(5)]
        # On extrait le nombre d'arêtes
        fd.readline()
        m = int(fd.readline())
        # On extrait les couples
        fd.readline()
        couples = [tuple(map(int, fd.readline().split())) for _ in range(m)]
        # On transforme nos couples en listes d'adjacences
        # (qui sera un dictionnaire de listes)
        E = couples_vers_liste_adjacences(V, couples)
    return V, E


# Prend un sommet v, et renvoie V, E auquel on a enlevé v
def supprimer_sommet(V, E, v):
    V2 = [v2 for v2 in V if v2!=v]
    E2 = {v2: l for v2, l in E.items() if v2!=v}
    for v2 in V2:
        E2[v2] = [v2 for v2 in E2[v2] if v2!=v]
    return V2, E2


# Prend un ensemble W de sommets, et renvoie V, E auquel on a enlevé les sommets de W
def supprimer_sommets(V, E, W):
    V2 = [v2 for v2 in V if v2 not in W]
    E2 = {v2: l for v2, l in E.items() if v2 not in W}
    for v2 in V2:
        E2[v2] = [v2 for v2 in E2[v2] if v2 not in W]
    return V2, E2


# Prend un graphe et renvoie un dictionnaire qui associe à chaque sommet son degré
def degres(V, E):
    return {v: len(E[v]) for v in V}


# Prend un graphe et renvoie un sommet de degre maximal
def sommet_degre_maximal(V, E):
    v_maximal, degre_maximal = None, 0
    for v in V:
        if degre_maximal < len(E[v]):
            degre_maximal = len(E[v])
            v_maximal = v
    return v_maximal


# Prend n>0, une probabilité p, et génère un graphe à n sommets avec des sommets ayant une probabilité p d'exister
def generer_graphe(n, p):
    V = list(range(n))
    couples = []
    for u in V:
        for v in V[u+1:]:
            if random()<p:
                couples.append((u, v))
    E = couples_vers_liste_adjacences(V, couples)
    return V, E


V, E = lire_instance('exempleinstance.txt')
V2, E2 = supprimer_sommets(V, E, [0])
print(V, E)
print(V2, E2)
print(degres(V, E))
print(sommet_degre_maximal(V, E))
print(generer_graphe(5, 0.5))
