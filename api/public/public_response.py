from fastapi import HTTPException


def not_found_exception(message: str):
    raise HTTPException(status_code=404, detail=str)


def bad_request_exception(message: str):
    raise HTTPException(status_code=400, detail=str)
