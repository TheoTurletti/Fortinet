From the windows server :

1/ Connect to Fortinet gui -> Status -> Administrator -> show active admin sessions -> note the source adress

2/ Admin-profiles -> create admin-profiles with the all access in Read/Write mode 

3/ Administrators -> create Admin Rest API -> Parameters :
admin profiles from step 2, 
trusted hosts : ip adress from step 1, 
desactivate PKI
CORS ALLOW Origin : https://fndn.fortinet.net

4/ Note API TOKEN that have been generated : Mine is mjbxgmnfhfgx4t494Gq7jt3NypQx17

5/ Launch keytab_kerberos_script.py