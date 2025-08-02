from langdetect import detect

lang_map = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "or": "Odia",
}

def detect_language(text):
    try:
        code = detect(text)
        return lang_map.get(code, code)
    except Exception:
        return "Unknown"
