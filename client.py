import grpc
import proto.edi_pb2 as edi_pb2
import proto.edi_pb2_grpc as edi_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp

def test_grpc_server():
    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')

    # Create a gRPC stub
    stub = edi_pb2_grpc.EDIServiceStub(channel)

    try:
        # Make a shipping request
        item1 = edi_pb2.Item(name="Item 1", unit_price=10.0, quantity=2)
        item2 = edi_pb2.Item(name="Item 2", unit_price=5.0, quantity=3)
        shipping_request = edi_pb2.ShippingRequest(
            items=[item1, item2],
            shipping_address=edi_pb2.Address(
                street="123 Main St",
                district="City Center",
                number=10,
                city="Some City",
                cep="12345-678",
                complement="Apt 3B"
            )
        )
        shipping_response = stub.CalculateShipping(shipping_request)
        for response in shipping_response:
            print("Name:", response.service)
            print("Shipping Cost:", response.shipping_cost)
            print("Expected Days:", response.expected_days)
            print()

        # Make an order creation request
        customer = edi_pb2.Customer(
            name="John Doe",
            cpf="12345678900",
            phonenumber="555-1234",
            email="johndoe@example.com"
        )
        order_timestamp = Timestamp()
        order_timestamp.GetCurrentTime()
        order = edi_pb2.Order(
                items=[item1, item2],
                total_price=35.0,
                date=order_timestamp,
                customer=customer,
                shipping_address=shipping_request.shipping_address
        )
        order_request = edi_pb2.CreateOrderRequest(
            order=order,
            service=edi_pb2.SERVICES.PAC
        )

        order_response = stub.CreateOrder(order_request)
        print("Tracking Code:", order_response.tracking_code)

        # cancel_request = edi_pb2.CancelOrderRequest(order_id="123456")
        # cancel_response = stub.CancelOrder(cancel_request)
        # print("Cancellation Success:", cancel_response.success)
        # print("Message:", cancel_response.message)

    except grpc.RpcError as e:
        print(f"Error: {e}")

    # Close the gRPC channel
    channel.close()

if __name__ == '__main__':
    test_grpc_server()