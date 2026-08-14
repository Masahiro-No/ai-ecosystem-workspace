from arq import create_pool
from arq.connections import RedisSettings
from arq.jobs import Job

from core.config import settings


class JobService:
    @staticmethod
    async def get_pool():
        return await create_pool(RedisSettings(
            host=settings.redis_host,
            port=settings.redis_port,
        ))

    @staticmethod
    async def enqueue(function_name: str, job_data: str) -> str:
        pool = await JobService.get_pool()
        job = await pool.enqueue_job(function_name, job_data)
        await pool.close()
        return job.job_id

    @staticmethod
    async def get_status(job_id: str) -> dict:
        pool = await JobService.get_pool()
        job = Job(job_id, pool)
        status = await job.status()
        info = await job.result_info()
        await pool.close()
        return {
            "job_id": job_id,
            "status": status.value,
            "result": str(info.result) if info else None,
        }
