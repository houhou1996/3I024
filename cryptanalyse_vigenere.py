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
freq_FR = [0.09213414037491088,  0.010354463742221126,  0.030178915678726964,  0.03753683726285317,  0.17174710607479665,  0.010939030914707838,  0.01061497737343803,  0.010717912027723734,  0.07507240372750529,  0.003832727374391129,  6.989390105819367e-05,  0.061368115927295096,  0.026498684088462805,  0.07030818127173859,  0.049140495636714375,  0.023697844853330825,  0.010160031617459242,  0.06609294363882899,  0.07816806814528274,  0.07374314880919855,  0.06356151362232132,  0.01645048271269667,  1.14371838095226e-05,  0.004071637436190045,  0.0023001447439151006,  0.0012263202640210343]

# Chiffrement César
def chiffre_cesar(txt, key):
    message_chiffre=""
    for i in txt:
        message_chiffre += alphabet[(alphabet.index(i) + key) %26]
    txt=message_chiffre
    return txt

# Déchiffrement César
def dechiffre_cesar(txt, key):
    message_dechiffre=""
    for i in txt:
        message_dechiffre += alphabet[(alphabet.index(i) - key) %26]
    txt=message_dechiffre
    return txt
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
    return 0

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
    text2=h2
    s=0
    for i in range(len(alphabet)):
        s+=(text1[i]*text2[i])/(sum(text1)*sum(text2))
    return s

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
	decalages = [0]
	d = 1
	d0 = cipher[0::key_length]
	j= 1
	while(j<key_length):
		ICM =[]
		for d in range(len(alphabet)):
			ICM.append(indice_coincidence_mutuelle(freq(d0),freq(cipher[j::key_length]),d))
		decalages.append(ICM.index(max(ICM)))
		j+=1
		d+=1
	return decalages
# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    key_length = longueur_clef(cipher)
    if(key_length != 0):
        # On récupére le tableau de décalages 
        decalages = tableau_decalages_ICM(cipher, key_length)
        j=0
        text_chifrre_en_cesar = ""
        # On parcourt le texte et on décale chaque lettre grâce au tableau décalages
        for i in cipher:
            text_chifrre_en_cesar+=dechiffre_cesar(i, decalages[j%len(decalages)])
            j+=1
        text_dechifrre_en_cesar = ""
        # On récupére la fréquence maximum du texte
        freq_max=lettre_freq_max(text_chifrre_en_cesar)
        # On récupére le décalage
        decalage=(freq_FR.index(max(freq_FR))-freq_max)%len(alphabet)
        for i in text_chifrre_en_cesar:
            text_dechifrre_en_cesar+=chiffre_cesar(i, decalage)
        return text_dechifrre_en_cesar
    else:
        return cipher

### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def moyenne(liste):
	return sum(liste)/len(liste)
def esperance(x):
	s=0
	for i in range(len(x)):
		s+=x[i];
	return s/len(x)
def correlation(L1,L2):
	s1=0
	s2=0
	s3=0
	for i in range(len(L1)):
		s1+= (L1[i]-esperance(L1)) * (L2[i]-esperance(L2))
		s2+= (L1[i]-esperance(L1)) ** 2
		s3+= (L2[i]-esperance(L2)) ** 2
	return s1/(math.sqrt(s2*s3))
# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    decalages = []
    maximal = []
    i=0
    while(i<key_length):
    	liste = []
    	for j in range(26):
    		liste.append(correlation(freq_FR,freq(dechiffre_cesar(cipher[i::key_length],j))))
    	maximal.append(max(liste))
    	decalages.append((liste.index(maximal[i])))
    	i+=1
    return (moyenne(maximal),decalages)
# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    i=1
    liste1=[]
    liste2=[]
    while i<=20:
        (score,key) = clef_correlations(cipher,i)
        liste1.append(score)
        liste2.append(key)
        i+=1
    maxi = max(liste1)
    key = liste2[liste1.index(maxi)]
    return dechiffre_vigenere(cipher,key)


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
