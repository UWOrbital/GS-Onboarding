from collections.abc import Callable
from typing import Any, Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# LOGGING:
from datetime import datetime, timezone
from time import perf_counter
from backend.utils.logging import logger


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
        start_time = perf_counter()
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        method = request.method
        path = request.url
        content_type = request.headers.get("content-type")
        query_params = request.query_params
        path_params = request.path_params

        # Log the request as it comes in! Incoming request logging!
        logger.info(
            f"Incoming request | "
            f"content_type={content_type} | "
            f"time={end_time} | "
            f"method={method} | "
            f"path={path} | "
            f"query_params={query_params} | "
            f"path_params={path_params}"
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = (perf_counter() - start_time) * 1000

            #The very much potential error
            logger.error(
                f"Request failed | "
                f"content_type={content_type} | "
                f"method={method} | "
                f"path={path} | "
                f"path_params={path_params} | "
                f"duration_ms={duration_ms:.2f} | "
                f"error={exc}"
            )
            # raise the error and stop logging
            raise

        duration_ms = (perf_counter() - start_time) * 1000

        # Outgoing logging for both sides!
        logger.info(
            f"Outgoing response | "
            f"content_type={content_type} | "
            f"method={method} | "
            f"path={path} | "
            f"path_params={path_params} | "
            f"status_code={response.status_code} | "
            f"duration_ms={duration_ms:.2f}"
        )

        return response