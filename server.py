import proto.edi_pb2 as edi_pb2
import proto.edi_pb2_grpc as edi_pb2_grpc
import grpc
from MelhorEnvioAPI import *
from model import *
from concurrent import futures
from dao import *
from protobuf_to_dict import protobuf_to_dict

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

        # Converter produtos para um dicionário JSON
        products_dict = [protobuf_to_dict(product) for product in products]

        # Chamar a API com os produtos em formato JSON
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
        date = request.order.date
        customer = request.order.customer
        shipping_address = request.order.shipping_address
        service_name = edi_pb2.SERVICES.Name(request.service)
        service = self.manipulateDB.selectService(service_name)

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
     
        api = MelhorEnvioAPI()
        response = api.create_cart(service_dict['id'], service_dict, receiver_dict, products_dict)
        package_code = response['protocol']
        return edi_pb2.CreateOrderResponse(tracking_code=package_code, sucess=True)

    def CancelOrder(self, request, context):
       
        return edi_pb2.CancelOrderResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    edi_pb2_grpc.add_EDIServiceServicer_to_server(EDIServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()