# Génération automatique d'architecture Active Directory


""" TO DO :

pip install pyad
pip install pypiwin32

"""
# pyad is a python library designed to provide a simple, object oriented interface to Active Directory through ADSI on the Windows platform.
# Doc here : https://zakird.github.io/pyad/

from pyad import *
import subprocess
import random


# Pour simplifier la gestion des utilisateurs et des groupe, on crée 3 unités d'organisations 
# OU Test is the main one.
# OU Users inside Test for users
# OU Groups inside Test for the groups
# These groups are delete and created automatically at each start of the script
def main():
   
   global ouTest, ouUsers, ouGroups

    # A CHANGER
    pyad.set_defaults(ldap_server="ELDEMO1.COM", username="Administrator", password="fortinet")
    eldemo1_com = pyad.adcontainer.ADContainer(distinguished_name="dc=eldemo1, dc=com")

    # Construction des 3 uo
    try :
        ouTest = pyad.adcontainer.ADContainer.create_container(eldemo1_com,name = "generation")
        ouUsers = pyad.adcontainer.ADContainer.create_container(ouTest,name = "Users")
        ouGroups = pyad.adcontainer.ADContainer.create_container(ouTest,name = "Groups")
    
    except:
        print("L'UO test2 existe déjà , reinitialisation ..\n\n")

        ### REINITIALISATION DE L'UO 
        remove_uo = "Remove-ADOrganizationalUnit -Identity \'OU=generation,DC=eldemo1,DC=com\' -Recursive -Confirm:$False"
        # Si cette commande renvoie une erreur, essayez de changez le path du powershell.exe
        # Le module pyad ne prend pas en charge la suppresion d'uo; il est nécessaire de passer par powershell
        subprocess.call("C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe "+remove_uo, shell=True)

        # Construction des 3 uo
        ouTest = pyad.adcontainer.ADContainer.create_container(eldemo1_com,name = "generation")
        ouUsers = pyad.adcontainer.ADContainer.create_container(ouTest,name = "Users")
        ouGroups = pyad.adcontainer.ADContainer.create_container(ouTest,name = "Groups")


    print("-----------------------------------------\n")
    print("Choose a generation function by number: \n\n")
    print("             No Nested Groups \n")
    print("1/ Groups per user, number of users (group >> user) (Uniforme)")
    print("2/ Users per Group, number of groups (user >> group) (Uniforme)")
    print("3/ Number of user, number of groups, max group per user (Attribution aléatoire) \n")
    print("             With Nested Groups \n")
    print("4/ Tree nested group generation by nb_groups/type of tree")
    print("5/ Tree nested group generation by depth/type_tree\n")
    print("-----------------------------------------")
    choice = input()

    if(int(choice)  == 1) :
        function1()
    if(int(choice) == 2):
        function2()
    if(int(choice) == 3) :
        function3()
    if(int(choice) == 4):
        function4()
    if(int(choice) == 5) :
        function5()

# 1/ Groups per user, number of users (group >> user) 
def function1() :
    nb_users = input("Number of users to generate : ")
    nb_users = int(nb_users)

    nb_groups_per_user = input("Number of groups per user : ")
    nb_groups_per_user = int(nb_groups_per_user)

    nb_groups = nb_users * nb_groups_per_user

    # Les utilisateurs ssont nommés de la manière suivante : user1, user2 ...   
    for i in range(nb_users) :
        username = "user"+str(i+1)
        aduser.ADUser.create(username, ouUsers, password="fortinet", upn_suffix="@eldemo1.com", enable=True, optional_attributes={"samaccountname":username,"userPrincipalName":username + "@eldemo1.com","givenname":username,"displayName":username})
    
    # Les groupes sont nommés de la manière suivante : 1g1, 1g2, 1g3 , 2g1, 2g2 ,2g3 , 3g1 ..
    # Les groupes 1gx sont les groupes racines, 2gx les groupes de profondeur 2,   3gx .. 3   , ...
    for i in range(nb_groups) :
        group_name = "1g"+str(i+1)
        pyad.adcontainer.ADContainer.create_group(ouGroups, name = group_name)

    num_groups = 1
    for i in range(nb_users) :
        username = "user"+str(i+1)
        user_to_add = pyad.adobject.ADObject(distinguished_name="cn="+username+",ou=Users,ou=generation,dc=eldemo1, dc=com")
        for j in range(nb_groups_per_user):

            groupname = "1g"+str(num_groups)

            group = pyad.adgroup.ADGroup(distinguished_name="cn="+groupname+", ou=Groups,ou=generation,dc=eldemo1, dc=com")
            group.add_members(user_to_add)
            num_groups += 1

