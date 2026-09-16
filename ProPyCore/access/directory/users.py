import warnings

from ..base import Base
from ...exceptions import NotFoundItemError


class Users(Base):
    """Access user information at the company and project levels."""

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def _endpoint(self, company_id, project_id=None):
        if project_id is not None:
            return f"/rest/v1.0/projects/{project_id}/users"

        return f"/rest/v1.1/companies/{company_id}/users"

    def _headers(self, company_id):
        return {"Procore-Company-Id": str(company_id)}

    def list(
        self,
        company_id,
        project_id=None,
        per_page=1000,
        return_request_obj=False,
    ):
        """
        List all users at the company or project level.
        """
        users = []
        page = 1

        while True:
            params = {
                "page": page,
                "per_page": per_page,
            }

            response = self.get_request(
                api_url=self._endpoint(company_id, project_id),
                additional_headers=self._headers(company_id),
                params=params,
                return_request_obj=return_request_obj,
            )

            if return_request_obj:
                return response

            if not response:
                break

            users.extend(response)
            page += 1

        return users

    def show(
        self,
        company_id,
        user_id,
        project_id=None,
        return_request_obj=False,
    ):
        """
        Show a user by their Procore user ID.
        """
        if project_id is not None:
            url = f"/rest/v1.0/projects/{project_id}/users/{user_id}"
        else:
            url = f"/rest/v1.3/companies/{company_id}/users/{user_id}"

        return self.get_request(
            api_url=url,
            additional_headers=self._headers(company_id),
            return_request_obj=return_request_obj,
        )

    def add(self, company_id, project_id, user_id, permission_template_id=None, return_request_obj=False):
        """
        Add an existing company user to a project.
        """
        payload = {
            "user": {
                "permission_template_id": permission_template_id,
            }
        }

        return self.post_request(
            api_url=(f"/rest/v1.0/projects/{project_id}" f"/users/{user_id}/actions/add"),
            additional_headers=self._headers(company_id),
            params={"project_id": project_id},
            json=payload,
            return_request_obj=return_request_obj,
        )

    # ------------------------------------------------------------------
    # Deprecated methods
    # ------------------------------------------------------------------

    def get(
        self,
        company_id,
        project_id=None,
        per_page=1000,
        return_request_obj=False,
    ):
        """
        Deprecated alias for list().
        """
        warnings.warn(
            "Users.get() is deprecated and will be removed in a future " "release. Use Users.list() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.list(
            company_id=company_id,
            project_id=project_id,
            per_page=per_page,
            return_request_obj=return_request_obj,
        )

    def find(
        self,
        company_id,
        user_id,
        project_id=None,
        return_request_obj=False,
    ):
        """
        Deprecated user lookup by ID, email address, or name.
        """
        warnings.warn(
            "Users.find() is deprecated and will be removed in a future " "release. Use Users.show() for ID lookups.",
            DeprecationWarning,
            stacklevel=2,
        )

        if isinstance(user_id, int):
            return self.show(
                company_id=company_id,
                user_id=user_id,
                project_id=project_id,
                return_request_obj=return_request_obj,
            )

        if not isinstance(user_id, str):
            raise TypeError("user_id must be an integer ID, email address, or name.")

        key = "email_address" if "@" in user_id else "name"

        for user in self.list(
            company_id=company_id,
            project_id=project_id,
            return_request_obj=return_request_obj,
        ):
            if user.get(key) == user_id:
                return user

        raise NotFoundItemError(f"Could not find User {user_id}")
