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

        if params is None:
            url = self.__server_url + api_url
        else:
            url = self.__server_url + api_url + "?" + urllib.parse.urlencode(params, doseq=True)

        headers = {"Authorization": f"Bearer {self.__access_token}"}
        if additional_headers is not None:
            for key, value in additional_headers.items():
                headers[key] = value

        response = requests.get(url, headers=headers)

        if response.ok:
            return response if return_request_obj else response.json()
        else:
            raise_exception(response)

    def post_request(
        self,
        api_url,
        additional_headers=None,
        params=None,
        data=None,
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
            POST data to send
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

        # Get URL
        if params is None:
            url = self.__server_url + api_url
        else:
            url = self.__server_url + api_url + "?" + urllib.parse.urlencode(params)

        # Get Headers
        headers = {"Authorization": f"Bearer {self.__access_token}"}
        if additional_headers is not None:
            for key, value in additional_headers.items():
                headers[key] = value

        # Make the request with file if necessary
        if files is None:
            headers["Content-Type"] = "application/json"
            response = requests.request(
                "POST",
                url,
                headers=headers,
                json=data,  # Use json parameter instead of data to properly serialize
            )
            """
            print(f"Request URL: {response.request.url}")
            print(f"Request Headers: {response.request.headers}")
            print(f"Request Data: {response.request.body}")
            """
        elif data is None:
            response = requests.request(
                "POST",
                url,
                headers=headers,
                files=files,  # use files for multipart/form-data
            )
        else:
            response = requests.request("POST", url, headers=headers, data=data, files=files)

        if response.ok:
            return response if return_request_obj else response.json()
        else:
            """
            print("Response Status Code:", response.status_code)
            print("Response Text:", response.text)
            """
            raise_exception(response)

    def patch_request(
        self,
        api_url,
        additional_headers=None,
        params=None,
        data=None,
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
            PATCH data to send
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

        # Get URL
        if params is None:
            url = self.__server_url + api_url
        else:
            url = self.__server_url + api_url + "?" + urllib.parse.urlencode(params)

        # Get Headers
        headers = {"Authorization": f"Bearer {self.__access_token}"}
        if additional_headers is not None:
            for key, value in additional_headers.items():
                headers[key] = value

        if files is False:
            response = requests.patch(
                url,
                headers=headers,
                json=data,  # json for folder update
            )
        elif files is True:
            response = requests.patch(
                url,
                headers=headers,
                data=data,  # data for file update
            )
        else:
            response = requests.patch(
                url,
                headers=headers,
                data=data,  # data for file update
                files=files,
            )

        if response.ok:
            return response if return_request_obj else response.json()
        else:
            raise_exception(response)

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

        # Get URL
        if params is None:
            url = self.__server_url + api_url
        else:
            url = self.__server_url + api_url + "?" + urllib.parse.urlencode(params)

        # Get Headers
        headers = {"Authorization": f"Bearer {self.__access_token}"}
        if additional_headers is not None:
            for key, value in additional_headers.items():
                headers[key] = value

        # DELETE request
        response = requests.delete(
            url=url,
            headers=headers,
        )

        if response.ok:
            if return_request_obj:
                return response
            return {"status_code": response.status_code}
        else:
            raise_exception(response)
