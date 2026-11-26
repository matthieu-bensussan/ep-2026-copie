from PIL import Image

def codage_rle(liste_octets):
    """Renvoie une liste d'octets obtenue par compression RLE."""
    liste_rle = []
    # On parcourt la liste d'octets passée en paramètre.
    i = 0
    while i < len(liste_octets):
        # On note la valeur de l'octet courant (couleur du pixel) au début du
        # run de pixels de couleur identique consécutifs.
        c = liste_octets[i]
        # On initialise à 1 la variable compteur comptant le nombre de pixels
        # de couleur identique consécutifs.
        k = 1
        # Tant que l'on a pas lu toute la liste et que le pixel suivant est de
        # la même couleur que celle du précédent (le run n'est pas encore fini)
        # et que le run n'a pas dépassé la longueur de 255. 
        #while i+k < len(liste_octets) and liste_octets[i+k] == c:
        while i+k < len(liste_octets) and liste_octets[i+k] == c and k < 255:
            # On incrémente la variable compteur indiquant la longueur du run.
            k += 1
        # On ajoute successivement dans la liste résultat encodée :
        # - longueur du run (nombre de pixel de couleur identiques : ne doit
        # pas dépasser 255 car codé sur un octet)
        # - la couleur répétée (nombre entre 0 et 255)
        liste_rle.append(k)
        liste_rle.append(c)
        i += k
    return liste_rle


def decodage_rle(liste_rle):
    """Renvoie la liste d'octets obtenue à partir de la liste liste_rle obtenue
    par compression RLE."""
    # On initialise le tableau résultat comme un tableau vide.
    res = []
    # On parcourt le tableau compressé passé en paramètre de deux en deux
    # pour noter chaque couple quantité, nombre.
    i = 0
    while i < len(liste_rle) - 1: # -1 pour éviter le dépassement d'indice
        quantite = liste_rle[i]
        nombre = liste_rle[i+1]
        # On complète le tableau résultat avec le run de cases identiques.
        res += quantite * [nombre]
        i += 2
    return res


def test_codage():
    assert codage_rle([255, 255, 0, 255, 255, 255]) == [2, 255, 1, 0, 3, 255]
    assert codage_rle(257 * [4]) == [255, 4, 2, 4]
    assert decodage_rle([2, 255, 1, 0, 3, 255]) == [255, 255, 0, 255, 255, 255]
    assert decodage_rle([3, 4, 1, 0, 2, 5]) == [4, 4, 4, 0, 5, 5]
    assert decodage_rle([5, 0]) == [0, 0, 0, 0, 0]


def enregistrer_octets(nom_fichier, liste_octets):
    """Enregistre une liste de valeurs numériques entre 0 et 255 dans le
    fichier nom_fichier. Si une valeur est plus grande que 255 on considère
    que c'est 255. De même pour les valeur plus petite que 0."""
    # Le fichier est ouvert en mode binaire pour pouvoir écrire sans
    # restriction toute valeur entre 0 et 255.
    with open(nom_fichier, 'wb') as fichier:
        # Pour convertir une liste de valeur entre 0 et 255 en une liste
        # d'octets qui peuvent être écrits dans le fichier, on utilise `bytes`.
        fichier.write(bytes([max(0, min(255, b)) for b in liste_octets]))


def charger_octets(nom_fichier):
    """Renvoie la liste des octets présents dans le fichier nom_fichier."""
    with open(nom_fichier, 'rb') as fichier:
        liste_octets = list(fichier.read())
        return liste_octets


def enregistrer_image(nom_image, largeur, liste_niveaux):
    """Enregistre un fichier image nom_image de la largeur donnée et dont les 
    valeurs de niveaux de gris des pixels sont celles de la liste
    liste_niveaux."""
    hauteur = len(liste_niveaux) // largeur
    im = Image.frombytes('L', (largeur, hauteur), bytes(liste_niveaux))
    im.save(nom_image)


def charger_image(nom_image):
    """Étant donné une image nom_image, renvoie un couple
    (largeur, liste_niveaux) où largeur est la largeur de l'image et
    liste_niveaux est la liste des valeurs de niveaux de gris de l'image ligne
    par ligne."""
    image = Image.open(nom_image).convert('L')
    return (image.width, list(image.tobytes()))

###############################################################################
# Fonction nécessaire pour les tests de la question 3                         #
###############################################################################

def encoder_decoder_image(nom_image):
    """Fonction de test permettant d'encoder puis décoder une image avec un
    codage RLE. Le fichier rle est nommé nom_image.rle et le fichier decodé
    est nom_image.dec.png ."""
    w, l = charger_image(nom_image)
    enregistrer_octets(nom_image+'.rle', codage_rle(l))
    l = charger_octets(nom_image+'.rle')
    enregistrer_image(nom_image+'.dec.png', w, decodage_rle(l))


if __name__ == "__main__":
    print("Essais pour la question 3.")
    encoder_decoder_image("bac_nsi_32.png")
    encoder_decoder_image("bac_nsi_256.png")