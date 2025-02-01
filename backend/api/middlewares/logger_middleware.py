from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from backend.utils.logging import logger

import time
import json
from datetime import datetime


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
        logger.info(f'{request.method} {request.url.path}')
        #logger.info(f"Request Parameters: {request.path_params}")
        current_datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        logger.info(f"Datetime of request: {current_datetime}")

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start  
        logger.info(f"Duration: {duration} seconds")

        return response
