from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from nodes.vision import analyse_image
from nodes.violations import match_violations
from nodes.supabase_store import store_report
from nodes.summarizer import summarize


def build_chain(reporter_phone: str = None, reported_image: str = None):
    def analyse_with_context(image_url: str):
        result = analyse_image(image_url)
        return {
            "analysis": result,
            "reporter_phone": reporter_phone,
            "reported_image": reported_image or image_url
        }
    
    def add_violations(data: dict):
        violations = match_violations(data["analysis"])
        return {
            **data,
            "violations": violations
        }
    
    return (
        RunnableLambda(analyse_with_context)
        | RunnableLambda(add_violations)
        | RunnableLambda(store_report)
        | RunnableLambda(summarize)
    )


chain = build_chain()
