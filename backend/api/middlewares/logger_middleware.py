from collections.abc import Callable
from typing import Any
from datetime import datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.utils import logging


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
        logging.logger_setup(enqueue=False, diagnose=True)

        time_start = datetime.now()
        response = await call_next(request)
        time_end = datetime.now()

        data = (
            "datetime of request: {}".format(time_start.isoformat(timespec='milliseconds')),
            "request parameters: {}".format(dict(request.query_params)),
            "duration of execution: {} ms".format((time_end-time_start).microseconds/1000)
        )

        logging.logger.info("current log: {}", data)
        return response
