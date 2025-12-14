import os
from openai import AzureOpenAI

class AzureOpenAIClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_version="2024-12-01-preview",
        )
        self.deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.responses.create(
            model=self.deployment,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        return response.output_text

