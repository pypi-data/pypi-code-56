import asyncio
import logging
import time
from fastapi import FastAPI, Response, Header, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import prometheus_client as pc

c = pc.Counter('nbapi_request_count', 'Count the total number of incoming request', [
               'path', 'status_code'])
g = pc.Gauge('nbapi_request_duration',
             'Gauge the duration of incoming request', ['path', 'status_code'])


class AuthError(Exception):
    pass


class NBApi(FastAPI):
    def __init__(self, title: str, cors_origins: list = []):
        super().__init__(title=title)
        if len(cors_origins) > 0:
            self.add_middleware(
                CORSMiddleware,
                allow_origins=cors_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        async def http_middleware(request: Request, call_next):
            ts = time.time()
            resp = await call_next(request)
            c.labels(path=request.url.path, status_code=resp.status_code).inc()
            g.labels(path=request.url.path, status_code=resp.status_code).set(
                time.time() - ts)
            return resp

        self.middleware('http')(http_middleware)

        async def metrics():
            return PlainTextResponse(pc.generate_latest())

        self.get('/metrics', include_in_schema=False)(metrics)

        async def handle_httperror(rec: Request, exc: StarletteHTTPException):
            logging.error(exc)
            return JSONResponse(
                status_code=200,
                content=jsonable_encoder(
                    {'status': 'failed', 'code': f'{exc.status_code}'}),
            )
        self.exception_handler(StarletteHTTPException)(handle_httperror)

        async def auth_error(rec: Request, exc: AuthError):
            logging.error(exc)
            return JSONResponse(
                status_code=200,
                content=jsonable_encoder(
                    {'status': 'failed', 'code': '401'}),
            )
        self.exception_handler(AuthError)(auth_error)

        async def handle_valueerror(rec: Request, exc: ValueError):
            logging.error(exc)
            return JSONResponse(
                status_code=200,
                content=jsonable_encoder(
                    {'status': 'failed', 'code': '400'}),
            )
        self.exception_handler(ValueError)(handle_valueerror)

        async def handle_exception(rec: Request, exc: Exception):
            logging.error(exc)
            return JSONResponse(
                status_code=200,
                content=jsonable_encoder(
                    {'status': 'failed', 'code': '500', 'msg': f'{str(exc)}'}),
            )
        self.exception_handler(Exception)(handle_exception)
