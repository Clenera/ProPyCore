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

        data = {"file": (file_name, file, "application/octet-stream")}

        return self.put_request(
            self._endpoint(company_id, project_id, schedule_id),
            additional_headers=additional_headers,
            files=data,
            return_request_obj=return_request_obj,
        )

    def check_import_status(
        self,
        company_id,
        project_id,
        schedule_id: int,
        job_id: int,
        return_request_obj=False,
    ):
        """
        Check the status of a schedule import for a given project.
        """
        additional_headers = {
            "Procore-Company-Id": str(company_id),
            "locale": "en",
        }

        endpoint = self._endpoint(company_id, project_id, schedule_id) + f"s/{job_id}"

        return self.get_request(
            endpoint,
            additional_headers=additional_headers,
            return_request_obj=return_request_obj,
        )

    def get_import_logs(
        self,
        company_id,
        project_id,
        schedule_id: int,
        job_id: int,
        return_request_obj=False,
    ):
        """
        Fetch the logs for a schedule import job.
        """
        additional_headers = {
            "Procore-Company-Id": str(company_id),
        }

        endpoint = (
            self._endpoint(company_id, project_id, schedule_id) + f"s/{job_id}/logs"
        )

        return self.get_request(
            endpoint,
            additional_headers=additional_headers,
            return_request_obj=return_request_obj,
        )
