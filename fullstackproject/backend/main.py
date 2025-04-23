from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from auth import create_access_token
from fastapi.responses import JSONResponse
from pydantic import  BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class UserRegister(BaseModel):
    username: str
    password: str


fake_users = {
    "admin": {"username": "admin", "password": "1234"}
}


token_blacklist = set()

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/logout")
def logout(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token bulunamadı")

    token = auth_header.split(" ")[1]
    print("Bir kullanıcı çıkış yaptı!")  # Bu satır terminalde görünür
    return JSONResponse(content={"message": "Çıkış başarılı."})
@app.post("/register")
def register(user: UserRegister):
    if user.username in fake_users:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten var")
    fake_users[user.username] = {
        "username": user.username,
        "password": user.password
    }
    print(f"Kullanıcı oluşturuldu: {user.username}")
    return {"message": "Kayıt başarılı!"}