from time import time
from base64 import b64encode
import requests
from steam.core.crypto import rsa_publickey, pkcs1v15_encrypt

#If captcha is needed, add the gid from the login response to this
#https://steamcommunity.com/login/rendercaptcha/?gid=

def rsa_key(username):
    rsa = requests.post('https://steamcommunity.com/login/getrsakey/', data={'username':username,'donotcache':int(time() * 1000)}).json()

    key = rsa_publickey(int(rsa['publickey_mod'], 16),int(rsa['publickey_exp'], 16),)

    timestamp = rsa['timestamp']

    return key, timestamp


#If the login does require steam gaurd etc you have to re-send the request with the fields that its requiring. for ex; if it asks for emailauth_needed":true, you resend the request, while regenerating the RSA Key etc but you enter the steam email code on line 26

def login(username,password):
    key, timestamp = rsa_key(username) 
    data = {
            'username':username,
            'password': b64encode(pkcs1v15_encrypt(key, password.encode('ascii'))),
            "emailauth": '', #Email Code (Steam Gaurd)
            'emailsteamid':'', #When asked for a steam code you split the response and obtain this.
            "twofactorcode": '', #Mobile Auth (Steam Gaurd)
            "captchagid": '', # get this from line 7
            "captcha_text": '', # get this from line 7
            "loginfriendlyname": "DESKTOP-37173813",
            "rsatimestamp": timestamp,
            "remember_login": 'true',
            "donotcache": int(time() * 100000),
        }
    dologin = requests.post('https://steamcommunity.com/login/dologin/', data=data)
    print(dologin.text)


username = input('Username: ')
password = input('Password: ')
login(username,password)

