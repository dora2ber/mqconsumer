
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



class SQLALchemy:

    def __init__(self):
        self._engine = None
        self._session  = None
        self.init_app()

    def init_app(self):
# PostgreSQL 연결 문자열
        DATABASE_URL = "postgresql://sm2postgres:Async2023!)@192.168.222.154:5432/sm2db"

# SQLAlchemy Engine 생성 및 Connection Pool 설정
        engine = create_engine(
            DATABASE_URL,
            pool_size=1000,  # 최대 연결 수
            max_overflow=10,  # 최대 추가 연결 수
            pool_timeout=30,  # 연결을 기다릴 최대 시간 (초)
            pool_recycle=3600,  # 연결을 재사용할 주기 (초)
            pool_pre_ping=True
        )

        self._engine = engine
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    def get_db(self):
        """
        요청마다 DB 세션 유지 함수
        :return:
        """
        if self._session is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine

Base = declarative_base()
db = SQLALchemy()


