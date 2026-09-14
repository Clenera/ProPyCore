from ..base import Base


class Triggers(Base):
    """
    Procore Webhook Triggers

    Company:
    /rest/v2.0/companies/{company_id}/webhooks/hooks/{hook_id}/triggers

    Project:
    /rest/v2.0/companies/{company_id}/projects/{project_id}/webhooks/hooks/{hook_id}/triggers
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def _endpoint(self, company_id, hook_id, project_id=None):
        if project_id is not None:
            return f"/rest/v2.0/companies/{company_id}" f"/projects/{project_id}" f"/webhooks/hooks/{hook_id}/triggers"

        return f"/rest/v2.0/companies/{company_id}" f"/webhooks/hooks/{hook_id}/triggers"

    def list(
        self,
        company_id,
        hook_id,
        project_id=None,
        page=None,
        per_page=None,
        return_request_obj=False,
    ):
        params = {}

        if page is not None:
            params["page"] = page

        if per_page is not None:
            params["per_page"] = per_page

        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.get_request(
            self._endpoint(company_id, hook_id, project_id),
            additional_headers=additional_headers,
            params=params,
            return_request_obj=return_request_obj,
        )

    def create(
        self,
        company_id,
        hook_id,
        resource_name,
        event_type,
        project_id=None,
        return_request_obj=False,
    ):
        payload = {
            "resource_name": resource_name,
            "event_type": event_type,
        }

        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.post_request(
            self._endpoint(company_id, hook_id, project_id),
            additional_headers=additional_headers,
            json=payload,
            return_request_obj=return_request_obj,
        )

    def delete(
        self,
        company_id,
        hook_id,
        trigger_id,
        project_id=None,
        return_request_obj=False,
    ):
        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.delete_request(
            f"{self._endpoint(company_id, hook_id, project_id)}/{trigger_id}",
            additional_headers=additional_headers,
            return_request_obj=return_request_obj,
        )

    def bulk_create(
        self,
        company_id,
        hook_id,
        triggers,
        project_id=None,
        return_request_obj=False,
    ):
        """
        triggers = [
            {
                "resource_name": "Commitments",
                "event_type": "create"
            }
        ]
        """

        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.post_request(
            f"{self._endpoint(company_id, hook_id, project_id)}/bulk",
            additional_headers=additional_headers,
            json=triggers,
            return_request_obj=return_request_obj,
        )

    def bulk_delete(
        self,
        company_id,
        hook_id,
        trigger_ids,
        project_id=None,
        return_request_obj=False,
    ):
        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self._request(
            "DELETE",
            f"{self._endpoint(company_id, hook_id, project_id)}/bulk",
            additional_headers=additional_headers,
            json=trigger_ids,
            return_request_obj=return_request_obj,
        )
