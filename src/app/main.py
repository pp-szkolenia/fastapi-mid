from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
import time

from app.routers import tasks, users, auth
from app.middleware import confirm_deletion, log_operations


app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    title="Task manager API",
    description="Description of my API which is visible in the documentation",
    version="1.0.0"
)
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", description="Test endpoint for demonstration purposes")
def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Hello world!"})


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)

    print("Response type:", type(response))  # not the actual response object

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


app.middleware("http")(confirm_deletion)
app.middleware("http")(log_operations)
