from typing import Union

import litellm
import litellm.experimental_mcp_client
from litellm import Message, acompletion, completion
from litellm.utils import CustomStreamWrapper, ModelResponse
from openai.types.chat.chat_completion_message_param import (
    ChatCompletionMessageParam,
)  # noqa


class Agent:
    def __init__(
        self,
        name: str,
        model: str,
        instruct: str,
        api_key: str,
        reasoning_effort: str = None,
        stream: bool = False,
        base_url: str = None,
    ):
        litellm.drop_params = True
        self.name = name
        self.model = model
        self.instruct = instruct
        self.base_url = base_url
        self.api_key = api_key
        self.reasoning_effort = reasoning_effort
        self.stream = stream

    async def arun(
        self, messages: list[ChatCompletionMessageParam]
    ) -> Union[ModelResponse, CustomStreamWrapper]:  # noqa
        return await acompletion(
            model=self.model,
            base_url=self.base_url,
            stream=self.stream,
            api_key=self.api_key,
            reasoning_effort=self.reasoning_effort,
            messages=[
                Message(role="system", content=self.instruct),
                *messages,
            ],  # noqa
        )

    def run(
        self, messages: list[ChatCompletionMessageParam]
    ) -> Union[ModelResponse, CustomStreamWrapper]:  # noqa
        return completion(
            model=self.model,
            base_url=self.base_url,
            stream=self.stream,
            api_key=self.api_key,
            reasoning_effort=self.reasoning_effort,
            messages=[
                Message(role="system", content=self.instruct),
                *messages,
            ],
        )

    async def mcp_tools():
        return await litellm.experimental_mcp_client.load_mcp_tools()
