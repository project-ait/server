from fastapi import APIRouter, HTTPException

from service.deepl import translate, LangCode

router = APIRouter()


@router.post("/")
async def root_translate(
        content: str,
        source: LangCode | str | None,
        target: LangCode | str | None
):
    res = translate(content, source, target)

    if res is None:
        raise HTTPException(status_code=500, detail="Translation failed")

    return res
