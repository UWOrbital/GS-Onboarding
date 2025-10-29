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
        params = dict(request.query_params)
        start_time = time.perf_counter()
        start_date = datetime.now()

        if params:
            logger.info(f"{params} was requested at {start_date}")
        else:
            logger.info(f"no params requested at {start_date}")

        response = await call_next(request)
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        end_date = datetime.now()
        logger.info(f"response executed in {duration} ms")

        return response
    

