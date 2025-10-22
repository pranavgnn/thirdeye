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
