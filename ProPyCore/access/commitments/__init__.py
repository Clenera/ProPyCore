from .purchase_order_contracts import PurchaseOrderContracts
from .work_order_contracts import WorkOrderContracts
from .change_orders import ChangeOrders


class Commitments:

    def __init__(self, access_token, server_url):
        self.purchase_order_contracts = PurchaseOrderContracts(access_token, server_url)
        self.work_order_contracts = WorkOrderContracts(access_token, server_url)
        self.change_orders = ChangeOrders(access_token, server_url)
