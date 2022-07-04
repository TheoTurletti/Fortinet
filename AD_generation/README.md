# Ce script est permet de générer des architectures Active Directory depuis un windows server :

Avant de lancer le script tapez les deux commandes suivantes dans un terminal pour installer les modules pythons nécessaires

1/ python3 -m pip install pyad
2/ python3 -m pip install pypiwin32

# A chaque lancement du script, les groupes sont supprimés et l'unité d'organisation est recréee

Si une erreur apparait pendant la réinitialisation, essayez de supprimer l'unité d'organisation de manière manuelle dans "Utilisateurs et Ordinateurs Active Directory".
Cela peut provenir de la protection contre la suppresion accidentelle

La ligne au début du main: 
# pyad.set_defaults(ldap_server="ELDEMO1.COM", username="Administrator", password="fortinet") 
ameliore grandement la rapidité de la génération
On passe de 1 génération par seconde sans cette ligne à 50.
# Elle est donc indispensable et doit être modifié en fonction des paramètres du serveur cible

# TOUS les utilisateurs et groupes sont générées dans une unité d'organisation spécifique


Les deux premiers choix sont des générations uniformes. Chaque groupes aura x uniques users ou inversement. La création sera symétrique

La génération du choix 1 formera de nombreux groupes avec chaque utilisateur associé à plusieurs groupes, ces utilisateurs étant les seuls membres de ces groupes.
Pour le choix 2, c'est l'inverse, à chaque groupe est associé plusieurs utilisateurs qui sont uniquement présent dans ce groupe.


Le troisième choix demande le nombre d'utilisateur, le nb de groupes et le nombres de groupes par user. 
Chaque user aura ici un nombre fixe de groupes mais l'attribution des groupes aux utilisateurs se fait  de manière aléatoire. Ainsi, un groupe peut avoir 0 membres alors qu'un autre plusieurs.



Les 4 èmes et 5 èmes choix sont des générations de groupes de type "nested".
Les groupes nested sont créees et agencés sous la forme d'arbre.

Le choix 4 demande le type d'arbre et le nombre de groupes. Choisir le type d'arbre 1 créera une chaine, 2 un arbre binaire, etc.. La profondeur dépendra de ces deux paramètres

Le choix 5 demande la profondeur et le type d'arbre. J'ai confondu volontairement les termes profondeur et hauteur de l'arbre.
Ici c'est le nombre de groupes qui variera en fonction des paramètres. Pour ce dernier choix, il faut faire attention à ne pas mettre une profondeur trop élevé car le nombre de groupe augmente de manière exponentielle.