from ..base import Base


class ContractsBase(Base):
    """
    Shared implementation for Procore purchase order and work order
    contract endpoints.
    """

    def __init__(
        self,
        access_token,
        server_url,
        resource_name,
        payload_key,
    ) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = f"/rest/v1.0/{resource_name}"
        self.payload_key = payload_key

    def _headers(self, company_id):
        return {"Procore-Company-Id": str(company_id)}

    def list(
        self,
        company_id,
        project_id,
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

        return self.get_request(
            self.endpoint,
            additional_headers=self._headers(company_id),
            params=params,
            return_request_obj=return_request_obj,
        )

    def get(
        self,
        company_id,
        contract_id,
        project_id=None,
        view="extended",
        return_request_obj=False,
    ):
        params = {"view": view}

        if project_id is not None:
            params["project_id"] = project_id

        return self.get_request(
            f"{self.endpoint}/{contract_id}",
            additional_headers=self._headers(company_id),
            params=params,
            return_request_obj=return_request_obj,
        )

    def create(
        self,
        company_id,
        project_id,
        contract,
        return_request_obj=False,
    ):
        payload = {
            "project_id": project_id,
            self.payload_key: contract,
        }

        return self.post_request(
            self.endpoint,
            additional_headers=self._headers(company_id),
            json=payload,
            return_request_obj=return_request_obj,
        )

    def update(
        self,
        company_id,
        contract_id,
        contract,
        project_id=None,
        return_request_obj=False,
    ):
        payload = {
            self.payload_key: contract,
        }

        if project_id is not None:
            payload["project_id"] = project_id

        return self.patch_request(
            f"{self.endpoint}/{contract_id}",
            additional_headers=self._headers(company_id),
            json=payload,
            return_request_obj=return_request_obj,
        )

    def delete(
        self,
        company_id,
        contract_id,
        project_id=None,
        return_request_obj=False,
    ):
        params = {}

        if project_id is not None:
            params["project_id"] = project_id

        return self.delete_request(
            f"{self.endpoint}/{contract_id}",
            additional_headers=self._headers(company_id),
            params=params,
            return_request_obj=return_request_obj,
        )

    def pdf(
        self,
        company_id,
        contract_id,
        project_id=None,
        return_request_obj=True,
    ):
        """
        Export a contract PDF.

        Returns the raw response by default so the caller can read the
        202 response and Location header.
        """
        params = {}

        if project_id is not None:
            params["project_id"] = project_id

        return self.post_request(
            f"{self.endpoint}/{contract_id}/pdf",
            additional_headers=self._headers(company_id),
            params=params,
            return_request_obj=return_request_obj,
        )
