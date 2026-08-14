from pydantic import BaseModel


class EnqueueRequest(BaseModel):
    function_name: str
    job_data: str


class EnqueueResponse(BaseModel):
    job_id: str
    status: str = "queued"


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: str | None = None
