from db_conn import Base
from sqlalchemy import  Column, Integer, String, Sequence, BigInteger

class LogTable(Base):
    __tablename__  = 'logtable'
    __table_args__ = {'schema': 'peg'}

    logid = Column(BigInteger,primary_key=True,nullable=False)
    logtime = Column(String(length=50),nullable=True)
    log_user = Column(String(length=50),nullable=False)
    log_desc = Column(String(length=1000),nullable=False)
    api_uri = Column(String(length=1500),nullable=False)