# 2/ Users per group, number of groups (user >> group) 
def function2() :
    nb_groups = input("Number of groups to generate : ")
    nb_groups = int(nb_groups)

    nb_users_per_group = input("Number of users per group : ")
    nb_users_per_group = int(nb_users_per_group)

    nb_users = nb_users_per_group * nb_groups

    # Les utilisateurs sont nommés de la manière suivante : user1, user2 ...   
    for i in range(nb_users) :
        username = "user"+str(i+1)
        # Création des utilisateurs
        aduser.ADUser.create(username, ouUsers, password="fortinet", upn_suffix="@eldemo1.com", enable=True, optional_attributes={"samaccountname":username,"userPrincipalName":username + "@eldemo1.com","givenname":username,"displayName":username})
    
    # Les groupes sont nommés de la manière suivante : 1g1, 1g2, 1g3 , 2g1, 2g2 ,2g3 , 3g1 ..
    # Les groupes 1gx sont les groupes racines, 2gx les groupes de profondeur 2,   3gx .. 3   , ...
    num_users = 1
    for i in range(nb_groups) :
        group_name = "1g"+str(i+1)
        # Création des groupes 
        pyad.adcontainer.ADContainer.create_group(ouGroups, name = group_name)
        for j in range(nb_users_per_group):

            username = "user"+str(num_users)
            user_to_add = pyad.adobject.ADObject(distinguished_name="cn="+username+",ou=Users,ou=generation,dc=eldemo1, dc=com")
            # Attribution des groupes
            group = pyad.adgroup.ADGroup(distinguished_name="cn="+group_name+", ou=Groups,ou=generation,dc=eldemo1, dc=com")
            group.add_members(user_to_add)
            num_users += 1
            
            
# 3/ Number of users, number of groups
def function3() :
    
    nb_groups = input("Number of groups to generate : ")
    nb_groups = int(nb_groups)

    nb_users = input("Number of users  : ")
    nb_users = int(nb_users)
    
    group_per_user = input("How many groups each user have ? : ")
    group_per_user = int(group_per_user)
    
    

    # Les groupes sont nommés de la manière suivante : 1g1, 1g2, 1g3 , 2g1, 2g2 ,2g3 , 3g1 ..
    # Les groupes 1gx sont les groupes racines, 2gx les groupes de profondeur 2,  3gx .. 3   , ...
    print("Création des groupes et des users ..")
    groups = []
    for i in range(nb_groups) :
        # Création des groupes 
        group_name = "1g"+str(i+1)
        g  = pyad.adcontainer.ADContainer.create_group(ouGroups, name = group_name)
        groups.append(g)

    # Les utilisateurs sont nommés de la manière suivante : user1, user2 ...   
    for i in range(nb_users) :
        # Création des users
        username = "user"+str(i+1)
        user_to_add = aduser.ADUser.create(username, ouUsers, password="fortinet", upn_suffix="@eldemo1.com", enable=True, optional_attributes={"samaccountname":username,"userPrincipalName":username + "@eldemo1.com","givenname":username,"displayName":username})
        for i in range(group_per_user) :
            # Attribution des groupes de manière aléatoire
            group_nb = random.randint(0, len(groups)-1)
            groups[group_nb].add_members(user_to_add)


