from random import random
from time import time
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d

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
        V = [int(fd.readline()) for i in range(n)]
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


"""
Pour montrer que l'algorithme glouton n'est pas optimal,
il suffit de regarder ce contre-exemple :
    0--1--2--3--4
L'algorithme glouton commence par enlever un sommet de degré maximal
(par exemple le sommet 2) ainsi que ses arêtes. On obtien ainsi :
    0--1  3--4
Ensuite, l'algorithme se répète. On peut par exemple obtenir comme
solution la couverture {1, 2, 3}. Cependant, cette couverture n'est
pas optimale, puisqu'il existe la couverture {1, 3} qui est plus petite.
Dans ce cas, l'algorithme renvoie une solution 3/2 fois plus grande
que nécessaire. Ce n'est donc pas une 3/2-approximation.

De même, pour cet exemple :
    0--1--2--3--4--5--6
L'algorithme peut renvoyer {1, 2, 3, 4, 5} au lieu de {1, 3, 5}.
Ce n'est donc pas une 5/3-approximation.

Et pour celui-ci :
    0--1--2--3--4--5--6--7--8
L'algorithme peut renvoyer {1, 2, 3, 4, 5, 6, 7} au lieu de {1, 3, 5, 7}.
Ce n'est donc pas une 7/4 approximation.

Ainsi, pour tout n>=2, ce n'est pas une (1+2*n)/(n+1) approximation.
À la limite, on n'obtient que ce n'est pas une r-approximation pour r<2.
"""

def algo_couplage(V, E):
    C = []
    for u in V:
        for v in E[u]:
            if u not in C and v not in C:
                C += [u, v]
    return C

def algo_glouton(V, E):
    C = []
    W = sommet_degre_maximal(V,E)
    while(W != None):
        C += [W]
        V,E = supprimer_sommet(V,E,W)
        W = sommet_degre_maximal(V,E)
    return C

# Question 3.3

def comparer_methodes():
    taille_algo_couplage = np.zeros((100, 100))
    taille_algo_glouton  = np.zeros((100, 100))
    t_algo_couplage      = np.zeros((100, 100))
    t_algo_glouton       = np.zeros((100, 100))
    for n in range(100):
        for p in range(100):
            V, E = generer_graphe(n, p/100)
            # On calcule le temps de algo_couplage et la taille du couplage renvoyé
            t0 = time()
            taille_algo_couplage[n, p] = len(algo_couplage(V, E))
            t1 = time()
            t_algo_couplage[n, p] = t1 - t0
            # On calcule le temps de algo_glouton et la taille du couplage renvoyé
            t0 = time()
            taille_algo_glouton[n, p] = len(algo_glouton(V, E))
            t1 = time()
            t_algo_glouton[n, p] = t1 - t0

    #Pour algo_couplage
    #Afficher la longueur de la solution selon n, avec p fixé
    for p in range(0, 100, 20):
        plt.plot(range(100), taille_algo_couplage[:, p], label=f'p={p}')
    plt.xlabel('n')
    plt.ylabel('Longueur de la couverture')
    plt.legend()
    plt.show()
    #Afficher la longueur de la solution selon p, avec n fixé
    for n in range(10, 100, 20):
        plt.plot(range(100), taille_algo_couplage[n], label=f'n={n}')
    plt.xlabel('p')
    plt.ylabel('Longueur de la couverture')
    plt.legend()
    plt.show()
    #Afficher le temps d'exécution selon n, avec p fixé
    for p in range(0, 100, 20):
        plt.plot(range(100), t_algo_couplage[:, p], label=f'p={p}')
    plt.xlabel('n')
    plt.ylabel("Temps d'exécution")
    plt.legend()
    plt.show()
    #Afficher le temps d'exécution selon p, avec n fixé
    for n in range(10, 100, 20):
        plt.plot(range(100), t_algo_couplage[n], label=f'n={n}')
    plt.xlabel('p')
    plt.ylabel("Temps d'exécution")
    plt.legend()
    plt.show()

    for data in [taille_algo_couplage, taille_algo_glouton, t_algo_couplage, t_algo_glouton]:
        X, Y = np.meshgrid(range(100), range(100))
        plt.figure().add_subplot(projection='3d').plot_surface(X.T, Y.T, data, edgecolor='royalblue', lw=0.5, rstride=8, cstride=8, alpha=0.3)
        plt.xlabel('n')
        plt.ylabel('p')
        plt.show()


