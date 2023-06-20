from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker


class Base(DeclarativeBase):
    engine = create_engine('sqlite:///db.sqlite3')
    session = sessionmaker(bind=engine)

    @declared_attr
    def __tablename__(cls):
        return ''.join(f'_{i.lower()}' if i.isupper() else i for i in cls.__name__).strip('_')