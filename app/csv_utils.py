import csv
from io import StringIO
from fastapi import UploadFile, HTTPException

async def parse_csv(file: UploadFile):
    contents = await file.read()
    text = contents.decode("utf-8")
    reader = csv.DictReader(StringIO(text))

    expected_fields = {"name", "address", "phone"}
    if not expected_fields.issuperset(reader.fieldnames):
        raise HTTPException(status_code=400, detail=f"Invalid CSV headers. Expected: {expected_fields}")

    hospitals = []
    for row in reader:
        if not row["name"] or not row["address"]:
            raise HTTPException(status_code=400, detail=f"Missing required fields in row: {row}")
        hospitals.append({
            "name": row["name"].strip(),
            "address": row["address"].strip(),
            "phone": row.get("phone", "").strip() or None
        })

    return hospitals
