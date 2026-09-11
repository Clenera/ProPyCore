from .contracts import ContractsBase


class PurchaseOrderContracts(ContractsBase):
    """
    Procore Purchase Order Contracts

    /rest/v1.0/purchase_order_contracts
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url, "purchase_order_contracts", "purchase_order_contract")
