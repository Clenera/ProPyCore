import urllib
import requests

from ..exceptions import raise_exception


class Base:
    """
    Base class for Procore API access
    """

    def __init__(self, access_token, server_url) -> None:
        """
        Initializes important API access parameters

        Creates
        -------
        __access_token : str
            token to access Procore resources
        __server_url : str
            base url to send GET/POST requests
        """

        self.__access_token = access_token
        self.__server_url = server_url

    def _request(
        self,
        method,
        api_url,
        additional_headers=None,
        params=None,
        return_request_obj: bool = False,
        **kwargs,
    ):
        """Build the auth headers/URL and dispatch a request via ``requests.request``.

        Parameters
        ----------
        method : str
            HTTP method to use (e.g. "GET", "POST", "PATCH", "DELETE")
        api_url : str
            endpoint for the specific API call
        additional_headers : dict, default None
            additional headers beyond Authorization
        params : dict, default None
            query parameters to append to the URL
        return_request_obj : bool, default False
            If True, return the underlying ``requests.Response`` object
            instead of the parsed JSON / default return type.
        **kwargs
            forwarded directly to ``requests.request`` (e.g. ``data``, ``json``, ``files``)

        Returns
        -------
        dict or requests.Response
            By default, the parsed JSON response, or for DELETE requests a
            dict containing the status code (``{"status_code": response.status_code}``).
            If ``return_request_obj`` is True, returns the raw
            ``requests.Response`` object instead.
        """

        if params is None:
            url = self.__server_url + api_url
        else:
            url = self.__server_url + api_url + "?" + urllib.parse.urlencode(params, doseq=True)

        headers = {"Authorization": f"Bearer {self.__access_token}"}
        if additional_headers is not None:
            headers.update(additional_headers)

        response = requests.request(method, url, headers=headers, **kwargs)

        if not response.ok:
            raise_exception(response)

        if return_request_obj:
            return response

        if method == "DELETE":
            return {"status_code": response.status_code}

        return response.json()

    def get_request(
        self,
        api_url,
        additional_headers=None,
        params=None,
        return_request_obj: bool = False,
    ):
        """Create an HTTP GET request.

        Parameters
        ----------
        api_url : str
            endpoint for the specific API call
        additional_headers : dict, default None
            additional headers beyond Authorization
        params : dict, default None
            GET parameters to parse
        return_request_obj : bool, default False
            If True, return the underlying ``requests.Response`` object
            instead of the parsed JSON / default return type.

        Returns
        -------
        dict or requests.Response
            By default, the GET response in JSON (``response.json()``).
            If ``return_request_obj`` is True, returns the raw
            ``requests.Response`` object instead.
        """

        return self._request(
            "GET",
            api_url,
            additional_headers=additional_headers,
            params=params,
            return_request_obj=return_request_obj,
        )

    def post_request(
        self,
        api_url,
        additional_headers=None,
        params=None,
        data=None,
        json=None,
        files=None,
        return_request_obj: bool = False,
    ):
        """Create an HTTP POST request.

        Parameters
        ----------
        api_url : str
            endpoint for the specific API call
        additional_headers : dict, default None
            additional headers beyond Authorization
        params : dict, default None
            Query parameters for the POST request
        data : dict, default None
            POST data to send. Treated as the JSON body unless ``files`` is set.
        json : dict, default None
            POST data to send as the JSON body. Takes precedence over ``data``
            when ``files`` is not set.
        files : list of tuple, default None
            open files to send to Procore
        return_request_obj : bool, default False
            If True, return the underlying ``requests.Response`` object
            instead of the parsed JSON / default return type.

        Returns
        -------
        dict or requests.Response
            By default, the POST response in JSON (``response.json()``).
            If ``return_request_obj`` is True, returns the raw
            ``requests.Response`` object instead.
        """

        if files is not None:
            request_kwargs = {"data": data, "files": files}
        else:
            request_kwargs = {"json": json if json is not None else data}

        return self._request(
            "POST",
            api_url,
            additional_headers=additional_headers,
            params=params,
            return_request_obj=return_request_obj,
            **request_kwargs,
        )

    def patch_request(
        self,
        api_url,
        additional_headers=None,
        params=None,
        data=None,
        json=None,
        files=False,
        return_request_obj: bool = False,
    ):
        """Create an HTTP PATCH request.

        Parameters
        ----------
        api_url : str
            endpoint for the specific API call
        additional_headers : dict, default None
            additional headers beyond Authorization
        params : dict, default None
            PATCH parameters to parse
        data : dict, default None
            PATCH data to send. Treated as the JSON body unless ``files`` is set.
        json : dict, default None
            PATCH data to send as the JSON body. Takes precedence over ``data``
            when ``files`` is False.
        files : dict or boolean, default False
            False - updating folder so use JSON request
            True - updating file, but no file to include
            dict - updating file with new document
        return_request_obj : bool, default False
            If True, return the underlying ``requests.Response`` object
            instead of the parsed JSON / default return type.

        Returns
        -------
        dict or requests.Response
            By default, the PATCH response in JSON (``response.json()``).
            If ``return_request_obj`` is True, returns the raw
            ``requests.Response`` object instead.
        """

        if files is False:
            request_kwargs = {"json": json if json is not None else data}
        elif files is True:
            request_kwargs = {"data": data}
        else:
            request_kwargs = {"data": data, "files": files}

        return self._request(
            "PATCH",
            api_url,
            additional_headers=additional_headers,
            params=params,
            return_request_obj=return_request_obj,
            **request_kwargs,
        )

    def delete_request(
        self,
        api_url,
        additional_headers=None,
        params=None,
        return_request_obj: bool = False,
    ):
        """
        Execute an HTTP DELETE request.

        Parameters
        ----------
        api_url : str
            endpoint for the specific API call
        additional_headers : dict, default None
            additional headers beyond Authorization
        params : dict, default None
            DELETE parameters to parse
        return_request_obj : bool, default False
            If True, return the underlying ``requests.Response`` object
            instead of the default status-code dict.

        Returns
        -------
        dict or requests.Response
            By default, a dict containing the status code,
            ``{"status_code": response.status_code}``.
            If ``return_request_obj`` is True, returns the raw
            ``requests.Response`` object instead.
        """

        return self._request(
            "DELETE",
            api_url,
            additional_headers=additional_headers,
            params=params,
            return_request_obj=return_request_obj,
        )
