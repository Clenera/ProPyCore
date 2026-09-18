import warnings

from .base import Base
from ..exceptions import NotFoundItemError


class Projects(Base):
    """
    Access and manage Procore projects.
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/projects"

    def _headers(self, company_id):
        return {
            "Procore-Company-Id": str(company_id),
        }

    def list(
        self,
        company_id,
        status="All",
        region=None,
        per_page=100,
        return_request_obj=False,
    ):
        projects = []
        page = 1

        while True:
            params = {
                "company_id": company_id,
                "page": page,
                "per_page": per_page,
                "filters[by_status]": status,
            }

            if region is not None:
                params["filters[region]"] = region

            response = self.get_request(
                api_url=self.endpoint,
                additional_headers=self._headers(company_id),
                params=params,
                return_request_obj=return_request_obj,
            )

            if return_request_obj:
                return response

            if not response:
                break

            projects.extend(response)

            if len(response) < per_page:
                break

            page += 1

        return projects

    def show(
        self,
        company_id,
        project_id,
        view=None,
        return_request_obj=False,
    ):

        params = {
            "company_id": company_id,
        }

        if view is not None:
            params["view"] = view

        return self.get_request(
            api_url=f"{self.endpoint}/{project_id}",
            params=params,
            additional_headers=self._headers(company_id),
            return_request_obj=return_request_obj,
        )

    def update(
        self,
        company_id,
        project_id,
        project,
        return_request_obj=False,
    ):
        """
        Project should contain only the fields to update and the id.

        Example:
        {
            "name": "New Project Name",
            "city": "Boise"
        }
        """

        return self.patch_request(
            api_url=f"{self.endpoint}/{project_id}",
            additional_headers=self._headers(company_id),
            json={"project": project, "company_id": company_id},
            return_request_obj=return_request_obj,
        )

    def get_type(
        self,
        company_id,
        project_id,
    ):
        project = self.show(
            company_id=company_id,
            project_id=project_id,
        )

        return project.get("type_name")

    # ------------------------------------------------------------------
    # Deprecated methods
    # ------------------------------------------------------------------

    def get(
        self,
        company_id,
        status="All",
        region=None,
        per_page=100,
        return_request_obj=False,
    ):
        warnings.warn(
            "Projects.get() is deprecated. Use Projects.list().",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.list(
            company_id=company_id,
            status=status,
            region=region,
            per_page=per_page,
            return_request_obj=return_request_obj,
        )

    def find(
        self,
        company_id,
        identifier,
        return_request_obj=False,
    ):

        if isinstance(identifier, int):
            return self.show(
                company_id=company_id,
                project_id=identifier,
                return_request_obj=return_request_obj,
            )

        for project in self.list(
            company_id=company_id,
        ):
            if project["name"] == identifier:
                return project

        raise NotFoundItemError(f"Could not find project {identifier}")

    def get_type(self, company_id, project_id):
        """
        Gets the type for the given project

        Parameters
        ----------
        company_id : int
            The identifier for the company
        project_id : int
            The identifier for the project

        Returns
        -------
        <type_name> : str
            Project type name
        """
        headers = {"Procore-Company-Id": f"{company_id}"}
        # Get the projects from the company endpoint which has the type_name field
        company_projects = self.get_request(
            api_url=f"/rest/v1.0/companies/{company_id}/projects", additional_headers=headers, params={}
        )

        # Search for the project with the matching project_id and return the type_name
        for project in company_projects:
            if project.get("id") == project_id:
                return project.get("type_name")

        raise NotFoundItemError(f"Could not find project {project_id}")
