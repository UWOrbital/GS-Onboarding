from collections.abc import Callable
from time import time 
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from ...utils.logging import logger


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

        start_time = time()

        try:
            response = await call_next(request)
        except Exception as e:
            logger.warning(f"Error calling next middleware!. Error: {str(e)}")


        logger.info(f"Outgoing response: {request.method} {request.url.path}")
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        
        try:
            body = await request.json()
            logger.info(f"Request body: {body}")
        except Exception as e:
            logger.warning(f"Error reading body!. Error: {str(e)}")


        end_time = time() - start_time
        logger.info(f"Response time: {end_time}")
  
        return response



       
