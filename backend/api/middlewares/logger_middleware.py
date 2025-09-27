from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from datetime import datetime
from loguru import logger


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
        logger.info(f"Request: {request.method} {request.url} at {start_time}")

        try:
            response = await call_next(request)

            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Status: {response.status_code}")
            logger.info(f"Completed in {duration:.2f} seconds")

            return response
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise e
