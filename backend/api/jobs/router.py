from fastapi import APIRouter, status

from api.jobs.controller import enqueue_job, get_job_status
from api.jobs.schema import EnqueueResponse, JobStatusResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])
router.add_api_route("/", enqueue_job, methods=["POST"], response_model=EnqueueResponse, status_code=status.HTTP_201_CREATED)
router.add_api_route("/{job_id}", get_job_status, methods=["GET"], response_model=JobStatusResponse, status_code=status.HTTP_200_OK)
