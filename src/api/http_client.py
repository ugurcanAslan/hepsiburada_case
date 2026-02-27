import json
import ssl
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


@dataclass
class HttpResponse:
    status_code: int
    headers: Dict[str, str]
    text: str

    def json(self) -> Any:
        if not self.text:
            return None
        return json.loads(self.text)


class HttpClient:
    def __init__(self, base_url: str, timeout: int = 20, verify_ssl: bool = True):
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.verify_ssl = verify_ssl

    def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Any] = None,
    ) -> HttpResponse:
        url = urljoin(self.base_url, path.lstrip("/"))
        req_headers = dict(headers or {})
        payload = None

        if json_body is not None:
            payload = json.dumps(json_body).encode("utf-8")
            req_headers.setdefault("Content-Type", "application/json")

        request = Request(url=url, method=method.upper(), headers=req_headers, data=payload)
        ssl_context = None
        if not self.verify_ssl:
            ssl_context = ssl._create_unverified_context()

        try:
            with urlopen(request, timeout=self.timeout, context=ssl_context) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return HttpResponse(
                    status_code=resp.getcode(),
                    headers=dict(resp.headers.items()),
                    text=body,
                )
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            return HttpResponse(
                status_code=exc.code,
                headers=dict(exc.headers.items()) if exc.headers else {},
                text=body,
            )
        except URLError as exc:
            raise AssertionError(f"Request failed for {method.upper()} {url}: {exc}") from exc

    def get(self, path: str, headers: Optional[Dict[str, str]] = None) -> HttpResponse:
        return self.request("GET", path, headers=headers)

    def post(
        self,
        path: str,
        json_body: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> HttpResponse:
        return self.request("POST", path, headers=headers, json_body=json_body)
