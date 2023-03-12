from fastapi import Depends,APIRouter,Request,Response,status
from fastapi.templating import Jinja2Templates
from model.userModel import User
from security import authSecurity


# instance
adminRouter=APIRouter()
templates=Jinja2Templates(directory="templates/")


@adminRouter.get("/dashbord")
def get_signup(request:Request,current_admin:User=Depends(authSecurity.get_current_admin)):
    return templates.TemplateResponse("admin/dashbord.html",{"request":request,"admin":current_admin})
