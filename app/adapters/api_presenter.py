import json
from typing import Optional

from ..application.interfaces.username_password_auth_response \
    import UsernamePasswordAuthOutputBoundary, UsernamePasswordAuthResponseModel


class ApiAuthTokenPresenter(UsernamePasswordAuthOutputBoundary):
    """_summary_
    """

    def __init__(self) -> None:
        self._response: str = "{}"

    def form_response(self,
                      response_data: UsernamePasswordAuthResponseModel) -> None:
        if response_data.success:
            response = {
                "status": "success",
                "message": response_data.message,
                "data": {
                    "user": {
                        "id": response_data.user.id,
                        "name": response_data.user.name,
                        "email": response_data.user.email
                    },
                    "token": {
                        "accessToken": response_data.token.access_token,
                        "tokenType": response_data.token.token_type,
                        "expiresIn": response_data.token.expires_in
                    }
                }
            }
        else:
            response = {
                "status": "error",
                "message": response_data.message,
            }
        self._response = json.dumps(response)

    @property
    def response(self) -> str:
        return self._response
