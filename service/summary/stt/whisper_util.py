# import typing
#
# import whisper
#
# _MODEL_SIZE = "base"
#
#
# _model = whisper.load_model(_MODEL_SIZE)
#
#
# def speech_to_text(file_path: str) -> typing.Union[str, None]:
#     try:
#         result = _model.transcribe(file_path)
#         return result["text"]
#     except Exception as e:
#         print(e)
#         return None
