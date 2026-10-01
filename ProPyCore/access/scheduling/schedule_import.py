from ..base import Base
import base64


class ScheduleImport(Base):
    """
    Procore Scheduling Schedule Import

    /rest/v2.0/companies/{company_id}/projects/{project_id}/schedules/{schedule_id}/import
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def _endpoint(self, company_id, project_id, schedule_id):
        return f"/rest/v2.0/companies/{company_id}/projects/{project_id}/schedules/{schedule_id}/import"

    def import_schedule(
        self,
        company_id,
        project_id,
        schedule_id,
        file: str,
        file_name: str,
        return_request_obj=False,
    ):
        """
        Initiate the import of a schedule for a given project. The file should be in a supported format (e.g., .mpp, .xml, .xlsx).
        """
        additional_headers = {
            "Procore-Company-Id": str(company_id),
            "locale": "en",
        }

        data = {"file": (file_name, open(file, "rb"), "application/octet-stream")}

        return self.put_request(
            self._endpoint(company_id, project_id, schedule_id),
            additional_headers=additional_headers,
            files=data,
            return_request_obj=return_request_obj,
        )
