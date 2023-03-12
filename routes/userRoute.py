from fastapi import Depends,APIRouter,Request,Response,status
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database.connection import get_db
from fastapi.security import OAuth2PasswordRequestForm
from controller import userController
from model.userModel import User
from schema.userSchema import Token
from security import authSecurity
from datetime import timedelta
from starlette.responses import RedirectResponse


# instance
userRouter=APIRouter()
templates=Jinja2Templates(directory="templates/")

@userRouter.get("/index")
def get_index(request:Request):
    return templates.TemplateResponse("front/home/index.html",{"request":request})

@userRouter.get("/")
def get_index(request:Request):
    return templates.TemplateResponse("front/home/index.html",{"request":request})

@userRouter.get("/signup")
def get_signup(request:Request):
    return templates.TemplateResponse("auth/signup.html",{"request":request})

@userRouter.get("/signin")
def get_signup(request:Request):
    return templates.TemplateResponse("auth/signin.html",{"request":request})

@userRouter.get("/event")
def get_signup(request:Request,current_user:User=Depends(authSecurity.get_current_user)):
    return templates.TemplateResponse("front/event.html",{"request":request,"user":current_user})



@userRouter.post("/signup")
def create_new_user(request:Request,db:Session=Depends(get_db),form_data:OAuth2PasswordRequestForm=Depends()):
    db_user=userController.get_user_by_username(db=db,username=form_data.email)
    if db_user:
        error="E-mail already exist"
        return templates.TemplateResponse("auth/signup.html",{"request":request,"error":error},status_code=301)
    else:
        new_user=User(email=form_data.email,username=form_data.email,password=authSecurity.get_password_hash(form_data.password))
        user=userController.create_user(db=db,signup=new_user)
        return templates.TemplateResponse("auth/signin.html",{"request":request,"user":user},status_code=200)



@userRouter.post("/signin", response_model=Token)
def login_for_access_token(response:Response,request:Request,form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): 
    user = userController.authenticate_user(
        db=db,
        username=form_data.email,
        password=form_data.password
    )
    if not user:
        error ="incorrect account Information "
        return templates.TemplateResponse('auth/signin.html',{"error":error, "request":request}, status_code=301)

    access_token_expires = timedelta(minutes=authSecurity.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authSecurity.create_access_token(
        data={"sub": user.username,"role":user.is_Admin}, expires_delta=access_token_expires
    )
    response = RedirectResponse(url="/index",status_code=status.HTTP_302_FOUND)

    # to save token in cookie
    response.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True) 
    return response
