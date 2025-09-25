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
        request_body = {}
        try: request_body = await request.json()
        except Exception as e: logger.info(f"error {e}")

        request_params = request_body.get("params")

        request_time = datetime.now()
        response = await call_next(request)
        response_time = datetime.now()
        duration_time = response_time - request_time

        logger.info(f"Request made at time: {request_time}, with parameters: {request_params}, and duration: {duration_time.total_seconds()} seconds")

        return response
