import os

import deepl
from fastapi import APIRouter

router = APIRouter()

API_KEY = os.environ.get("DEEPL_KEY")
translator = deepl.Translator(API_KEY)


@router.post("/toKr")
async def translate(text: str):
    return translator.translate_text(text, source_lang="EN", target_lang="KO")
