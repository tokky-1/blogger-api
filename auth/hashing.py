from passlib.context import CryptContext

hashcontext=CryptContext(schemes=["bcrypt"])

def createhash(password:str):  
    return hashcontext.hash(password)
    
def verifyhash(plainpassword:str, hashedpassword:str):
    return hashcontext.verify(plainpassword,hashedpassword)

