import time
import logging
from collections.abc import Callable
from typing import Any
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging to ensure it is readable in the terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s"
)
logger = logging.getLogger("api_logger")

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs.
        """
        # 1. Record the start time and request metadata
        start_time = time.time()
        method = request.method
        url = request.url.path
        query_params = dict(request.query_params)

        # 2. Process the request to get the response
        try:
            response = await call_next(request)
        except Exception as e:
            # Ensure errors are logged if the endpoint crashes
            logger.error(f"Request Failed | {method} {url} | Error: {str(e)}")
            
            # Raise an HTTPException with the error detail and a 500 status code
            raise HTTPException(status_code=500, detail=str(e))

        # 3. Calculate duration
        process_time = (time.time() - start_time) * 1000  # Duration in milliseconds

        # 4. Format and print the logs
        log_message = (
            f"\n"
            f"--- Request Log ---\n"
            f"Method:     {method}\n"
            f"Path:       {url}\n"
            f"Params:     {query_params}\n"
            f"Status:     {response.status_code}\n"
            f"Duration:   {process_time:.2f}ms\n"
            f"-------------------"
        )
        
        logger.info(log_message)

        return response