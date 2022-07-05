# Génération automatique d'architecture Active Directory


# Template pour générer des users et des groupes 
# Ne gère pas les groupes nested, ces derniers sont gérés dans le script python.


# Paramètres : Groupe, user_per_group, % enabled

# Ici il y a plus de user que de groupes, chaque user sera membre d'un seul groupe.


$UtilisateurMotDePasse = "fortinet" 



$nested = Read-Host "Nested-group ? y/n"

"""Cas sans Nested-Group"""
if($nested -eq "n"){


[int] $nbgroupe = Read-Host "Merci de Rentrer le Nombre de Groupes à Créer"

[int] $nb_usr_grp = Read-Host "Merci de Rentrer le Nombre d’Utilisateurs par groupe"

[int] $enabled_users = Read-Host "Merci de Rentrer le pourcentage d'utilisateur activé"

[int] $nbuser = $nbgroupe * $nb_usr_grp

Write-Output "Création de $nbgroupe groupes avec $nb_usr_grp utilisateurs par groupe => $nbuser utilisateurs "
#Création d'une UO pour la génération
NEW-ADOrganizationalUnit “test3” –path “DC=eldemo1,DC=com” -ProtectedFromAccidentalDeletion 0
NEW-ADOrganizationalUnit “User” –path “OU=test3,DC=eldemo1,DC=com” -ProtectedFromAccidentalDeletion 0
NEW-ADOrganizationalUnit “Group” –path “OU=test3,DC=eldemo1,DC=com” -ProtectedFromAccidentalDeletion 0


#Boucle de génération d'utilisateurs
for ($i=1; $i -le $nbuser; $i++)
{


$random = Get-Random -Maximum 100
$UtilisateurNom = "User$i"
if($random -le $enabled_users){


New-ADUser -Name "$UtilisateurNom" `
                    -DisplayName "$UtilisateurNom" `
                    -GivenName $UtilisateurNom `
                    -SamAccountName $UtilisateurNom `
                    -UserPrincipalName "$UtilisateurNom@eldemo1.com" `
                    -Path "OU=User,OU=test3,DC=eldemo1,DC=com" `
                    -AccountPassword(ConvertTo-SecureString $UtilisateurMotDePasse -AsPlainText -Force) `
                    -ChangePasswordAtLogon $false `
                    -Enabled $true

}else{
New-ADUser -Name "$UtilisateurNom" `
                    -DisplayName "$UtilisateurNom" `
                    -GivenName $UtilisateurNom `
                    -SamAccountName $UtilisateurNom `
                    -UserPrincipalName "$UtilisateurNom@eldemo1.com" `
                    -Path "OU=User,OU=test3,DC=eldemo1,DC=com" `
                    -AccountPassword(ConvertTo-SecureString $UtilisateurMotDePasse -AsPlainText -Force) `
                    -ChangePasswordAtLogon $false `
                    -Enabled $false
}
}
$num_user = 1
#Génération des groupes
for ($i=1; $i -le $nbgroupe; $i++)
{
    $GroupeNom = "A$i"
    New-ADGroup -Name "$GroupeNom" -SamAccountName $GroupeNom -GroupCategory Security -GroupScope Global -DisplayName "$GroupeNom" -Path "OU=Group,OU=test3,DC=eldemo1,DC=com"

    # Attribution des Groupes
    # Ici il y a plus de user que de groupes, chaque user sera membre d'un seul groupe.
    for ($j=1; $j -le $nb_usr_grp; $j++)
{
    $nom_user = "User$num_user"
    $num_user++

    Add-ADGroupMember -identity $GroupeNom -Members $nom_user  
  
}
}
}