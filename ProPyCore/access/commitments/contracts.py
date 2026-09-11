from ..base import Base


class ContractsBase(Base):
    """
    Shared implementation for Procore's purchase order and work order
    contract endpoints, which are identical apart from the endpoint path
    and payload key.
    """

    def __init__(self, access_token, server_url, resource_name, payload_key) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = f"/rest/v1.0/{resource_name}"
        self.payload_key = payload_key

    def list(
        self,
        project_id,
        company_id,
        view="extended",
        page=None,
        per_page=None,
        filters=None,
        return_request_obj=False,
    ):
        params = {
            "project_id": project_id,
            "view": view,
        }

        if page is not None:
            params["page"] = page

        if per_page is not None:
            params["per_page"] = per_page

        if filters:
            params.update(filters)

        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.get_request(
            self.endpoint, additional_headers=additional_headers, params=params, return_request_obj=return_request_obj
        )

    def get(
        self,
        contract_id,
        project_id=None,
        view="extended",
    ):
        params = {"view": view}

        if project_id is not None:
            params["project_id"] = project_id

        return self.get_request(
            f"{self.endpoint}/{contract_id}",
            params=params,
        )

    def create(
        self,
        project_id,
        contract,
    ):
        payload = {
            "project_id": project_id,
            self.payload_key: contract,
        }

        return self.post_request(
            self.endpoint,
            json=payload,
        )

    def update(
        self,
        contract_id,
        contract,
    ):
        payload = {
            self.payload_key: contract,
        }

        return self.patch_request(
            f"{self.endpoint}/{contract_id}",
            json=payload,
        )

    def delete(self, contract_id):
        return self.delete_request(f"{self.endpoint}/{contract_id}")

    def pdf(self, contract_id):
        """
        Export contract PDF.
        Returns 202 and a Location header.
        """
        return self.post_request(f"{self.endpoint}/{contract_id}/pdf")