def premiere_arete(V, E):
    for u in V:
        for v in E[u]:
            return (u, v)


def branchement(V, E):
    #S'il n'y a pas d'arêtes, on renvoie la couverture vide
    if all(liste==[] for liste in E.values()):
        return []
    else:
        u, v = premiere_arete(V, E)
        # On considère le cas où l'on supprime u et on le met dans la couverture
        V1, E1 = supprimer_sommet(V, E, u)
        C1 = branchement(V1, E1) + [u]
        # On considère le cas où l'on supprime v et on le met dans la couverture
        V2, E2 = supprimer_sommet(V, E, v)
        C2 = branchement(V2, E2) + [v]
        # On renvoie la couverture minimale parmi les deux
        return C1 if len(C1)<len(C2) else C2


def evaluer(f):
    taille = np.zeros((20, 5))
    t      = np.zeros((20, 5))
    for n in range(20):
        for i, p in enumerate(np.linspace(0, 1, 5)):
            V, E = generer_graphe(n, p)
            t0 = time()
            taille[n, i] = len(f(V, E))
            t1 = time()
            t[n, i] = t1 - t0

    for j, p in enumerate(np.linspace(0, 1, 5)):
        plt.plot(range(20), t[:, j], label=f'p={p}')
    plt.xlabel('n')
    plt.ylabel("Temps d'exécution")
    plt.legend()
    plt.show()

    for j, p in enumerate(np.linspace(0, 1, 5)):
        plt.plot(range(20), taille[:, j], label=f'p={p}')
    plt.xlabel('n')
    plt.ylabel("Taille de la couverture")
    plt.legend()
    plt.show()


    taille = []
    t      = []
    for n in range(1, 20):
        V, E = generer_graphe(n, 1/np.sqrt(n))
        t0 = time()
        taille.append(len(f(V, E)))
        t1 = time()
        t.append(t1 - t0)

    plt.plot(range(1, 20), t)
    plt.xlabel('n (et p=sqrt(n))')
    plt.ylabel("Temps d'exécution")
    plt.show()

    plt.plot(range(1, 20), taille)
    plt.xlabel('n (et p=sqrt(n))')
    plt.ylabel("Taille de la couverture")
    plt.show()

def branchement_avec_proxy(V, E, proxy):
    if all(liste==[] for liste in E.values()):
        return []
    else:
        u, v = premiere_arete(V, E)
        # On considère le cas où l'on supprime u et on le met dans la couverture
        V1, E1 = supprimer_sommet(V, E, u)
        # On considère le cas où l'on supprime v et on le met dans la couverture
        V2, E2 = supprimer_sommet(V, E, v)
        # On répète récursivement là où la proxy/heuristique est la plus prometteuse
        return branchement_avec_proxy(V1, E1, proxy) + [u] if proxy(V1, E1)<proxy(V2, E2) else branchement_avec_proxy(V2, E2, proxy) + [v]
        
def proxy_couplage(V, E):
    return len(algo_couplage(V, E))

def nb_aretes(V, E):
    return sum(len(E[v]) for v in V)/2

def degre_maximal(V, E):
    return max(len(E[v]) for v in V)

