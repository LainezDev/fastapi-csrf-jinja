from starlette.requests import Request
from typing import Dict, Any

def csrf_token_processor(csrf_cookie_name: str = "csrftoken", csrf_header_name: str = "x-csrftoken"):
    def processor(request: Request) -> Dict[str, Any]:
        csrf_token = request.cookies.get(csrf_cookie_name)
        csrf_input = (
            f'<input type="hidden" name="{csrf_cookie_name}" value="{csrf_token}">'
        )
        csrf_header = {csrf_header_name: csrf_token}
        return {
            "csrf_token": csrf_token,
            "csrf_input": csrf_input,
            "csrf_header": csrf_header,
        }
    return processor