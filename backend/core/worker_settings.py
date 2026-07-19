from arq.connections import RedisSettings

async def simple_work(ctx: dict, job_data: str):
    print("---------------------------------")
    print(f"[WORKER] กำลังประมวลผล Job...")
    print(f"[WORKER] ข้อมูลที่ได้รับ: {job_data}")
    print("---------------------------------")
    return "Success"

class WorkerSettings:
    functions = [simple_work]
    redis_settings = RedisSettings(host='localhost', port=6379)