# Sorbonne Université 3I024 2018-2019
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : Tamene Hocine 3701946
# Etudiant.e 2 : Kacel Liza

import sys, getopt, string, math
from math import *


# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Fréquence moyenne des lettres en français
# À modifier
freq_FR = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# Chiffrement César
def chiffre_cesar(txt, key):
	message_chiffre=""
	for i in txt:
		message_chiffre += alphabet[(alphabet.index(i) + key) %26]
	return message_chiffre

# Déchiffrement César
def dechiffre_cesar(txt, key):
	message_dechiffre=""
	for i in txt:
		message_dechiffre += alphabet[(alphabet.index(i) - key) %26]
	return message_dechiffre

# Chiffrement Vigenere
def chiffre_vigenere(txt, key):
	messageChiffre = ""
	for i in range(len(txt)):
		messageChiffre+=alphabet[(alphabet.index(txt[i])+key[i%len(key)])%26]
	return messageChiffre

# Déchiffrement Vigenere
def dechiffre_vigenere(txt, key):
	messageDechiffre = ""
	for i in range(len(txt)):
		messageDechiffre+=alphabet[(alphabet.index(txt[i])-key[i % len(key)])%26]
	return messageDechiffre
  

# Analyse de fréquences
def freq(txt):
	hist = []
	for i in alphabet:	
		hist.append(txt.count(i))
	return hist

# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    return freq(txt).index(max(freq(txt)))

# indice de coïncidence
def indice_coincidence(hist):
    s=0
    if(sum(hist)>1) :
        for i in hist:
            s+=(i*(i-1))/((sum(hist)*(sum(hist)-1)))
    return s
# Recherche la longueur de la cl
""" une fonction qui estime la longueur de la clé a partir des indices de coincidencs """
def longueur_clef(cipher):
    longueur_cle = 3
    #rechercher la longueur tant que la longueur de la clé ne dépasse pas 20 lettres
    while(longueur_cle <= 20):
        i=0
        liste=[]
        while(i<longueur_cle):
            s1=""
            for k in cipher[i::longueur_cle]:
                s1+=k 
            liste.append(indice_coincidence(freq(s1)))
            i+=1
        if(sum(liste)/len(liste)>0.06):
            return longueur_cle    
        longueur_cle+=1
    return 0;

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    decalages=[]
    j=0
    while(j<key_length):
        s=""
        for i in cipher[j::key_length]:
            s+=i
        decalages.append((alphabet.index(alphabet[lettre_freq_max(s)])-alphabet.index('E'))%26)
        j+=1
    return decalages


# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    return dechiffre_vigenere(cipher,clef_par_decalages(cipher,longueur_clef(cipher)))


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def shift(liste,d):
    a = d % len(liste)
    return liste[-a:] + liste[:-a]


def indice_coincidence_mutuelle(h1,h2,d):
    text1=shift(h1,d)
    text2=shift(h2,d)
    s=0
    for i in range(len(alphabet)):
        s+=(text1[i]*text2[i])/(sum(text1)*sum(text2))
    return s
print(indice_coincidence_mutuelle(freq("ABABAB"),freq("CDCDCD"),2))

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Documentation à écrire
    """
    decalages=[0]*key_length
    return decalages

# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Documentation à écrire
    """
    return "TODO"


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1,L2):
    """
    Documentation à écrire
    """
    return 0.0

# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """
    Documentation à écrire
    """
    key=[0]*key_length
    score = 0.0
    return (score, key)

# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Documentation à écrire
    """
    return "TODO"


################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################


# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))
    
if __name__ == "__main__":
   main(sys.argv[1:])
