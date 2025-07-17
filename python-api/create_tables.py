from models import Base
from database import engine

Base.metadata.create_all(bind=engine)
print("테이블 생성 완료!") 