def proxy_borne_inf(V, E):
    n, m, delta = len(V), nb_aretes(V, E), degre_maximal(V, E)
    b1 = np.ceil(m / degre_maximal(V, E)) if delta > 0 else 0
    b2 = proxy_couplage(V, E)
    b3 = (2*n - 1 - np.sqrt((2*n - 1)**2 - 8*m))/ 2
    return max(b1, b2, b3)

def proxy_glouton(V, E):
    return len(algo_glouton(V, E))

# Question 4.3.1
def branchement_ameliore(V, E):
    #S'il n'y a pas d'arêtes, on renvoie la couverture vide
    if all(liste==[] for liste in E.values()):
        return []
    else:
        u, v = premiere_arete(V, E)
        # On considère le cas où l'on supprime u et on le met dans la couverture
        V1, E1 = supprimer_sommet(V, E, u)
        C1 = branchement(V1, E1) + [u]
        # On considère le cas où l'on ne prend pas u (on le supprime car on ne veut pas le prendre) et où l'on prend tous les voisins de u (on les supprime car on les prend)
        V2, E2 = supprimer_sommets(V, E, [u] + E[u])
        C2 = branchement(V2, E2) + E[u]
        # On renvoie la couverture minimale parmi les deux
        return C1 if len(C1)<len(C2) else C2

#Question 4.3.2
def branchement_doublement_ameliore(V, E):
    #S'il n'y a pas d'arêtes, on renvoie la couverture vide
    if all(liste==[] for liste in E.values()):
        return []
    else:
        u = sommet_degre_maximal(V, E)
        v = E[u][0]
        # On considère le cas où l'on supprime u et on le met dans la couverture
        V1, E1 = supprimer_sommet(V, E, u)
        C1 = branchement(V1, E1) + [u]
        # On considère le cas où l'on ne prend pas u (on le supprime car on ne veut pas le prendre) et où l'on prend tous les voisins de u (on les supprime car on les prend)
        V2, E2 = supprimer_sommets(V, E, [u] + E[u])
        C2 = branchement(V2, E2) + E[u]
        # On renvoie la couverture minimale parmi les deux
        return C1 if len(C1)<len(C2) else C2

"""
Question 4.3.3

Soit G un graphe, et soit C* une couverture optimale contenant un sommet u de degré 1. Puisque u est degré 1, il est relié à exactement un autre sommet v. Considérons C' = (C* \setminus \{u\}) \cup \{v\}. Cet ensemble a la même taille que C*. De plus, la seule arête qui peut ne plus être couverte en enlevant u est de nouveau couverte par l'ajout de v. C'est donc une couverture, qui est optimale et qui ne contient pas u.
"""

# Question 4.3.3
def branchement_test_degre(V, E):
    #S'il n'y a pas d'arêtes, on renvoie la couverture vide
    if all(liste==[] for liste in E.values()):
        return []
    else:
        u, v = premiere_arete(V, E)
        
        # Si u est de degré 1, on ne branche que sur v
        if len(E[u])==1:
            V2, E2 = supprimer_sommet(V, E, v)
            return branchement(V2, E2) + [v]
        # Si v est de degré 1, on ne branche que sur u
        if len(E[v])==1:
            V1, E1 = supprimer_sommet(V, E, u)
            return branchement(V1, E1) + [u]
        
        # On considère le cas où l'on supprime u et on le met dans la couverture
        V1, E1 = supprimer_sommet(V, E, u)
        C1 = branchement(V1, E1) + [u]
        # On considère le cas où l'on supprime v et on le met dans la couverture
        V2, E2 = supprimer_sommet(V, E, v)
        C2 = branchement(V2, E2) + [v]
        # On renvoie la couverture minimale parmi les deux
        return C1 if len(C1)<len(C2) else C2

# Question 4.4.2
def proxy_m(V, E):
    # Lorsque choisir u donne un nombre d'arêtes m1, et que choisir v donne un nombre d'arêtes m2, avec m1 < m2, il est souvent préférable de brancher sur u, donc la proxy/heuristique serait de minimiser m. (c'est aussi équivalent à brancher sur le sommet de degré maximal parmi u et v).
    return nb_aretes(V, E)

