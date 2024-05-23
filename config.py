MAX_USERS = 10
MAX_GPT_TOKENS = 120
MAX_USER_GPT_TOKENS = 4000

DB_FILE = 'TravelBot.db'
LOGS = 'logs.txt'
IAM_TOKEN_PATH = 'creds/iam.txt'


SYSTEM_PROMPT1 = [{'role': 'system', 'text': f'Расскажи о достопримечательностях города под названием '}]
TOKENIZE_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
GPT_MODEL = 'yandexgpt-lite'
GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"