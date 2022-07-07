from django.contrib.auth import get_user_model
from mock import patch
from rest_framework.test import APITestCase

from ecommerce.layer_service.rate_exchange import RateExchange
from ecommerce.tests.utils import MockRequest

User = get_user_model()

class RateExchangeTests(APITestCase):

    data = [{"casa":{"compra":"126,85","venta":"132,85","agencia":"349","nombre":"Dolar Oficial","variacion":"0","ventaCero":"TRUE","decimales":"2"}},{"casa":{"compra":"100,00","venta":"250,00","agencia":"310","nombre":"Dolar Blue","variacion":"-1,57","ventaCero":"TRUE","decimales":"2"}},{"casa":{"compra":"No Cotiza","venta":"0","agencia":"311","nombre":"Dolar Soja","variacion":"0","ventaCero":"TRUE","decimales":"3"}},{"casa":{"compra":"279,42","venta":"280,24","agencia":"312","nombre":"Dolar Contado con Liqui","variacion":"0,07","ventaCero":"TRUE","decimales":"2"}},{"casa":{"compra":"268,810","venta":"268,030","agencia":"313","nombre":"Dolar Bolsa","variacion":"0,380","ventaCero":"TRUE","decimales":"3"}},{"casa":{"compra":"9.852,070","venta":"0","agencia":"399","nombre":"Bitcoin","variacion":"-100,00","ventaCero":"TRUE","decimales":"3"}},{"casa":{"nombre":"Dolar turista","compra":"No Cotiza","venta":"219,20","agencia":"406","variacion":"0","ventaCero":"TRUE","decimales":"2"}},{"casa":{"compra":"122,79","venta":"130,61","agencia":"302","nombre":"Dolar","decimales":"3"}},{"casa":{"nombre":"Argentina","compra":"2.489,00","venta":"1,55","mejor_compra":"True","mejor_venta":"False","fecha":"05\/05\/15","recorrido":"16:30","afluencia":{},"agencia":"141","observaciones":{}}}]

    def setUp(self):
        pass

    
    @patch(
        "ecommerce.layer_service.rate_exchange.requests.get",
        return_value=MockRequest(status_code=200, content=data)
    )
    def test_fetch_rate_usd_blue_happy_path(self, _):
        exchange = RateExchange()
        rate = exchange.fetch_rate_usd_blue()
        self.assertEqual(rate*100, 1)
        
    