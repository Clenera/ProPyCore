from .base import Base
from ..exceptions import NotFoundItemError


class Submittal(Base):
    """
    Access and work with submittals in a given project.
    https://developers.procore.com/reference/rest/submittals?version=latest
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        # Different submittal endpoints use different API versions.
        self.endpoint = "/rest"

    def get_statuses(
        self,
        company_id,
        project_id,
        return_request_obj: bool = False,
    ):
        """
        Get all available submittal statuses.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        return_request_obj : bool, default False
            If True, return the underlying requests.Response object.

        Returns
        -------
        list or requests.Response
            Available submittal statuses or the raw response object.
        """
        headers = {
            "Procore-Company-Id": str(company_id),
        }

        return self.get_request(
            api_url=(f"{self.endpoint}/v1.0/projects/{project_id}" "/submittals/filter_options/status_id"),
            additional_headers=headers,
            return_request_obj=return_request_obj,
        )

    def get_types(
        self,
        company_id,
        project_id,
        return_request_obj: bool = False,
    ):
        """
        Get all available submittal types.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        return_request_obj : bool, default False
            If True, return the underlying requests.Response object.

        Returns
        -------
        list or requests.Response
            Available submittal types or the raw response object.
        """
        headers = {
            "Procore-Company-Id": str(company_id),
        }

        return self.get_request(
            api_url=(f"{self.endpoint}/v1.0/projects/{project_id}" "/submittals/filter_options/type"),
            additional_headers=headers,
            return_request_obj=return_request_obj,
        )

    def get(
        self,
        company_id,
        project_id,
        page=1,
        per_page=100,
        status_ids=None,
        types=None,
        return_request_obj: bool = False,
    ):
        """
        Get submittals for a project.

        By default, all pages are retrieved and combined into one list. When
        return_request_obj is True, only the requested page is retrieved and
        the underlying requests.Response object is returned.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        page : int, default 1
            Starting page number. In raw-response mode, this is the only page
            retrieved.
        per_page : int, default 100
            Number of submittals to include per page.
        status_ids : int, str, or list, default None
            Filter by one or more status IDs.
        types : str or list, default None
            Filter by one or more submittal types.
        return_request_obj : bool, default False
            If True, return the raw response for the requested page instead of
            automatically retrieving all pages.

        Returns
        -------
        list or requests.Response
            Submittals or the raw response object.
        """
        headers = {
            "Procore-Company-Id": str(company_id),
        }

        params = {
            "page": page,
            "per_page": per_page,
        }

        if status_ids is not None:
            if not isinstance(status_ids, list):
                status_ids = [status_ids]

            params["filters[status_id]"] = [str(status_id) for status_id in status_ids]

        if types is not None:
            if not isinstance(types, list):
                types = [types]

            params["filters[type]"] = [str(submittal_type) for submittal_type in types]

        api_url = f"{self.endpoint}/v1.1/projects/{project_id}/submittals"

        if return_request_obj:
            return self.get_request(
                api_url=api_url,
                additional_headers=headers,
                params=params,
                return_request_obj=True,
            )

        submittals = []

        while True:
            submittal_selection = self.get_request(
                api_url=api_url,
                additional_headers=headers,
                params=params,
            )

            if not submittal_selection:
                break

            submittals.extend(submittal_selection)
            params["page"] += 1

        return submittals

    def show(
        self,
        company_id,
        project_id,
        submittal_id,
        return_request_obj: bool = False,
    ):
        """
        Get a specific submittal.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        submittal_id : int
            Unique identifier for the submittal.
        return_request_obj : bool, default False
            If True, return the underlying requests.Response object.

        Returns
        -------
        dict or requests.Response
            Submittal information or the raw response object.
        """
        headers = {
            "Procore-Company-Id": str(company_id),
        }

        return self.get_request(
            api_url=(f"{self.endpoint}/v1.1/projects/{project_id}" f"/submittals/{submittal_id}"),
            additional_headers=headers,
            return_request_obj=return_request_obj,
        )

    def create(
        self,
        company_id,
        project_id,
        submittal_body,
        params={},
        return_request_obj: bool = False,
    ):
        """
        Create a submittal.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        submittal_body : dict
            Submittal fields accepted by the Procore API. The SDK wraps this
            dictionary inside the required ``submittal`` property.
        return_request_obj : bool, default False
            If True, return the underlying requests.Response object.

        Returns
        -------
        dict or requests.Response
            Created submittal or the raw response object.
        """
        headers = {
            "Procore-Company-Id": str(company_id),
        }

        body = {
            "submittal": submittal_body,
        }

        return self.post_request(
            api_url=(f"{self.endpoint}/v1.0/projects/{project_id}/submittals"),
            additional_headers=headers,
            json=body,
            params=params,
            return_request_obj=return_request_obj,
        )

    def find(
        self,
        company_id,
        project_id,
        identifier,
        return_request_obj: bool = False,
    ):
        """
        Find a submittal by ID or exact title.

        Parameters
        ----------
        company_id : int
            Unique identifier for the company.
        project_id : int
            Unique identifier for the project.
        identifier : int or str
            Submittal ID or exact submittal title.
        return_request_obj : bool, default False
            If True, return the raw response from the final show request.

        Returns
        -------
        dict or requests.Response
            Matching submittal or the raw response object.

        Raises
        ------
        NotFoundItemError
            Raised when no matching submittal is found.
        """
        submittals = self.get(
            company_id=company_id,
            project_id=project_id,
        )

        key = "id" if isinstance(identifier, int) else "title"

        for submittal in submittals:
            if submittal.get(key) == identifier:
                return self.show(
                    company_id=company_id,
                    project_id=project_id,
                    submittal_id=submittal["id"],
                    return_request_obj=return_request_obj,
                )

        raise NotFoundItemError(f"Could not find Submittal {identifier}")
