from openai import OpenAI
from config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

chat_completion = client.chat.completions.create(
    model="gpt-4o-mini", messages=[{"role": "user", "content": "Hello world"}]
)
print(chat_completion)
