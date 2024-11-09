from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


# TODO:(Member) Implement this logging middleware
class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, length of time of request and response.

        @param request: Request received to this middleware
        @param call_next: Endpoint or next middleware to be called
        @return Response from endpoint
        """
        # TODO:(Member) Finish implementing this method
        response = await call_next(request)
        return response
