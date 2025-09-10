from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from backend.utils.logging import logger
from datetime import datetime
import json

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method

        start_time = datetime.now()
        request_datetime = datetime.now().isoformat()
        
        # Try reading request body
        try:
            body_bytes = await request.body()
            request_body = body_bytes.decode("utf-8") if body_bytes else None
        except Exception:
            request_body = "Unable to read body"

        # log request info
        logger.info(
            f"Incoming Request at Time: {request_datetime} with Method: {request.method} for Url: {request.url}, Headers: {dict(request.headers)}, Params: {dict(request.query_params)}, and Body: {request_body}"
        )

        # process request
        response = await call_next(request)

        # compute duration
        current_time = datetime.now()
        duration = (current_time - start_time).total_seconds()

        logger.info(f"Outgoing Response with Status Code: {response.status_code}, headers: {dict(response.headers)}, Media Type: {response.media_type}. Duration was {duration:.6f} seconds")
        
        return response
