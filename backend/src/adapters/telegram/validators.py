import re
from typing import Optional
from src.domain.entities.enums import VideoSource

class URLValidator:
    INSTAGRAM_PATTERN = r'https?://(www\.)?instagram\.com/(p|reel)/[\w-]+/?'
    TIKTOK_PATTERN = r'https?://(www\.)?(tiktok\.com|vm\.tiktok\.com)/[\w@./-]+'

    @staticmethod
    def validate(url: str) -> tuple[bool, Optional[VideoSource], str]:
        ig_match = re.search(URLValidator.INSTAGRAM_PATTERN, url)
        if ig_match:
            clean_url = ig_match.group(0)
            return True, VideoSource.INSTAGRAM, clean_url
        tt_match = re.search(URLValidator.TIKTOK_PATTERN, url)
        if tt_match:
            clean_url = tt_match.group(0)
            return True, VideoSource.TIKTOK, clean_url
        return False, None, url

    @staticmethod
    def extract_note(text: str, url: str) -> str:
        note = text.replace(url, "").strip()
        note = re.sub(r'\s+', ' ', note).strip()
        return note
