import proto.edi_pb2 as edi_pb2
import proto.edi_pb2_grpc as edi_pb2_grpc
import grpc
from MelhorEnvioAPI import *
from model import *
from concurrent import futures
from dao import *
from protobuf_to_dict import protobuf_to_dict
import datetime

class AcessDB:
    def insert(obj):
        try:
            session = DAO.getSession()
            DAO.insert(session, obj)
            session.commit()
            session.close()
            return 1
        except:
            return 0
        
    def update(obj):
        try:
            session = DAO.getSession()
            DAO.update(session, obj)
            session.commit()
            session.close()
            return 1
        except:
            return 0
        
    def selectClientAddress(name):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            client_address = DAOClientAddress.select(session, name)
            session.commit()
            session.close()
            return client_address
        except:
            return 0
    
    def selectTransportOrder(code):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            transport_order = DAOTransportOrder.select(session, code)
            session.commit()
            session.close()
            return transport_order
        except:
            return 0
        
    def selectService(name):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            service = DAOServices.select(session, name)
            session.commit()
            session.close()
            return service
        except:
            return 0

        
class EDIServicer(edi_pb2_grpc.EDIServiceServicer):
    def __init__(self):
        self.manipulateDB = AcessDB

    def CalculateShipping(self, request: edi_pb2.ShippingRequest, context):
        to_postal_code = request.shipping_address.cep
        products = request.items

        products_dict = [protobuf_to_dict(product) for product in products]

        api = MelhorEnvioAPI()
        items = api.calculate_shipping(to_postal_code, products_dict)
        response = edi_pb2.ShippingResponse()

        for item in items:
            response.service = item["name"]
            response.shipping_cost = float(item["price"])
            response.expected_days = int(item["delivery_time"])
            yield response

    def CreateOrder(self, request, context):
        products = request.order.items
        customer = request.order.customer
        shipping_address = request.order.shipping_address
        service_name = edi_pb2.SERVICES.Name(request.service)
        service = self.manipulateDB.selectService(service_name)
        delivery_time = request.delivery_time
        sucess = True

        service_dict = {
            "id": service.id,
            "name": service.name,
            "phone": service.phone,
            "address": service.street,
            "complement": service.complement,
            "number": service.number,
            "district": service.district,
            "city": service.city,
            "postal_code": service.postal_code
        } 

        receiver_dict = {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phonenumber,
            "email": customer.email,
            "address": shipping_address.street,
            "complement": shipping_address.complement,
            "number": shipping_address.number,
            "district":shipping_address.district,
            "city": shipping_address.city,
            "postal_code": shipping_address.cep
        }

        products_dict = [protobuf_to_dict(product) for product in products]

        #inserindo o cliente no banco 
        receiver_db = dict(receiver_dict)  
        receiver_db["street"] = receiver_db.pop("address") 
        receiver_db["cep"] = receiver_db.pop("postal_code") 

        clientAddress = ClientAddres()

        for key, value in receiver_db.items():
            if hasattr(clientAddress, key):
                setattr(clientAddress, key, value)

        if self.manipulateDB.selectClientAddress(clientAddress.id):
            if not self.manipulateDB.update(clientAddress):
                sucess = False
        else:
            if not self.manipulateDB.insert(clientAddress):
                sucess = False
           
        #consultando a api para gerar o código de rastreamento dos produtos
        api = MelhorEnvioAPI()
        response = api.create_cart(service_dict['id'], service_dict, receiver_dict, products_dict)
        package_code = response['protocol']

        #inserindo o transport_order no banco
        client = self.manipulateDB.selectClientAddress(customer.id)

        transport_order = TransportOrder(package_code=package_code, delivery_time=delivery_time, status='Awaiting Collection')
        transport_order.client_address = client
        transport_order.service = service

        if not self.manipulateDB.insert(transport_order):
            sucess = False
        
        if sucess:
            print('Cliente inserido ou atualizado e TransportOrder inserindo no banco!')

        return edi_pb2.CreateOrderResponse(tracking_code=package_code, sucess=sucess)
    
    def CancelOrder(self, request, context):
        tracking_code = request.tracking_code
        success = False
        message = ''
        order_transport = self.manipulateDB.selectTransportOrder(tracking_code)

        if not order_transport:
            success = False
            message = 'Ordem de transporte não encontrada'

        created_at_datetime = order_transport.created_at
        max_date = created_at_datetime + datetime.timedelta(days=1)

        if datetime.date.today() > max_date:
            success = False
            message = 'A data máxima para cancelamento foi excedida'
        else:
            success = True
            message = 'Ordem de transporte cancelada com sucesso'
            order_transport.status = 'Canceled'

            if not self.manipulateDB.update(order_transport):
                success = False
                message = 'Erro ao atualizar o status da ordem de transporte'

        return edi_pb2.CancelOrderResponse(success = success, message = message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    edi_pb2_grpc.add_EDIServiceServicer_to_server(EDIServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()