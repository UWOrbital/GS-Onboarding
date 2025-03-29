from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time


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

        start_time = time.time() #start time

        #log incoming request
        logging.info(f"Request recieved: {request.method} {request.url}")
        logging.info(f"Query Params: {request.query_params}")

        response = await call_next(request)

        #calculate the duration
        end_time = time.time()
        duration = ((end_time - start_time) * 1000, 2)

        #log outgoing response
        logging.info(f"Response sent: {response.status_code} in {duration}ms")
        
        return response