def proxy_random(V, E):
    return random()

V, E = lire_instance('exempleinstance.txt')
V2, E2 = supprimer_sommets(V, E, [0])
print(V, E)
print(V2, E2)
print(degres(V, E))
print(sommet_degre_maximal(V, E))
print(generer_graphe(5, 0.5))
print(branchement(V, E))
print(branchement_test_degre(V, E))




"""
Soit G = (V, E) un graphe, M un couplage de G, et C une couverture de G.
1)

Puisque C est une couverture de G, alors elle couvre toutes les arêtes de G. Donc, en comptant la somme des degrés de C, on compte au moins une fois chaque arête de G. Donc la somme des degrés de C est au moins égale à m :
    m \leq \sum_{c \in C} d(c) \leq \sum_{c \in C} \Delta = \Delta \sum_{c \in C} 1 = \Delta * |C|

Donc |C| \geq \frac{m}{\Delta} et puisque |C| est entier, alors |C| \geq \lceil \frac{m}{\Delta} \rceil.

2) Puisque C est une couverture de G, elle couvre toutes les arêtes de G, y compris les arêtes de M. C contient donc, pour chaque arête de M, une extrémité de cette arête. Ces extrémités sont distinctes puisque M est un couplage. C admet donc au moins |M| éléments.

3) Puisque G contient une couverture de taille |C|, alors il y a |C|



Puisque C est une couverture, alors elle couvre toutes les arêtes de E. Donc E \subseteq C \times V. Ainsi, |E| <= |C| * |V|.

sqrt(|E|) = ((2n - 1) - sqrt((2n - 1)² - 8m)) / 2
|E| = ((2n - 1) - sqrt((2n - 1)² - 8m))² / 4
|E| = ((2n - 1)² - 2 * (2n - 1) * sqrt((2n - 1)² - 8m) + ((2n - 1)² - 8m)) / 4
|E| = (2 * (2n - 1)² - 2 * (2n - 1) * sqrt((2n - 1)² - 8m) - 8m) / 4

(2n - 1)² - (2n - 1)² - 8m = 8m


Puisque |E| <= |V|², alors |V| >= sqrt(|E|).


Brouillon : Puisque M est un couplage, alors chaque arête est indépendante, donc chaque extrémité est différente. En prenant au hazard une extrémité de chaque arête de M, on obtient un couplage.

Puisque C est une couverture, alors aucun sommet n'est relié entre eux. En choisissant pour chaque sommet de C au plus une arête incidente, on obtient un couplage.

Pour chaque arête de M, on a deux extrémités. Puisque M est un couplage, toutes ses arêtes sont indépendantes, et donc on a 2*|M| extrémités. Mais, puisque le nombre d'extrémités ne peut pas dépasser le nombre de sommets du graphe, alors 2*|M| <= |V| et donc |M| <= |V|/2.

On sait que la taille de E (donc m) est égale à la moitié de la somme des degrés du graphe :
    m = \frac{1}{2} \sum_{v \in V} d(v)
      \leq \frac{1}{2} \sum_{v \in V} \Delta
      \leq \frac{1}{2} \Delta \sum_{v \in V} 1
      \leq \frac{1}{2} \Delta * |V|

On obtient donc :
    2 * |V| \geq \frac{m}{\Delta}

On sait que |E| <= |V| * ∆

"""


#comparer_methodes()
#evaluer(branchement)
#evaluer(lambda V, E: branchement_avec_proxy(V, E, proxy_couplage))
#evaluer(lambda V, E: branchement_avec_proxy(V, E, proxy_borne_inf))
#evaluer(lambda V, E: branchement_avec_proxy(V, E, proxy_glouton))
#evaluer(branchement_ameliore)
#evaluer(branchement_doublement_ameliore)
