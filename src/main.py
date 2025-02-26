from fastapi import Depends, FastAPI, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakAdmin, KeycloakOpenID
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    KEYCLOAK_ADMIN_USERNAME: str
    KEYCLOAK_ADMIN_PASSWORD: str

    class Config:
        env_file = None


settings = Settings()

# Keycloak Client Initialization (for authentication)
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    realm_name=settings.KEYCLOAK_REALM,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)

# Keycloak Admin Initialization (for user management)
keycloak_admin = KeycloakAdmin(
    server_url=settings.KEYCLOAK_SERVER_URL,
    username=settings.KEYCLOAK_ADMIN_USERNAME,
    password=settings.KEYCLOAK_ADMIN_PASSWORD,
    realm_name=settings.KEYCLOAK_REALM,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
    verify=True,  # Remove client_secret here
)

# OAuth2 Password Bearer Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# App Configuration
app = FastAPI(root_path="/web-auth")

# CORS Middleware for cross-origin requests
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserCreate(BaseModel):
    email: str
    username: str
    firstName: str
    lastName: str
    password: str


class User(BaseModel):
    username: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


@app.post("/register")
def register(user: UserCreate):
    """
    Register a new user with Keycloak.
    """
    try:
        # Create user via Keycloak Admin API
        user_data = {
            "email": user.email,
            "username": user.username,
            "enabled": True,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "credentials": [{"value": user.password, "type": "password"}],
            "realmRoles": ["user"],  # Assign a role if needed
        }
        keycloak_admin.create_user(user_data)
        return {"message": f"User '{user.username}' registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")


@app.post("/token")
def login(username: str = Form(...), password: str = Form(...)):
    """
    Authenticate a user and retrieve an access token.
    """
    try:
        token_response = keycloak_openid.token(
            username=username,
            password=password,
            grant_type="password",
        )
        return {
            "access_token": token_response["access_token"],
            "refresh_token": token_response["refresh_token"],
            "token_type": "bearer",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/verify-token")
def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verify the validity of an access token.
    """
    try:
        user_info = keycloak_openid.userinfo(token)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": "Token is valid", "user_info": user_info}
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Token verification failed: {str(e)}"
        )


@app.get("/user-info")
def user_info(token: str = Depends(oauth2_scheme)):
    """
    Retrieve user information based on the access token.
    """
    try:
        user_info = keycloak_openid.userinfo(token)
        return user_info
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Failed to fetch user info: {str(e)}"
        )


@app.post("/logout")
def logout(body: RefreshToken):
    """
    Logout a user by invalidating the access token.
    """
    try:
        keycloak_openid.logout(refresh_token=body.refresh_token)
        return {"message": "Logout successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Logout failed: {str(e)}")
    
@app.get("/healthz")
def health_check():
    """
    Health check endpoint.
    """
    try:
        return {"status": "healthy"}
    except Exception as e:
        # If the check fails, return an HTTPException
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
