from fastapi import Depends

from api.auth.model import User
from api.auth.service import get_current_user
from api.jobs.schema import EnqueueRequest, EnqueueResponse, JobStatusResponse
from api.jobs.service import JobService


async def enqueue_job(
    payload: EnqueueRequest,
    _: User = Depends(get_current_user),
) -> EnqueueResponse:
    job_id = await JobService.enqueue(payload.function_name, payload.job_data)
    return EnqueueResponse(job_id=job_id)


async def get_job_status(
    job_id: str,
    _: User = Depends(get_current_user),
) -> JobStatusResponse:
    result = await JobService.get_status(job_id)
    return JobStatusResponse(**result)
