from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from nodes.vision import analyse_image
from nodes.violations import match_violations
from nodes.summarizer import summarize

chain = (
    RunnableLambda(analyse_image)
    | RunnableParallel(analysis=RunnablePassthrough(), violations=RunnableLambda(match_violations))
    | RunnableLambda(summarize)
)

# res = chain.invoke("https://images.hindustantimes.com/auto/img/2025/03/18/1600x900/Delhi_Traffic_Violation_1713763214287_1742269490008.jpg")

# print(res)