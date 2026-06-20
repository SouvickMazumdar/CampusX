from fastapi import FastAPI, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# OAuth2AuthorizationCodeBearer this is used for login from Google/Github login redirect

app=FastAPI()
oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl='/token')
# it automatically extracts the token from the headers thats why when /token endpoint is being triggered teh valid token is the token
# which get stored in the header. This is picked by the oauth2scheme and make it available for whole application

@app.post('/token')
def login(username: str=Form(...), password: str=Form(...)):# Form(...) means it is required
    if username=='Souvick' and password=='pas123':
        return {'access_token': 'valid_token', 'token_type':'bearer'}
    raise HTTPException(status_code=400, detail='Invalid Credentials')

def decode_token(token: str):
    if token=='valid_token':
        return {'name':'John'}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid authentication Credentials',

    )
    
def get_current_user(token: str=Depends(oauth2_scheme)):
    return decode_token(token)
    

@app.get('/profile')
def get_profile(user=Depends(get_current_user)):
    return {'username':user['name']}
