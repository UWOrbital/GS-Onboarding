from collections.abc import Callable
from time import time 
from typing import Any
from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from backend.utils.logging import logger_setup, logger_close


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

        #logger_setup() assuming this is run during startup

        logger.info(f"Incoming request: {request.method} {request.url.path}");
        logger.info(f"Params: {request.query_params}");
        logger.info(f"Headers: {dict(request.headers)}");

        try:
            start_time = time()
            response = await call_next(request)
            end_time = time() - start_time

            logger.info(f"Outgoing response: {request.method} {request.url.path}")
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            logger.info(f"Response time: {end_time}")

            #await logger_close()
            return response

        except Exception as e:
            #await logger_close()
            raise

       
