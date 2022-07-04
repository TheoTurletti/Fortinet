import requests
import os

kerberos_name = input("Please enter a name for the keytab : ")
princ = input("Please give the principal (EX : http/fortigate.eldemo1.com@eldemo1.com) : ")
fortigate = input("Give the fortigate domain name (EX : fortigate@eldemo1.com) : ")
domain = princ.partition("@")[2]
fgtadress = input("Give the fortigate ip adress ( EX: 10.222.19.250) : ")
access_token = input("Give the access token (check README to generate it) : ")

# La première commande génére une keytab
command1 = "ktpass -princ "+princ+" -mapuser "+fortigate+ " -pass * -crypto All -ptype KRB5_NT_PRINCIPAL -out fgt.keytab"

# Ces deux dernières commandes permettent de convertir la keytab en .txt
command2 = "certutil -encode fgt.keytab tmp.b64"
command3 = "findstr /v /c:- tmp.b64 > fgt1.txt "

#Lancement des 3 commandes 
os.system(command1+"&&"+command2+"&&"+ command3)

# Permet d'enlever les saut de lignes
with open("fgt1.txt", "r") as myfile:
  string1=myfile.read().replace('\n','')


#s = requests.Session()
#s.cert = 'C:/Users/DELL/Downloads/Fortinet_CA_SSL.cer'
# 'C:/Users/DELL/AppData/Local/Programs/Python/Python39/Lib/site-packages/certifi/cacert.pem'


# Je n'ai pas réussi à valider le certificat SSL téléchargé dans les 
# réglages du fgt, par conséquent, le post se fait de manière non sécurisée.

api_url = "https://"+fgtadress+"/api/v2/cmdb/user/krb-keytab/?access_token="+access_token

post = {
    "name": kerberos_name,
    "pac-data":"disable",
    "principal": princ,
    "ldap-server":[
        {
          "name":domain,
        }],
    "keytab": string1}

response = requests.post(api_url, json = post, verify = False)


if (response.status_code == 200):
  print("\n------------\n\nKeytab has been correctly configured\n\n------------")