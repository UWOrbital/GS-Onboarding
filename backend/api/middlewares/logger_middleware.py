from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging
from time import perf_counter

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

        start_time = perf_counter()  # start time

        #log incoming request
        logging.info(f"Request recieved: {request.method} {request.url}")
        logging.info(f"Query Params: {request.query_params}")

        response = await call_next(request)

        #read and log response body
        response_body = b"".join([chunk async for chunk in response.body_iterator])
        try:
            body_text = response_body.decode("utf-8")
            logging.info(f"Response Body: {body_text}")
        except UnicodeDecodeError:
            logging.info("Response Body: [Non-text response]")

        #calculate the duration
        end_time = perf_counter()
        duration = (end_time - start_time)*1000

        #log outgoing response
        logging.info(f"Response sent: {response.status_code} in {duration:.2f}ms")
        
        #return a new response
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
