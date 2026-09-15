from ..base import Base


class ChangeOrders(Base):
    """
    Procore Commitment Change Orders

    /rest/v1.0/projects/{project_id}/commitment_change_orders
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def _endpoint(self, company_id, project_id):
        # Doesn't use company_id
        return f"/rest/v1.0/projects/{project_id}/commitment_change_orders"

    def list(
        self,
        company_id,
        project_id,
        view="default",
        page=None,
        per_page=None,
        return_request_obj=False,
    ):
        params = {"view": view}

        if page is not None:
            params["page"] = page

        if per_page is not None:
            params["per_page"] = per_page

        return self.get_request(
            self._endpoint(company_id, project_id),
            additional_headers={"Procore-Company-Id": str(company_id)},
            params=params,
            return_request_obj=return_request_obj,
        )

    def get(
        self,
        company_id,
        project_id,
        id,
        view="default",
        return_request_obj=False,
    ):
        return self.get_request(
            f"{self._endpoint(company_id, project_id)}/{id}",
            additional_headers={"Procore-Company-Id": str(company_id)},
            params={"view": view},
            return_request_obj=return_request_obj,
        )

    def update(
        self,
        company_id,
        project_id,
        id,
        update_body,
        run_configurable_validations=True,
        view="default",
        return_request_obj=False,
    ):
        """
        https://developers.procore.com/reference/rest/commitment-change-orders?version=latest#update-commitment-change-order
        Update Body Schema:
        {
          "change_order": {
            "contract_id": 512340,
            "batch_id": 512340,
            "change_order_change_reason_id": 512340,
            "location_id": 512340,
            "designated_reviewer_id": 512340,
            "received_from_id": 512340,
            "description": "New Building",
            "due_date": "2017-03-31",
            "paid_date": "2017-03-31",
            "invoiced_date": "2017-03-31",
            "title": "Station 3",
            "status": "draft",
            "reference": "Reference",
            "number": "CO-1",
            "revision": 1,
            "field_change": "Field Change",
            "signature_required": true,
            "signed_change_order_received_date": "2015-01-30",
            "schedule_impact_amount": 5,
            "executed": true,
            "private": true,
            "paid": true,
            "reason": "Material cost increase",
            "custom_field_%{custom_field_definition_id}": "string",
            "enable_ssov": false,
            "revised_substantial_completion_date": "2017-10-30",
            "change_event_attachment_ids": [
              42
            ],
            "request_for_quote_attachment_ids": [
              42
            ],
            "attachment_ids": [
              42
            ],
            "drawing_revision_ids": [
              42
            ],
            "file_version_ids": [
              42
            ],
            "form_ids": [
              42
            ],
            "image_ids": [
              42
            ],
            "upload_ids": [
              "string"
            ]
          }
        }
        """

        if type(update_body) is not dict:
            raise ValueError("update_body must be a dictionary")
        if not update_body:
            raise ValueError("update_body cannot be empty")
        if not "change_order" in update_body:
            update_body = {"change_order": update_body}

        return self.patch_request(
            f"{self._endpoint(company_id, project_id)}/{id}",
            additional_headers={"Procore-Company-Id": str(company_id)},
            json=update_body,
            params={
                "view": view,
                "run_configurable_validations": run_configurable_validations,
            },
            return_request_obj=return_request_obj,
        )
