from functools import lru_cache
from langchain.chat_models import init_chat_model


@lru_cache(maxsize=8)
def chat_model(model_id: str):
    return init_chat_model(model_id)


def structured_chat_model(model_id: str, schema):
    return chat_model(model_id).with_structured_output(schema)

