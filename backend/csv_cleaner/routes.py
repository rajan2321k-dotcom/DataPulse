from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from backend.csv_cleaner.cleaner import clean_csv

import os
import uuid


router = APIRouter(
    prefix="/csv",
    tags=["CSV Cleaner"]
)


UPLOAD_FOLDER = "data/csv_uploads"
OUTPUT_FOLDER = "data/csv_cleaned"


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# --------------------------------------------------
# UPLOAD + CLEAN CSV
# --------------------------------------------------

@router.post("/clean")
async def clean_uploaded_csv(
    file: UploadFile = File(...)
):

    # --------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    # --------------------------------------------------
    # UNIQUE FILE NAME
    # --------------------------------------------------

    file_id = str(uuid.uuid4())

    original_filename = file.filename

    input_filename = (
        f"{file_id}_{original_filename}"
    )

    output_filename = (
        f"cleaned_{file_id}_{original_filename}"
    )

    input_path = os.path.join(
        UPLOAD_FOLDER,
        input_filename
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    # --------------------------------------------------
    # SAVE UPLOADED FILE
    # --------------------------------------------------

    content = await file.read()

    with open(input_path, "wb") as buffer:
        buffer.write(content)

    # --------------------------------------------------
    # CLEAN CSV
    # --------------------------------------------------

    try:

        result = clean_csv(
            input_path,
            output_path
        )

    except Exception as e:

        if os.path.exists(input_path):
            os.remove(input_path)

        raise HTTPException(
            status_code=500,
            detail=f"CSV cleaning failed: {str(e)}"
        )

    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return {
        "success": True,
        "message": "CSV cleaned successfully",

        "filename": original_filename,

        "statistics": {
            "original_records":
                result["original_records"],

            "cleaned_records":
                result["cleaned_records"],

            "missing_values":
                result["missing_values"],

            "invalid_values":
                result["invalid_values"]
        },

        "download_url":
            f"/csv/download/{output_filename}"
    }


# --------------------------------------------------
# DOWNLOAD CLEANED CSV
# --------------------------------------------------

@router.get("/download/{filename}")
def download_cleaned_csv(filename: str):

    file_path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail="Cleaned file not found"
        )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )