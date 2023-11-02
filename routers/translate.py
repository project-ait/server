import os

import deepl
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

API_KEY = os.environ.get("DEEPL_KEY")
translator = deepl.Translator(API_KEY)


class TranslatedModel(BaseModel):
    text: str


@router.post("/toKr")
async def translate(data: TranslatedModel):
    return translator.translate_text(data.text, source_lang="EN", target_lang="KO")


@router.post("/toEn")
async def translate(data: TranslatedModel):
    return translator.translate_text(data.text, source_lang="KO", target_lang="EN-US")