#Nested Group by Type of tree
def function4():

    # Génération de groupes sous la forme d'arbre
    print("\nGroup Generation \n")	

    #Param groups
    nb_groups = input("Number of groups : ")
    nb_groups = int(nb_groups)
    # Ce paramètre correspond au type de l'arbre, ainsi en choisissant 2, chaque noeud parent aura au moins 2 enfants. Cela correspondrait à un arbre binaire
    type_tree = input("Type of tree : number of child groups per each parent group : ")
    type_tree = int(type_tree)
    
    
    """
    # Par défault, chaque parent a au moins 1 enfant afin d'éviter d'avoir des coupes dans l'arbre
    # Ce paramètre permet de donner la forme de l'arbre. En effet, un arbre de type 10 (max 10 enfants par parents) mais avec ce paramètre fixer à 2 aura la forme d'un arbre binaire avec exceptionnelement 
    # des parents qui ont 10 enfants
    avg_branch = input("avg groups per each parent group (Must be between 1 and type of tree): ")

    probability_node = int(avg_branch)/int(type_tree)
    """



    # Genération de l'arbre
    # Les groupes sont nommés de la manière suivante : 1g1, 1g2, 1g3 , 2g1, 2g2 ,2g3 , 3g1 ..
    # Les groupes 1gx sont les groupes racines, 2gx les groupes de profondeur 2,   3gx .. 3   , ... 
    depth = 0

    # Création du Noeud racine
    container_name = "group_depth"+str(depth)
    #Création de l'uo group_depth 0 contenant le noeud racine
    ou_depth = pyad.adcontainer.ADContainer.create_container(ouGroups,name = container_name)
    pyad.adcontainer.ADContainer.create_group(ou_depth,name = "0g1")
    
    g_number = 1 
    depth +=1
    container_name = "group_depth"+str(depth)
    ou_depth = pyad.adcontainer.ADContainer.create_container(ouGroups,name = container_name)
 
    for i in range(nb_groups-1) :
     
        # Création des groupes
        group_name = str(depth)+"g"+str(g_number)
        pyad.adcontainer.ADContainer.create_group(ou_depth, name = group_name)
  
  
        # Le nombre de groupe par niveau = type_d'arbre^(hauteur) pour un arbre complet
        # Ajout d'une profondeur
        if((g_number)%pow(type_tree,depth) == 0) :
            depth += 1
            container_name = "group_depth"+str(depth)
            #Création de l'uo group_depth-x ou seront insérés les groupes de groupes de profondeurs x
            ou_depth = pyad.adcontainer.ADContainer.create_container(ouGroups,name = container_name)
            g_number =0
        
        g_number +=1

    # Attributions des groupes enfants en utilisant l'architecture par conteneur générée plus haut
    for i in range(depth):
        name_container1 ='ou=group_depth'+str(i)+',ou=Groups,ou=generation,dc=eldemo1,dc=com'
        name_container2 = 'ou=group_depth'+str(i+1)+',ou=Groups,ou=generation,dc=eldemo1, dc=com'
        nb_child_iter = 0
        # Ici on récupère les groupes enfants des groupes de profondeux x et on les stocke sous la forme 
        # de tableau dans la variable "children"
        # Les unités d'organisation créées précèdement en fonction de leur profondeur permettent 
        # de faire l'attribution des groupes enfants aux groupes parents
        children = pyad.adcontainer.ADContainer(name_container2).get_children()
        length_children = len(children)
  
        # Pour chaque groupe parent, on lui attribue ses groupes enfants grâce au tableau regroupant les groupes enfants
        for group_parent in pyad.adcontainer.ADContainer(name_container1).get_children() :
            for i in range(type_tree) :
                
                # Dans le cas ou l'arbre n'est pas complet
                if(i+nb_child_iter >= length_children):
                    break
 
                group_parent.add_members(children[i+nb_child_iter])
            #nb_child_iter permet d'éviter d'ajouter deux groupes enfants identiques
            nb_child_iter += type_tree
            
    
 
    # AJOUT UTILISATEURS 
    nb_utilisateur = input("nombre d'utilisateur : ")
    nb_utilisateur = int(nb_utilisateur)
    # Les groupes "feuilles" sont les groupes enfants les plus bas dans l'arbre, la dernière couche de groupe
    percentage_user = input("Pourcentage d'utilisateur sur les groupes feuilles : ")
    percentage_user = int(percentage_user)
    
    # On crée un tableau pour les groupes feuilles et un tableau pour les groupes parents/nested
    # Cela nous permettra de gérer la répartition d'utilisateur sur les groupes feuilles
    leaf = []
    nested = []
    
    # On récupère tous les groupes grâce à cette fonction
    children = pyad.adcontainer.ADContainer("ou=Groups,ou=generation,dc=eldemo1, dc=com").get_children(True)
    for g in children :
        if(g.type ==  "group") :
            # Si le c'est un groupe feuille, on le met dans leaf
            if (len(g.get_members()) == 0):
                leaf.append(g)
            # Sinon on le met dans le tableau nested
            else :
                nested.append(g)
                
    
    if(percentage_user < 0) :
         percentage_user = 0
    elif(percentage_user>100):
        percentage_user = 100


    leaf_len = len(leaf) 
    nested_len = len(nested)
    
    print("Création et Rajout des utilisateurs ..")
    for i in range(nb_utilisateur) :
        rand = random.randint(1,100)
        # Répartition des utilisateurs en fonction du pourcentage choisi
        
        if(rand <= percentage_user) :
            # Rajout d'User dans feuille
            username = "user"+str(i+1)
            # On créee l'utilisateur
            user_to_add = aduser.ADUser.create(username, ouUsers, password="fortinet", upn_suffix="@eldemo1.com", enable=True, optional_attributes={"samaccountname":username,"userPrincipalName":username + "@eldemo1.com","givenname":username,"displayName":username})
            #user_to_add = pyad.adobject.ADObject(distinguished_name="cn="+username+",ou=Users,ou=test2,dc=eldemo1, dc=com")
            
            # On rajoute l'utilisateur dans un groupes aléatoire parmi ceux présent dans le tableau leaf
            random_group_nb = random.randint(0,leaf_len-1)
            leaf[random_group_nb].add_members(user_to_add)
        else :
            # Rajout d'User dans nested group
            username = "user"+str(i+1)
            # Création de l'utilisateur
            user_to_add =aduser.ADUser.create(username, ouUsers, password="fortinet", upn_suffix="@eldemo1.com", enable=True, optional_attributes={"samaccountname":username,"userPrincipalName":username + "@eldemo1.com","givenname":username,"displayName":username})
            
             # On rajoute l'utilisateur dans un groupes aléatoire parmi ceux présent dans le tableau nested
            random_group_nb = random.randint(0,nested_len-1)
            nested[random_group_nb].add_members(user_to_add)
    
        


