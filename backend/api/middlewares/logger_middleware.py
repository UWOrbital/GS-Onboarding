from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.utils.logging import logger
from datetime import datetime
import json


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        
        start_time = datetime.now()
        request_datetime = start_time.strftime("%Y/%m/%d %H:%M")

        try:
            request_body = await request.json()
        except Exception:
            request_body = {}
        request_params = request_body.get("params", None)

        logger.info(f"Request URL: {request.url}")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request params: {request_params}")
        logger.info(f"Time of call: {request_datetime}")

        try:
            response = await call_next(request)
        except Exception:
            logger.error("Internal error", exc_info=True)
            return Response("Internal error", status_code=500)

        duration = (datetime.now() - start_time).total_seconds()

        body_chunks = [chunk async for chunk in response.body_iterator]
        raw_body = b"".join(body_chunks).decode("utf-8")

        parsed_body = raw_body
        if "application/json" in response.headers.get("content-type", "") and raw_body.strip():
            try:
                parsed_body = json.loads(raw_body)
            except json.JSONDecodeError:
                logger.info("Couldn't parse as JSON")

        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response body: {parsed_body}")
        logger.info(f"Response headers: {dict(response.headers)}")
        logger.info(f"Duration: {duration:.3f}s")

        return Response(
            content=raw_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
        
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method