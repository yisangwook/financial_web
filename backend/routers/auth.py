from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
import auth # auth.py에서 유틸리티 함수 임포트
from auth import get_db # auth.py에서 get_db 임포트

router = APIRouter(
    prefix="/auth", # /auth 경로 접두사 사용
    tags=["auth"] # 문서화를 위한 태그
)

# --- Pydantic 모델 정의 ---
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel): # 사용자 정보 응답 모델 (비밀번호 제외)
    id: int
    username: str
    is_active: bool

    class Config:
        orm_mode = True # SQLAlchemy 모델과 매핑

# --- 사용자 등록 엔드포인트 ---
@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- 로그인 엔드포인트 (토큰 발급) ---
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES) # auth.py에서 설정된 시간 사용
    access_token = auth.create_access_token(
        data={"sub": user.username} # 토큰에 사용자 이름 저장
        # expires_delta=access_token_expires # 만료 시간 설정 (선택 사항, 기본값 사용 가능)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- 현재 사용자 정보 가져오기 (테스트용, 인증 필요) ---
@router.get("/me/", response_model=User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user