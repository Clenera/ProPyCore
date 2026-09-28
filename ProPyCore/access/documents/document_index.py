from ..base import Base
from ...exceptions import NotFoundItemError


class DocumentIndex(Base):
    """
    Access Procore documents at the company and project levels.

    Documents include both files and folders.

    Company:
    GET /rest/v2.0/companies/{company_id}/documents

    Project:
    GET /rest/v2.0/companies/{company_id}/projects/{project_id}/documents

    Revisions:
    GET /rest/v2.0/companies/{company_id}/documents/{document_id}/revisions
    GET /rest/v2.0/companies/{company_id}/projects/{project_id}/documents/{document_id}/revisions
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def _endpoint(self, company_id, project_id=None):
        if project_id is not None:
            return f"/rest/v2.0/companies/{company_id}" f"/projects/{project_id}/documents"

        return f"/rest/v2.0/companies/{company_id}/documents"

    def _headers(self, company_id):
        return {
            "Procore-Company-Id": str(company_id),
        }

    @staticmethod
    def _data(response):
        """
        Extract the data property from a v2 response.
        """
        if isinstance(response, dict):
            return response.get("data", [])

        return response

    def list(
        self,
        company_id,
        project_id=None,
        view="normal",
        sort=None,
        document_type=None,
        file_types=None,
        folder_id=None,
        search=None,
        created_by_ids=None,
        created_at=None,
        updated_at=None,
        custom_tag_ids=None,
        custom_fields=None,
        private=None,
        is_in_recycle_bin=None,
        include_descendants=None,
        page=None,
        per_page=100,
        return_request_obj=False,
    ):
        """
        List company or project documents.

        document_type:
            "file" or "folder"

        view:
            "normal" or "extended"
        """
        params = {
            "view": view,
            "per_page": per_page,
        }

        if sort is not None:
            params["sort"] = sort

        if document_type is not None:
            params["filters[document_type]"] = document_type

        if file_types is not None:
            params["filters[file_type]"] = file_types

        if folder_id is not None:
            params["filters[folder_id]"] = folder_id

        if search is not None:
            params["filters[search]"] = search

        if created_by_ids is not None:
            params["filters[created_by_id]"] = created_by_ids

        if created_at is not None:
            params["filters[created_at]"] = created_at

        if updated_at is not None:
            params["filters[updated_at]"] = updated_at

        if custom_tag_ids is not None:
            params["filters[custom_tag_ids]"] = custom_tag_ids

        if custom_fields is not None:
            params["filters[custom_fields]"] = custom_fields

        if private is not None:
            params["filters[private]"] = private

        if is_in_recycle_bin is not None:
            params["filters[is_in_recycle_bin]"] = is_in_recycle_bin

        if include_descendants is not None:
            params["include_descendants"] = include_descendants

        if page is not None:
            params["page"] = page

            return self.get_request(
                api_url=self._endpoint(company_id, project_id),
                additional_headers=self._headers(company_id),
                params=params,
                return_request_obj=return_request_obj,
            )

        documents = []
        current_page = 1

        while True:
            params["page"] = current_page

            response = self.get_request(
                api_url=self._endpoint(company_id, project_id),
                additional_headers=self._headers(company_id),
                params=params,
                return_request_obj=return_request_obj,
            )

            if return_request_obj:
                return response

            page_documents = self._data(response)

            if not page_documents:
                break

            documents.extend(page_documents)

            if len(page_documents) < per_page:
                break

            current_page += 1

        return documents

    def show(
        self,
        company_id,
        document_id,
        project_id=None,
        view="extended",
        return_request_obj=False,
    ):
        """
        Return one document by ID through the document index.

        The v2 OAS does not define a direct document show endpoint.
        """
        documents = self.list(
            company_id=company_id,
            project_id=project_id,
            view=view,
            return_request_obj=return_request_obj,
        )

        if return_request_obj:
            return documents

        document_id = str(document_id)

        for document in documents:
            if str(document.get("id")) == document_id:
                return document

        raise NotFoundItemError(f"Could not find document {document_id}")

    def search(
        self,
        company_id,
        value,
        project_id=None,
        document_type=None,
        file_types=None,
        folder_id=None,
        include_descendants=True,
        view="normal",
        sort=None,
        page=None,
        per_page=100,
        return_request_obj=False,
    ):
        """
        Search company or project documents using Procore's search filter.
        """
        return self.list(
            company_id=company_id,
            project_id=project_id,
            view=view,
            sort=sort,
            document_type=document_type,
            file_types=file_types,
            folder_id=folder_id,
            search=value,
            include_descendants=include_descendants,
            page=page,
            per_page=per_page,
            return_request_obj=return_request_obj,
        )

    def revisions(
        self,
        company_id,
        document_id,
        project_id=None,
        return_request_obj=False,
    ):
        """
        List recent revisions for a file document.
        """
        return self.get_request(
            api_url=(f"{self._endpoint(company_id, project_id)}" f"/{document_id}/revisions"),
            additional_headers=self._headers(company_id),
            return_request_obj=return_request_obj,
        )
