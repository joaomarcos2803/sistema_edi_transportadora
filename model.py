# coding: utf-8
from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ClientAddres(Base):
    __tablename__ = 'client_address'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    street = Column(String(60), nullable=False)
    city = Column(String(40), nullable=False)
    cep = Column(String(20), nullable=False)
    district = Column(String(50), nullable=False)
    number = Column(Integer, nullable=False)
    complement = Column(String(60))


class Service(Base):
    __tablename__ = 'services'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    street = Column(String(80), nullable=False)
    complement = Column(String(100), nullable=False)
    number = Column(Integer, nullable=False)
    district = Column(String(50), nullable=False)
    city = Column(String(80), nullable=False)
    postal_code = Column(String(20), nullable=False)


class TransportOrder(Base):
    __tablename__ = 'transport_order'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".transport_order_id_seq'::regclass)"))
    package_code = Column(String(50), nullable=False, unique=True)
    created_at = Column(Date, server_default=text("now()"))
    delivery_time = Column(Integer, nullable=False)
    status = Column(Enum('Awaiting Collection', 'Send', 'In Transport', 'Delivered', 'Canceled', name='status_type'), nullable=False)
    client_address_id = Column(ForeignKey('public.client_address.id', ondelete='CASCADE'), nullable=False)
    service_id = Column(ForeignKey('public.services.id'), nullable=False)

    client_address = relationship('ClientAddres')
    service = relationship('Service')
