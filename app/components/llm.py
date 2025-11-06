from app.common.logger import get_logger
from langchain_groq import ChatGroq
from app.common.custom_exception import CustomException
from app.config.config import GROQ_API_KEY,MODEL_NAME

logger = get_logger(__name__)

def load_llm(api_key: str = GROQ_API_KEY, model_name: str = MODEL_NAME):
    try:
        logger.info("Loading LLM from Groq")

        llm = ChatGroq(
            api_key=api_key, 
            model=model_name, 
            temperature=0
            )
    
        logger.info("LLM model loaded successfully")

        return llm
    
    except Exception as e:
        error_message = CustomException("Failed to load the llm model" , e)
        logger.error(str(error_message))