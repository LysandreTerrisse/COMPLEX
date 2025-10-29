from random import random
from time import time
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d


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


# Prends une fonction f(V, E), calcule f(V, E) cinq fois, et renvoie le temps médien
def temps_medien(f, V, E):
    t = []
    for _ in range(5):
        t0 = time()
        f(V, E)
        t1 = time()
        t.append(t1 - t0)
    return np.median(t)


def graphique(matrice, nom_axe_z, p_values = None, n_values = None):
    #Si aucune valeur pour p et n n'est spécifiée, on affiche matrice[n, p] selon n et p
    if p_values is None and n_values is None:
        X, Y = np.meshgrid(range(101), range(101))
        plt.figure().add_subplot(projection='3d').plot_surface(X.T, Y.T, matrice, edgecolor='royalblue', lw=0.5, rstride=8, cstride=8, alpha=0.3)
        plt.xlabel('n')
        plt.ylabel('p')
        plt.show()
    #Si aucune valeur pour n n'est spécifiée, on affiche matrice[n, p] selon n, avec p fixé
    elif n_values is None:
        for p in p_values:
            plt.plot(range(len(matrice)), matrice[:, p], label=f'p={p/(len(matrice[0])-1)}')
        plt.xlabel('n')
        plt.ylabel(nom_axe_z)
        plt.legend()
        plt.show()
    #Si aucune valeur pour p n'est spécifiée, on affiche matrice[n, p] selon p, avec n fixé
    elif p_values is None:
        for n in n_values:
            plt.plot(range(len(matrice[0])), matrice[n], label=f'n={n}')
        plt.xlabel('p')
        plt.ylabel(nom_axe_z)
        plt.legend()
        plt.show()
    else:
        exit("La fonction graphique ne peut pas prendre à la fois p_values et n_values")


# Question 3.3
def comparer_methodes():
    taille_algo_couplage = np.zeros((101, 101))
    taille_algo_glouton  = np.zeros((101, 101))
    t_algo_couplage      = np.zeros((101, 101))
    t_algo_glouton       = np.zeros((101, 101))
    for n in range(101):
        for p in range(101):
            V, E = generer_graphe(n, p/100)
            # On calcule le temps de algo_couplage et la taille du couplage renvoyé
            taille_algo_couplage[n, p] = len(algo_couplage(V, E))
            t_algo_couplage[n, p] = temps_medien(algo_couplage, V, E)
            # On calcule le temps de algo_glouton et la taille du couplage renvoyé
            taille_algo_glouton[n, p] = len(algo_glouton(V, E))
            t_algo_glouton[n, p] = temps_medien(algo_glouton, V, E)

    graphique(taille_algo_couplage, 'Longueur de la couverture', p_values = range(10, 100, 20))
    graphique(taille_algo_glouton , 'Longueur de la couverture', p_values = range(10, 100, 20))
    graphique(taille_algo_couplage, 'Longueur de la couverture', n_values = range(10, 100, 20))
    graphique(taille_algo_glouton , 'Longueur de la couverture', n_values = range(10, 100, 20))
    graphique(t_algo_couplage     , "Temps d'exécution"        , p_values = range(10, 100, 20))
    graphique(t_algo_glouton      , "Temps d'exécution"        , p_values = range(10, 100, 20))
    graphique(t_algo_couplage     , "Temps d'exécution"        , n_values = range(10, 100, 20))
    graphique(t_algo_glouton      , "Temps d'exécution"        , n_values = range(10, 100, 20))
    graphique(taille_algo_couplage, 'Longueur de la couverture')
    graphique(taille_algo_glouton , 'Longueur de la couverture')
    graphique(t_algo_couplage     , "Temps d'exécution")
    graphique(t_algo_glouton      , "Temps d'exécution")


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
        for p in range(5):
            V, E = generer_graphe(n, p/4)
            taille[n, p] = len(f(V, E))
            t[n, p] = temps_medien(f, V, E)

    graphique(t,      "Temps d'exécution"      , p_values=range(5))
    graphique(taille, "Taille de la couverture", p_values=range(5))
    
    taille = []
    t      = []
    for n in range(1, 20):
        V, E = generer_graphe(n, 1/np.sqrt(n))
        taille.append(len(f(V, E)))
        t.append(temps_medien(f, V, E))

    plt.plot(range(1, 20), t)
    plt.xlabel('n (et p=sqrt(n))')
    plt.ylabel("Temps d'exécution")
    plt.show()

    plt.plot(range(1, 20), taille)
    plt.xlabel('n (et p=sqrt(n))')
    plt.ylabel("Taille de la couverture")
    plt.show()


def borne_inf(V, E):
    n, m, delta = len(V), nb_aretes(V, E), degre_maximal(V, E)
    b1 = np.ceil(m / degre_maximal(V, E)) if delta > 0 else 0
    b2 = len(algo_couplage(V, E))
    b3 = (2*n - 1 - np.sqrt((2*n - 1)**2 - 8*m))/ 2
    return max(b1, b2, b3)


# Question 4.2.2
def branchement_avec_borne(V, E):
    #S'il n'y a pas d'arêtes, on renvoie la couverture vide
    if all(liste==[] for liste in E.values()):
        return []
    else:
        u, v = premiere_arete(V, E)
        # On considère le cas où l'on supprime u et on le met dans la couverture
        V1, E1 = supprimer_sommet(V, E, u)
        C1 = branchement(V1, E1) + [u]
        
        # Si la couverture obtenue a comme taille la borne inférieure, alors elle est optimale, donc on la renvoie:
        if len(C1) == borne_inf(V, E):
            return C1
        
        
        # On considère le cas où l'on supprime v et on le met dans la couverture
        V2, E2 = supprimer_sommet(V, E, v)
        C2 = branchement(V2, E2) + [v]
        # On renvoie la couverture minimale parmi les deux
        return C1 if len(C1)<len(C2) else C2


def nb_aretes(V, E):
    return sum(len(E[v]) for v in V)/2


def degre_maximal(V, E):
    return max(len(E[v]) for v in V)


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


# Question 4.4.1
def rapport_approximation():
    rapport_couplage = np.zeros((20, 5))
    rapport_glouton = np.zeros((20, 5))
    for n in range(20):
        for p in range(5):
            V, E = generer_graphe(n, p/4)
            taille_optimale = len(branchement(V, E))
            rapport_couplage[n, p] = len(algo_couplage(V, E))/taille_optimale if taille_optimale != 0 else 1
            rapport_glouton[n, p] = len(algo_glouton(V, E))/taille_optimale if taille_optimale != 0 else 1

    graphique(rapport_couplage, "Rapport d'approximation du couplage", p_values=range(5))
    graphique(rapport_glouton, "Rapport d'approximation du glouton", p_values=range(5))


V, E = lire_instance('exempleinstance.txt')
print(branchement(V, E))
print(branchement_avec_borne(V, E))
print(branchement_ameliore(V, E))
print(branchement_doublement_ameliore(V, E))
print(branchement_test_degre(V, E))


# graphiques pour la question 3.3
#comparer_methodes()
# graphiques pour la question 4.1.2
#evaluer(branchement)
# graphiques pour la question 4.2.2
#evaluer(branchement_avec_borne)
# graphiques pour la question 4.3.1
#evaluer(branchement_ameliore)
# graphiques pour la question 4.3.2
#evaluer(branchement_doublement_ameliore)
# graphiques pour la question 4.3.3
#evaluer(branchement_test_degre)
# graphiques pour la question 4.4.1
#rapport_approximation()
