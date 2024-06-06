# fastapi-csrf-jinja

`fastapi-csrf-jinja` is a CSRF middleware for FastAPI applications that supports tokens in both headers and HTML forms. This library is based on `starlette-csrf`, with additional support for Jinja template integration.

## How it works?

1. The user makes a first request with a method considered safe (by default `GET`, `HEAD`, `OPTIONS`, `TRACE`).
2. It receives in response a cookie (named by default `csrftoken`) which contains a secret value.
3. When the user wants to make an unsafe request, the server expects them to send the same secret value in a header (named by default `x-csrftoken`). Additionally, the middleware now allows submission of the token via HTML forms using Jinja.
4. The middleware compares the secret value provided in the cookie with the value in the header or form:
   * If they match, the request is processed.
   * Otherwise, a `403 Forbidden` error response is given.

## Features
- Supports CSRF tokens in headers and HTML forms.
- Jinja template processor for easy CSRF token management in forms.

## Installation

```bash
pip install fastapi-csrf-jinja
```

## Usage with FastAPI

```py
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi_csrf_jinja.middleware import FastAPICSRFJinjaMiddleware
from fastapi_csrf_jinja.jinja_processor import csrf_token_processor

app = FastAPI()

cookie_name = "your_cookie_name"
header_name = "your_header_name"

app.add_middleware(
   FastAPICSRFJinjaMiddleware, 
   secret = "your_secret",
   cookie_name = cookie_name,
   header_name = header_name,
   )

templates = Jinja2Templates(
    directory="templates", 
    context_processors=[csrf_token_processor(cookie_name, header_name)]
    )
```

- Defaults to `cookie_name` as `"csrftoken"` and `header_name` as `"x-csrftoken"` if not specified.

## Usage with Jinja and HTML forms

Now, the middleware integrates with a context processor, a function that returns a dictionary containing the CSRF token, CSRF input, and CSRF header for use with other tools such as HTMX.

Simply using {{ csrf_input | safe }} in each form is now sufficient to ensure a more secure web application. For example:

```html
<form method="post">
    {{ csrf_input | safe }}
    <!-- Other form fields here -->
    <button type="submit">Submit</button>
</form>
```

Furthermore, we can use {{ csrf_header }} in HTMX requests. For example:

```html
<form hx-patch="/route/edit" hx-headers='{{ csrf_header | tojson | safe }}'  hx-trigger="submit" hx-target="#yourtarget" hx-swap="outerHTML" >
    <!-- Other form fields here -->
    <button type="submit">Submit</button>
</form>
```

## Arguments

* `secret` (`str`): Secret to sign the CSRF token value. **Be sure to choose a strong passphrase and keep it SECRET**.
* `required_urls` (`Optional[List[re.Pattern]]` - `None`): List of URL regexes that the CSRF check should **always** be enforced, no matter the method or the cookies present.
* `exempt_urls` (`Optional[List[re.Pattern]]` - `None`): List of URL regexes that the CSRF check should be skipped on. Useful if you have any APIs that you know do not need CSRF protection.
* `sensitive_cookies` (`Set[str]` - `None`): Set of cookie names that should trigger the CSRF check if they are present in the request. Useful if you have other authentication methods that don't rely on cookies and don't need CSRF enforcement. If this parameter is `None`, the default, CSRF is **always** enforced.
* `safe_methods` (`Set[str]` - `{"GET", "HEAD", "OPTIONS", "TRACE"}`): HTTP methods considered safe which don't need CSRF protection.
* `cookie_name` (`str` - `csrftoken`): Name of the cookie.
* `cookie_path` `str` - `/`): Cookie path.
* `cookie_domain` (`Optional[str]` - `None`): Cookie domain. If your frontend and API lives in different sub-domains, be sure to set this argument with your root domain to allow your frontend sub-domain to read the cookie on the JavaScript side.
* `cookie_secure` (`bool` - `False`): Whether to only send the cookie to the server via SSL request.
* `cookie_samesite` (`str` - `lax`): Samesite strategy of the cookie.
* `header_name` (`str` - `x-csrftoken`): Name of the header where you should set the CSRF token.

## License

This project is licensed under the terms of the MIT license.
