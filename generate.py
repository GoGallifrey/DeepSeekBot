from openai import AsyncOpenAI
from config import AI_TOKEN

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_TOKEN,
)

async def AI_GEN(text: str):
    try:
        completion = await client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {
                    "role": "user",
                    "content": text  # Используем переданный текст
                }
            ]
        )
        # Выводим только текст ответа
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None