from sqlalchemy.orm import Session
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from model import *

class DAO():
    def getSession():
        engine = create_engine("postgresql+psycopg2://postgres:teste@localhost:5432/EDI")
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    
    def insert(session, obj):
        session.add(obj)

class DAOClientAddress():
    def select(session, name):
        client = session.query(ClientAddres).filter(ClientAddres.name == name).first()
        return client

class DAOTransportOrder():
    def select(session, package_code):
        transport_order = session.query(TransportOrder).filter(TransportOrder.package_code == package_code).first()
        return transport_order
    
class DAOServices():
    def select(session, name):
        service = session.query(Service).filter(Service.name == name).first()
        return service
    
