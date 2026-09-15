from ..base import Base


class Resources(Base):
    """
    Procore Webhook Resources

    Company:
    /rest/v2.0/companies/{company_id}/webhooks/resources

    Project:
    /rest/v2.0/companies/{company_id}/projects/{project_id}/webhooks/resources
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def _endpoint(self, company_id, project_id=None):
        if project_id is not None:
            return f"/rest/v2.0/companies/{company_id}" f"/projects/{project_id}" f"/webhooks/resources"

        return f"/rest/v2.0/companies/{company_id}/webhooks/resources"

    def list(
        self,
        company_id,
        payload_version,
        payload_format,
        project_id=None,
        namespace=None,
        page=None,
        per_page=None,
        return_request_obj=False,
    ):
        params = {
            "payload_format": payload_format,
            "payload_version": payload_version,
        }

        if namespace is not None:
            params["namespace"] = namespace

        if page is not None:
            params["page"] = page

        if per_page is not None:
            params["per_page"] = per_page

        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.get_request(
            self._endpoint(company_id, project_id),
            additional_headers=additional_headers,
            params=params,
            return_request_obj=return_request_obj,
        )
