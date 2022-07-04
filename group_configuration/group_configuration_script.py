import requests

group_name_tab = [] 
choice = True
DN_tab = []

server_name = input("Please give the server name (EX : eldemo1.com) : ")
partition = server_name.partition(".")
#partition sans le point
new_partition = []
for mot in partition :
    if(mot != "."):
        new_partition.append(mot)

# Génération du distinguished name à partir du nom du server
base_dn = ""
for i in range(len(new_partition)):
    base_dn = base_dn +",DC="+new_partition[i]

while(choice):
    
    group_name = input("Please enter a name for the group : ")
    group_name_tab.append(group_name)

    

    DN = input("\nPlease give the distingushed name of the group you want to import without the server path\nExample : For the group : CN=A1,OU=groups,OU=test2"+base_dn+", only write CN=A1,OU=groups,OU=test2  : \n")
    DN = DN + base_dn

    response1 = True
    while(response1):
        satisfied = input("Is that ok ? "+ DN + " (y/n) : ")
        if(satisfied.lower() == "y"):
            response1 = False
        elif(satisfied.lower() == "n"):
            DN = DN = input("Please give the entire distingushed name of the group you want to import\nExample :  CN=A1,OU=groups,OU=test2,DC=eldemo1,DC=com  : ")
            response1 = False

    response2 = True
    while(response2):
        yn = input("Do you want to add another group ? y/n : ")
        if(yn.lower() == "y"):
            choice = True
            response2 = False
        elif(yn.lower() == "n"):
            choice = False
            response2 = False


    DN_tab.append(DN)
    print(str(len(DN_tab))+ " group selected : ")
    for dn in DN_tab :
        print(dn)



fgtadress = input("Give the fortigate ip adress ( EX: 10.222.19.250) : ")
access_token = input("Give the access token (check README to generate it) : ")



# Je n'ai pas réussi à valider le certificat SSL téléchargé dans les 
# réglages du fgt, par conséquent, le post se fait de manière non sécurisée.

api_url = "https://"+fgtadress+"/api/v2/cmdb/user/group/?access_token="+access_token
for i in range(len(DN_tab)):
    post =  {
      "name":group_name_tab[i],
      "group-type":"firewall",
      "authtimeout":0,
      "auth-concurrent-override":"disable",
      "auth-concurrent-value":0,
      "http-digest-realm":"",
      "sso-attribute-value":"",
      "member":[
        {
          "name":server_name,
        }
      ],
      "match":[
        {
          "server-name":server_name,
          "group-name":DN_tab[i]
        }
      ],
      "user-id":"email",
      "password":"auto-generate",
      "user-name":"disable",
      "sponsor":"optional",
      "company":"optional",
      "email":"enable",
      "mobile-phone":"disable",
      "sms-server":"fortiguard",
      "sms-custom-server":"",
      "expire-type":"immediately",
      "expire":14400,
      "max-accounts":0,
      "multiple-guest-add":"disable",
      "guest":[
      ]
    }
    #print(post)
    response = requests.post(api_url, json = post, verify = False)
    if (response.status_code == 200):
        print("\n------------------------\n\nGroup "+group_name_tab[i]+ " has been correctly configured on the fortigate\n\n------------------------")