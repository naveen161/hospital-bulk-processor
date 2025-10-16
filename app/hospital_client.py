import httpx
from app.models import HospitalResult

BASE_URL = "https://hospital-directory.onrender.com"

async def create_hospital(hospital: dict, batch_id: str, row_num: int):
    async with httpx.AsyncClient(timeout=20.0) as client:
        data = {**hospital, "creation_batch_id": batch_id}
        try:
            resp = await client.post(f"{BASE_URL}/hospitals/", json=data)
            resp.raise_for_status()
            result = resp.json()
            return HospitalResult(
                row=row_num,
                hospital_id=result.get("id", -1),
                name=result.get("name", hospital["name"]),
                status="created_and_activated" if result.get("active") else "created"
            ).dict()
        except httpx.HTTPStatusError as e:
            return {
                "row": row_num,
                "status": "failed",
                "error": f"HTTP {e.response.status_code}: {e.response.text}"
            }
        except httpx.RequestError as e:
            return {
                "row": row_num,
                "status": "failed",
                "error": f"Request error: {str(e)}"
            }
        except Exception as e:
            return {
                "row": row_num,
                "status": "failed",
                "error": f"Unexpected error: {str(e)}"
            }

async def activate_batch(batch_id: str) -> bool:
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            resp = await client.patch(f"{BASE_URL}/hospitals/batch/{batch_id}/activate")
            return resp.status_code == 200
        except Exception:
            return False


async def get_all_hospitals():
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{BASE_URL}/hospitals/")
        if resp.status_code == 200:
            return resp.json()
        return {"error": f"Failed to fetch hospitals. Status code: {resp.status_code}"}


async def create_hospital_individual(hospital: dict):
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(f"{BASE_URL}/hospitals/", json=hospital)
        return resp.json()

async def get_hospital_by_id(hospital_id: int):
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{BASE_URL}/hospitals/{hospital_id}")
        return resp.json()

async def update_hospital(hospital_id: int, hospital: dict):
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.put(f"{BASE_URL}/hospitals/{hospital_id}", json=hospital)
        return resp.json()

async def delete_hospital(hospital_id: int):
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.delete(f"{BASE_URL}/hospitals/{hospital_id}")
        return {"status": resp.status_code, "message": "Deleted" if resp.status_code == 200 else resp.text}
    

async def get_hospitals_by_batch(batch_id: str):
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{BASE_URL}/hospitals/batch/{batch_id}")
        if resp.status_code == 200:
            return resp.json()
        return {"error": f"Failed to fetch hospitals for batch {batch_id}. Status: {resp.status_code}"}

