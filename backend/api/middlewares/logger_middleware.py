from time import time, strftime
from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from backend.utils.logging import logger

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        @param request: Request received to this middleware from client (it is supplied by FastAPI)
        @param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        @return Response from endpoint
        """
        # TODO:(Member) Finish implementing this method
        start_time = time()
        request_time = strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"Request started: [{request_time}] | {request.method} | {request.url.path} | Params: {request.query_params}")
        
        response = await call_next(request)

        raw_byte = b""
        async for chunk in response.body_iterator:
            raw_byte += chunk

        # Log response details and duration
        duration = time() - start_time

        logger.info(f"Response sent: {raw_byte} {response.status_code} | Duration: {duration:.4f}s")
        return Response(content=raw_byte, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)
