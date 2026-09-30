from ..base import Base


class Schedules(Base):
    """
    Procore Scheduling Schedules

    /rest/v2.0/companies/{company_id}/projects/{project_id}/schedules
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def _endpoint(self, company_id, project_id):
        return f"/rest/v2.0/companies/{company_id}/projects/{project_id}/schedules"

    def list(
        self,
        company_id,
        project_id,
        page=None,
        per_page=None,
        schedule_id: str = None,
        schedule_name: str = None,
        schedule_type: str = None,
        is_active: bool = None,
        updated_at: str = None,
        sort: str = None,
        return_request_obj=False,
    ):
        """
        Fetches a list of schedules for a given project.
        Allowed values for the `schedule_type` parameter are: `ONBOARDING`, `READONLY_PROJECT_SCHEDULE`, `READONLY_ONBOARDING`, `IMPORTED_READ_WRITE_ONBOARDING`, `IMPORTED_READ_WRITE_PROJECT_SCHEDULE`, and `LOOKAHEAD_ONBOARDING`.
        The `updated_at` parameter should be in ISO 8601 format (e.g., `2023-01-01T00:00:00Z`).
        Allowed values for the `sort` parameter are: `schedule_id`, `schedule_name`, `schedule_type`, `is_active`, and `updated_at`. The default sort order is ascending. To sort in descending order, prefix the field name with a minus sign (e.g., `-updated_at`).
        """

        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if schedule_id is not None:
            params["filters[schedule_id]"] = schedule_id
        if schedule_name is not None:
            params["filters[schedule_name]"] = schedule_name
        if schedule_type is not None:
            params["filters[schedule_type]"] = schedule_type
        if is_active is not None:
            params["filters[is_active]"] = str(is_active).lower()
        if updated_at is not None:
            params["filters[updated_at][gt]"] = updated_at
        if sort is not None:
            params["sort"] = sort

        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.get_request(
            self._endpoint(company_id, project_id),
            additional_headers=additional_headers,
            return_request_obj=return_request_obj,
        )

    def get(self, company_id, project_id, schedule_id, return_request_obj=False):
        """
        Fetches a specific schedule by its ID for a given project.
        """
        additional_headers = {"Procore-Company-Id": str(company_id)}

        return self.get_request(
            f"{self._endpoint(company_id, project_id)}/{schedule_id}",
            additional_headers=additional_headers,
            return_request_obj=return_request_obj,
        )
