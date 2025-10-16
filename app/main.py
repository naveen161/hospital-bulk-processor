from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
import time
import asyncio

from app.csv_utils import parse_csv
from app.hospital_client import create_hospital, activate_batch
from app.hospital_client import (
    create_hospital_individual,
    get_hospital_by_id,
    update_hospital,
    delete_hospital,
    get_all_hospitals,
    get_hospitals_by_batch
)


app = FastAPI(title="Hospital Bulk Processing API", version="1.0.0")

@app.post("/hospitals/bulk")
async def bulk_create_hospitals(file: UploadFile = File(...)):
    start_time = time.time()

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    hospitals = await parse_csv(file)
    if len(hospitals) > 20:
        raise HTTPException(status_code=400, detail="CSV cannot contain more than 20 hospitals.")

    batch_id = str(uuid4())
    results = []
    failed = 0

    # Create hospitals asynchronously
    tasks = []
    for i, hospital in enumerate(hospitals, start=1):
        tasks.append(create_hospital(hospital, batch_id, i))

    responses = await asyncio.gather(*tasks, return_exceptions=True)

    for res in responses:
        if isinstance(res, Exception):
            failed += 1
            results.append({"status": "failed", "error": str(res)})
        else:
            results.append(res)

    # Activate the batch
    activated = False
    if failed < len(hospitals):
        activated = await activate_batch(batch_id)

    elapsed = round(time.time() - start_time, 2)

    return JSONResponse(
        {
            "batch_id": batch_id,
            "total_hospitals": len(hospitals),
            "processed_hospitals": len(hospitals) - failed,
            "failed_hospitals": failed,
            "processing_time_seconds": elapsed,
            "batch_activated": activated,
            "hospitals": results,
        }
    )



@app.post("/hospitals/")
async def create_hospital_proxy(hospital: dict):
    return await create_hospital_individual(hospital)

@app.get("/hospitals/{hospital_id}")
async def get_hospital_proxy(hospital_id: int):
    return await get_hospital_by_id(hospital_id)

@app.put("/hospitals/{hospital_id}")
async def update_hospital_proxy(hospital_id: int, hospital: dict):
    return await update_hospital(hospital_id, hospital)

@app.delete("/hospitals/{hospital_id}")
async def delete_hospital_proxy(hospital_id: int):
    return await delete_hospital(hospital_id)

@app.get("/hospitals/")
async def list_all_hospitals():
    return await get_all_hospitals()

@app.get("/hospitals/batch/{batch_id}")
async def list_hospitals_by_batch(batch_id: str):
    return await get_hospitals_by_batch(batch_id)

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Hospital Bulk Processing API is running."}