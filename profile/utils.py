from core.globals import LANGUAGE_KEY, OCCUPATION_KEY, STATUS_KEY
from core.utils import get_status_or_occupation_title_by_language
from profile.messages import PROFILE_MESSAGE, PROFILE_STATUS_TEMPLATE, PROFILE_OCCUPATION_TEMPLATE


def get_profile_message(language: str, status: dict, occupation: dict) -> str:
    status = get_status_or_occupation_title_by_language(status, language)
    occupation = get_status_or_occupation_title_by_language(occupation, language)

    return (f"{PROFILE_MESSAGE[language]}\n\n"
            f"{PROFILE_STATUS_TEMPLATE[language]}{status}\n"
            f"{PROFILE_OCCUPATION_TEMPLATE[language]}{occupation}")
