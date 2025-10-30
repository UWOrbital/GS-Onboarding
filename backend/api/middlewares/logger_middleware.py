from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from backend.utils.logging import logger
import time

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
        start_time = time.perf_counter()

        date_time = datetime.now()

        method = request.method
        url = str(request.url)
        
        if request.client:
            client = request.client.host
        else:
            client = "client unknown"

        logger.info(
            f'"Incoming request | method:" {method} | '
            f'"url:" {url} | '
            f'"client:" {client} | '
            f'"request datetime:" {date_time} | '
        )

        try:
            response = await call_next(request)
            status = response.status_code
            duration = time.perf_counter() - start_time

            logger.info(
                f'"Outgoing response | status:" {status} | '
                f'"duration:" {duration:.2f} | '
                f'"method:" {method}| '
                f'"url:" {url} | '
            )

            return response
        
        except Exception as e:
            logger.error(
                f"Error: method: {method} | url: {url} | client: {client}"
                f"Error: {e}"
            )
            raise ValueError("Error processing incoming request")