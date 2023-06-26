import requests

class MelhorEnvioAPI:
    def __init__(self):
        self.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImY4ZjZhNTA5OTk5NmVjZTU4MDY3YzFhMDAzNGVkN2M0ODFhZTRlOWQzMjdkODE3MjAzODhjYjUzMjI3OTUzMTIzNDlkODkzZjUzMzQwMjgxIn0.eyJhdWQiOiI5NTYiLCJqdGkiOiJmOGY2YTUwOTk5OTZlY2U1ODA2N2MxYTAwMzRlZDdjNDgxYWU0ZTlkMzI3ZDgxNzIwMzg4Y2I1MzIyNzk1MzEyMzQ5ZDg5M2Y1MzM0MDI4MSIsImlhdCI6MTY4NzY2NTk4MSwibmJmIjoxNjg3NjY1OTgxLCJleHAiOjE3MTkyODgzODEsInN1YiI6IjE4NmUxMGQ3LTBmMDgtNDAyOC1iMjU4LThlMTFjODEwY2YwYiIsInNjb3BlcyI6WyJjYXJ0LXJlYWQiLCJjYXJ0LXdyaXRlIiwiY29tcGFuaWVzLXJlYWQiLCJjb21wYW5pZXMtd3JpdGUiLCJjb3Vwb25zLXJlYWQiLCJjb3Vwb25zLXdyaXRlIiwibm90aWZpY2F0aW9ucy1yZWFkIiwib3JkZXJzLXJlYWQiLCJwcm9kdWN0cy1yZWFkIiwicHJvZHVjdHMtZGVzdHJveSIsInByb2R1Y3RzLXdyaXRlIiwicHVyY2hhc2VzLXJlYWQiLCJzaGlwcGluZy1jYWxjdWxhdGUiLCJzaGlwcGluZy1jYW5jZWwiLCJzaGlwcGluZy1jaGVja291dCIsInNoaXBwaW5nLWNvbXBhbmllcyIsInNoaXBwaW5nLWdlbmVyYXRlIiwic2hpcHBpbmctcHJldmlldyIsInNoaXBwaW5nLXByaW50Iiwic2hpcHBpbmctc2hhcmUiLCJzaGlwcGluZy10cmFja2luZyIsImVjb21tZXJjZS1zaGlwcGluZyIsInRyYW5zYWN0aW9ucy1yZWFkIiwidXNlcnMtcmVhZCIsInVzZXJzLXdyaXRlIiwid2ViaG9va3MtcmVhZCIsIndlYmhvb2tzLXdyaXRlIl19.EB9rzvsXH1xM9dXk9BMF9UvdtQwuIUDpdVx97v7jU8uvQ8ErE1yVpWtWYI4ebkEyBs-LiE6WKMraQj701ebht-DhHUMU0QCxOY3pjWdQuMJFcRh70XvohwjK7VjmjESeLt47ZkQRA-h_loM9U9rwESjiuJZGBDHvFnlI_uxLLwSMZE02m7F77ErTzlQcYa1UWE1xOGFkAKKJXjvFOMcHGMYehWzIVgqtXe9zC4NefUnJ3hozUIF-riC2aETAVnTojtw4czVQnPuVqzqRVITL_QnnkQJwG4kXnL6ATT5yvrMhS8SROOCaHKN7bVD-holbYHlVXeNrdmd_8IJLiYwyIpgEl0IIgjoSiagGebPiK4e0FznqKm25cFX5_SCG0aoXsdh_Qnn2F8UjsJfhEmuBGDuVeiYToPefip6BiusXacr5liTGAyjQB_-csGmh-Ycoj1pAOX-aqeAZCDXIx2UOTLjXzfWmx2fS5pPbo7LdtPYkgDRWUPavJPtNnApy_r7dKvz3PuXZQw8g7E_A-P8NY79Hk8d4iQrgSazN88UpbpAJINxRRTBttr_WBx6SYWo3216QTsE2wU28HBoUeT3ddfk_KKZseB07BOeF156BWYJw5RBc-8QMhvLHdZE2LSv97YUO5mL5NRGqksZPykXHtN5CQHp9KbJ9PoLJogBnVX4'
        self.user_agent = "Teste"
        self.base_url = "https://sandbox.melhorenvio.com.br/api/v2/me"
        self.services = "1,2"
        self.height = 50
        self.width = 80
        self.length = 30
        self.weight = 20   
        self.transport_cep = "88032900"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"{self.user_agent}"
        }

    def create_cart(self, service_id, service, receiver, products):
        url = f"{self.base_url}/cart"

        payload = {
            "service": service_id,
            "from": service,
            "to": receiver,
            "products": products,
            "volumes": {
                "height": self.height,
                "width": self.width,
                "length": self.length,
                "weight": self.weight
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            data = response.json()
            return data
        
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None

    def calculate_shipping(self, to_postal_code, products):
        url = f"{self.base_url}/shipment/calculate"
                
        payload = {
            "from": {
                "postal_code": self.transport_cep
            },
            "to": {
                "postal_code": to_postal_code
            },
            "products": products,
            "services": self.services
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            data = response.json()
            result = []

            for item in data:
                result.append (
                    {
                        "name": item["name"],
                        "price": item["price"],
                        "delivery_time": item["delivery_time"]
                    }
                )
            return result
        
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None