from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from backend.utils.logging import logger
from starlette.middleware.base import BaseHTTPMiddleware
from time import time


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
        logger.info(f"Req headers:{dict(request.headers)}")
        logger.info(f"Req: {request.method} {request.url}")
        try:
            body = await response.json()
            logger.info("Req Body: {body}")
        except Exception as error:
            logger.warning(f"Unable to parse Request Body.  Error: {str(error)}")
        startTime = time()
        response = await call_next(request)
        executionTime = time() - startTime
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response Headers: {response.headers}")
        logger.info(f"Response Time:{executionTime:.2f} seconds")
        return response