def function5() :
    # Génération de groupes sous la forme d'arbre
    print("\nGroup Generation \n")	

    #Param groups
    depth = input("Depth (height of the tree) : ")
    depth = int(depth)

    type_tree = input("Type of tree : number of child groups per each parent group : ")
    type_tree = int(type_tree)
 
    # Ce calcul correspond au nombre de groupe par niveau 
    # C'est la suite de i allant de 0 à n : type_d'arbre^(i) pour un arbre complet avec n étant la profondeur
    nb_groups = 0
    for i in range(depth+1) :
        nb_groups += pow(type_tree,i)


    # Genération de l'arbre
    # Les groupes sont nommés de la manière suivante : 1g1, 1g2, 1g3 , 2g1, 2g2 ,2g3 , 3g1 ..
    # Les groupes 1gx sont les groupes racines, 2gx les groupes de profondeur 2,  3gx .. 3   , ...

    
    depth = 0
    #Noeud racine
    container_name = "group_depth"+str(depth)
    #Création de l'uo group_depth 0 contenant le noeud racine
    ou_depth = pyad.adcontainer.ADContainer.create_container(ouGroups,name = container_name)
    pyad.adcontainer.ADContainer.create_group(ou_depth,name = "0g1")

    print(str(nb_groups)+" groups are being created ..")
    g_number = 1 
    depth +=1
    container_name = "group_depth"+str(depth)
    ou_depth = pyad.adcontainer.ADContainer.create_container(ouGroups,name = container_name)
 
    for i in range(nb_groups-1) :
     
        # Création des groupes
        group_name = str(depth)+"g"+str(g_number)
        pyad.adcontainer.ADContainer.create_group(ou_depth, name = group_name)
  
        # Le nombre de groupe par niveau vaut type_d'arbre^(hauteur) pour un arbre complet
        # Ajout d'une profondeur
        if((g_number)%pow(type_tree,depth) == 0) :
            depth += 1
            container_name = "group_depth"+str(depth)
            ou_depth = pyad.adcontainer.ADContainer.create_container(ouGroups,name = container_name)
            g_number =0
        

        
        g_number +=1


    # Attributions des groupes enfants en utilisant l'architecture par conteneur générée plus haut
    for i in range(depth):
        name_container1 ='ou=group_depth'+str(i)+',ou=Groups,ou=generation,dc=eldemo1,dc=com'
        name_container2 = 'ou=group_depth'+str(i+1)+',ou=Groups,ou=generation,dc=eldemo1, dc=com'
        nb_child_iter = 0
        # Ici on récupère les groupes enfants des groupes de profondeux x et on les stocke sous la forme 
        # de tableau dans la variable "children"
        # Les unités d'organisation créées précèdement en fonction de leur profondeur permettent 
        # de faire l'attribution des groupes enfants aux groupes parents
        children = pyad.adcontainer.ADContainer(name_container2).get_children()
        length_children = len(children)
  
        # Pour chaque groupe parent, on lui attribue ses groupes enfants grâce au tableau regroupant les groupes enfants
        for group_parent in pyad.adcontainer.ADContainer(name_container1).get_children() :
            for i in range(type_tree) :
                
                # Dans le cas ou l'arbre n'est pas complet
                if(i+nb_child_iter >= length_children):
                    break
 
                group_parent.add_members(children[i+nb_child_iter])
            #nb_child_iter permet d'éviter d'ajouter deux groupes enfants identiques
            nb_child_iter += type_tree
            
    
 
    # AJOUT UTILISATEURS 
    nb_utilisateur = input("nombre d'utilisateur : ")
    nb_utilisateur = int(nb_utilisateur)
    # Les groupes "feuilles" sont les groupes enfants les plus bas dans l'arbre, la dernière couche de groupe
    percentage_user = input("Pourcentage d'utilisateur sur les groupes feuilles : ")
    percentage_user = int(percentage_user)
    
    # On crée un tableau pour les groupes feuilles et un tableau pour les groupes parents/nested
    # Cela nous permettra de gérer la répartition d'utilisateur sur les groupes feuilles
    leaf = []
    nested = []
    
    # On récupère tous les groupes grâce à cette fonction
    children = pyad.adcontainer.ADContainer("ou=Groups,ou=generation,dc=eldemo1, dc=com").get_children(True)
    for g in children :
        if(g.type ==  "group") :
            # Si le c'est un groupe feuille, on le met dans leaf
            if (len(g.get_members()) == 0):
                leaf.append(g)
            # Sinon on le met dans le tableau nested
            else :
                nested.append(g)
                
    
    if(percentage_user < 0) :
         percentage_user = 0
    elif(percentage_user>100):
        percentage_user = 100


    leaf_len = len(leaf) 
    nested_len = len(nested)
    
    print("Création et Rajout des utilisateurs ..")
    for i in range(nb_utilisateur) :
        rand = random.randint(1,100)
        # Répartition des utilisateurs en fonction du pourcentage choisi
        
        if(rand <= percentage_user) :
            # Rajout d'User dans feuille
            username = "user"+str(i+1)
            # On créee l'utilisateur
            user_to_add = aduser.ADUser.create(username, ouUsers, password="fortinet", upn_suffix="@eldemo1.com", enable=True, optional_attributes={"samaccountname":username,"userPrincipalName":username + "@eldemo1.com","givenname":username,"displayName":username})
            #user_to_add = pyad.adobject.ADObject(distinguished_name="cn="+username+",ou=Users,ou=test2,dc=eldemo1, dc=com")
            
            # On rajoute l'utilisateur dans un groupes aléatoire parmi ceux présent dans le tableau leaf
            random_group_nb = random.randint(0,leaf_len-1)
            leaf[random_group_nb].add_members(user_to_add)
        else :
            # Rajout d'User dans nested group
            username = "user"+str(i+1)
            # Création de l'utilisateur
            user_to_add =aduser.ADUser.create(username, ouUsers, password="fortinet", upn_suffix="@eldemo1.com", enable=True, optional_attributes={"samaccountname":username,"userPrincipalName":username + "@eldemo1.com","givenname":username,"displayName":username})
            
             # On rajoute l'utilisateur dans un groupes aléatoire parmi ceux présent dans le tableau nested
            random_group_nb = random.randint(0,nested_len-1)
            nested[random_group_nb].add_members(user_to_add)
    
if __name__ == "__main__":
    main()



print("DONE")