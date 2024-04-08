ENV_LOGIN_KEY = "API_LOGIN"
ENV_PASSWORD_KEY = "API_PASSWORD"
ENV_API_URL_KEY = "API_URL"
ENV_TG_TOKEN_KEY = "TG_TOKEN"
ENV_LANGUAGE_MODE_KEY = "LANGUAGE_MODE"
ENV_GENERATOR_MODE_KEY = "GENERATOR_MODE"
ENV_DEBUG_KEY = "DEBUG"
ENV_REDIS_HOST_KEY = "REDIS_HOST"
ENV_REDIS_PORT_KEY = "REDIS_PORT"

EMAIL_KEY = "email"
PASSWORD_KEY = "password"
BOT_ID_KEY = "botId"
USER_ID_KEY = "userId"
TELEGRAM_ID_KEY = "telegramId"
ADDITIONAL_KEY = "additional"
REFRESH_TOKEN_KEY = "refreshToken"
ACCESS_TOKEN_KEY = "accessToken"
OCCUPATION_TITLE_KEY = "occupationTitle"
STATUS_TITLE_KEY = "statusTitle"
STATUS_KEY = "status"
STATUS_ID_KEY = "statusId"
OCCUPATION_KEY = "occupation"
OCCUPATION_ID_KEY = "occupationId"
ID_KEY = "id"
CODE_KEY = "code"
IS_FINISHED_KEY = "isFinished"
LANGUAGE_KEY = "language"
TITLE_RU_KEY = "titleRu"
TITLE_EN_KEY = "titleEn"
TEMPLATE_OVERLAY_KEY = "overlaying"
OCCUPATION_LIST_KEY = "occupationList"
STATUS_LIST_KEY = "statusList"
TEMPLATE_LIST_KEY = "templateList"
TEMPLATE_ID_KEY = "templateId"
TEMPLATE_KEY = "template"
TEMPLATES_SWITCHER_KEY = "templates"
TYPE_KEY = "type"
USER_OVERLAY_CHOICE_KEY = "templateOverlay"
FILE_PATH_KEY = "filePath"
FILE_KEY = "file"

URL_LOGIN_VALUE = "/auth/login"
URL_ACCESS_TOKEN_VALUE = "/auth/login/access-token"
URL_BOT_USER_VALUE = "/bot-user"
URL_STATUSES_BY_BOT_VALUE = "/status/by-bot/{}"
URL_OCCUPATIONS_BY_BOT_VALUE = "/occupation/by-status/{}"
URL_STATIC_TEMPLATE_BY_BOT_VALUE = "/template/by-bot/static/{}"
URL_ANIMATED_TEMPLATE_BY_BOT_VALUE = "/template/by-bot/animated/{}"
URL_TEMPLATE_BY_ID_VALUE = "/template/{}"
URL_REQUEST_VALUE = "/request"

ERROR_NOT_AUTH_KEY_TEXT = "Not authenticated"

LANGUAGE_MULTY_KEY = "MULTY"
LANGUAGE_RU_KEY = "RU"
LANGUAGE_EN_KEY = "EN"

LANGUAGE_RU_LOCAL_VALUE = "Русский"
LANGUAGE_EN_LOCAL_VALUE = "Английский"

GENERATOR_STATIC_KEY = "STATIC"
GENERATOR_ANIMATION_KEY = "ANIMATION"
GENERATOR_ANIMATED_KEY = "ANIMATED"
GENERATOR_MIX_KEY = "MIX"

GENERATOR_OVERLAY_ABOVE_KEY = "ABOVE"
GENERATOR_OVERLAY_INSIDE_KEY = "INSIDE"

COMMAND_START_VALUE = 'start'
COMMAND_HELP_VALUE = 'help'

LANGUAGE_IN_RUSSIAN = {
    LANGUAGE_RU_LOCAL_VALUE: LANGUAGE_RU_KEY,
    LANGUAGE_EN_LOCAL_VALUE: LANGUAGE_EN_KEY,
}

EXECUTION_TIME_RECORDS = [3]

USERS_TMP: dict[str, dict] = {}
