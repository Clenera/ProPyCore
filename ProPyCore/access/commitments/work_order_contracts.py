from .contracts import ContractsBase


class WorkOrderContracts(ContractsBase):
    """
    Procore Work Order Contracts

    /rest/v1.0/work_order_contracts
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url, "work_order_contracts", "work_order_contract")
