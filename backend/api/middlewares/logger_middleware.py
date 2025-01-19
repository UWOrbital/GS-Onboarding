from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from ...utils.logging import logger_setup, logger_setup_file, logger_close, logger
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
        # Set up the logger
        logger_setup_file(enqueue=True, diagnose=True)


        # Log the incoming request
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.info(f"Request headers: {dict(request.headers)}")

        try:
            body = await request.json()
            logger.info(f"Request body: {body}")
        except Exception as e:
            logger.warning(f"Request body could not be read or is empty. Error: {str(e)}")

        # Measure request duration
        start_time = time()

        # Call the next middleware or the endpoint
        response = await call_next(request)

        # Calculate the duration of the request
        execution_time = time() - start_time

        # Log the response details
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        logger.info(f"Response Time: {execution_time:.6f} seconds")

        await logger_close()

        return response
