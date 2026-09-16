import warnings

from ..base import Base
from ...exceptions import NotFoundItemError


class People(Base):
    """Access user information on a Company and Project Level"""

    def get_url(self, company_id, project_id=None):
        """
        Returns the url specific to People at company or project level

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int, default None
            unique identifier for the project
            None specifies company-level

        Returns
        -------
        <get_url> : str
            url for People request
        """
        if project_id is None:
            return f"/rest/v1.0/companies/{company_id}/people"
        else:
            return f"/rest/v1.0/projects/{project_id}/people"

    def list(
        self,
        company_id,
        project_id=None,
        per_page=1000,
    ):
        """
        Gets a list of all people from the company or project level

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int, default None
            unique identifier for the project
            None specifies company-level
        per_page : int, default 100
            number of companies to include

        Returns
        -------
        people : list of dict
            list where each value is a dict with a person's information
        """
        people = []
        n_people = 1
        page = 1

        while n_people > 0:
            params = {
                "page": page,
                "per_page": per_page,
                "company_id": company_id,  # this parameter is only used in Company Vendors, but including it for other requests does not seem to create any issues
            }

            headers = {"Procore-Company-Id": str(company_id)}
            url = self.get_url(
                company_id=company_id,
                project_id=project_id,
            )
            people_per_page = self.get_request(
                api_url=url,
                additional_headers=headers,
                params=params,
            )

            n_people = len(people_per_page)
            people += people_per_page
            page += 1

        return people

    def show(
        self,
        company_id,
        person_id,
        project_id=None,
        return_request_obj=False,
    ):

        headers = {"Procore-Company-Id": str(company_id)}

        return self.get_request(
            api_url=(f"{self.get_url(company_id, project_id)}/{person_id}"),
            additional_headers=headers,
            return_request_obj=return_request_obj,
        )

    # ------------------------------------------------------------------
    # Deprecated aliases
    # ------------------------------------------------------------------

    def get(
        self,
        company_id,
        project_id=None,
        per_page=1000,
    ):
        """
        Gets a list of all people from the company or project level

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int, default None
            unique identifier for the project
            None specifies company-level
        per_page : int, default 100
            number of companies to include

        Returns
        -------
        people : list of dict
            list where each value is a dict with a person's information
        """
        warnings.warn(
            "People.get() is deprecated and will be removed in a future " "release. Use People.list() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.list(
            company_id=company_id,
            project_id=project_id,
            per_page=per_page,
        )

    def find(
        self,
        company_id,
        person_id,
        project_id=None,
    ):
        warnings.warn(
            "People.find() is deprecated and will be removed in a future " "release. Use People.show() for ID lookups.",
            DeprecationWarning,
            stacklevel=2,
        )

        if isinstance(person_id, int):
            return self.show(
                company_id=company_id,
                person_id=person_id,
                project_id=project_id,
            )

        if isinstance(person_id, str) and "@" in person_id:
            for person in self.list(
                company_id=company_id,
                project_id=project_id,
            ):
                if person.get("contact", {}).get("email") == person_id:
                    return person

            raise NotFoundItemError(f"Could not find Person {person_id}")

        raise TypeError(f"Invalid person_id type or format: {person_id}")
