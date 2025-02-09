from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import time
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
        logger.info(f'Date of request: {datetime.now().strftime('%A, %d. %B %Y %I: %M%p')}.')
        logger.info(f'<underline>REQUEST INFORMATION</underline>\nMethod: {request.method} URL: {request.url} Path Params:{request.path_params} Status: {request.state}')
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        logger.info(f'Duration: {end_time-start_time} seconds.')
        return response