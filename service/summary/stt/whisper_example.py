# reference: https://github.com/openai/whisper


import whisper

# 모델은 tiny, medium, large등 선택 가능
_MODEL_SIZE = "base"
_FILE_PATH = "Enter your file path"

print("creating model...")
model = whisper.load_model(_MODEL_SIZE)

result = model.transcribe(_FILE_PATH)

print(result["text"])
