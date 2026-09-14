from ..base import Base


class Hooks(Base):
    """
    Procore Webhooks Hooks

    /rest/v2.0/companies/{company_id}/webhooks/hooks
    /rest/v2.0/companies/{company_id}/projects/{project_id}/webhooks/hooks
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def _endpoint(self, company_id, project_id=None):
        if project_id is not None:
            return f"/rest/v2.0/companies/{company_id}/projects/{project_id}/webhooks/hooks"
        return f"/rest/v2.0/companies/{company_id}/webhooks/hooks"

    def list(
        self,
        company_id,
        project_id=None,
        namespace=None,
        payload_version=None,
        include_trigger_count=None,
        page=None,
        per_page=None,
        return_request_obj=False,
    ):
        params = {}

        if namespace is not None:
            params["namespace"] = namespace

        if payload_version is not None:
            params["payload_version"] = payload_version

        if include_trigger_count is not None:
            params["include_trigger_count"] = include_trigger_count

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

    def get(self, company_id, hook_id, project_id=None, return_request_obj: bool = False):
        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.get_request(
            f"{self._endpoint(company_id, project_id)}/{hook_id}",
            additional_headers=additional_headers,
            return_request_obj=return_request_obj,
        )

    def create(
        self,
        company_id,
        destination_url,
        payload_version,
        namespace,
        project_id=None,
        destination_headers=None,
        return_request_obj: bool = False,
    ):
        payload = {
            "destination_url": destination_url,
            "payload_version": payload_version,
            "namespace": namespace,
        }

        if destination_headers is not None:
            payload["destination_headers"] = destination_headers

        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.post_request(
            self._endpoint(company_id, project_id),
            additional_headers=additional_headers,
            data=payload,
            return_request_obj=return_request_obj,
        )

    def update(
        self,
        company_id,
        hook_id,
        project_id=None,
        destination_url=None,
        payload_version=None,
        namespace=None,
        destination_headers=None,
        status=None,
        return_request_obj: bool = False,
    ):
        payload = {}

        if destination_url is not None:
            payload["destination_url"] = destination_url

        if payload_version is not None:
            payload["payload_version"] = payload_version

        if namespace is not None:
            payload["namespace"] = namespace

        if destination_headers is not None:
            payload["destination_headers"] = destination_headers

        if status is not None:
            payload["status"] = status

        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.patch_request(
            f"{self._endpoint(company_id, project_id)}/{hook_id}",
            additional_headers=additional_headers,
            data=payload,
            return_request_obj=return_request_obj,
        )

    def delete(self, company_id, hook_id, project_id=None, return_request_obj: bool = False):
        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.delete_request(
            f"{self._endpoint(company_id, project_id)}/{hook_id}",
            additional_headers=additional_headers,
            return_request_obj=return_request_obj,
        )
