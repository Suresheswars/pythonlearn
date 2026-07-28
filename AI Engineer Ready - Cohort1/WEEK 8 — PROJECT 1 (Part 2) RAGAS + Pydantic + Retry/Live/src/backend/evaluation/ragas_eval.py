from ragas.llms import LangchainLLMWrapper
from ragas import SingleTurnSample # user_input, response, retrieved_contexts, reference
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import LLMContextPrecisionWithoutReference,ResponseRelevancy,Faithfulness, LLMContextRecall, FactualCorrectness
import asyncio
from src.backend.logger import GLOBAL_LOGGER as log
from src.backend.rag.llm import get_llm
from src.backend.rag.embeddings import get_embeddings
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_core.prompts import PromptTemplate
from src.backend.core.config import settings

def evaluate_hallucination(query,response, retrieved_context):
    """
    Measures if the answer contains information NOT present in the context.
    Ragas uses 'Faithfulness' for this. A low Faithfulness score = High Hallucination.
    """
    try:
        log.info('Checking for Hallucinations')
        sample = SingleTurnSample(
            user_input = query,
            response=response,
            retrieved_contexts=retrieved_context, 
        )
        async def main():
            llm = get_llm()
            evaluator_llm = LangchainLLMWrapper(llm)
            # Faithfulness: Is the answer derived solely from the context?
            metric = Faithfulness(llm=evaluator_llm)
            score = await metric.single_turn_ascore(sample)
            
            # Hallucination Score can be interpreted as 1 - Faithfulness
            hallucination_score = 1 - score
            return {
                "hallucination_detected": hallucination_score > 0.1, # Threshold
                "hallucination_score": hallucination_score
            }
        
        return asyncio.run(main())
    except Exception as e:
        log.error("Error during hallucination check", error=str(e))
        return e


def evaluate_factual_correctness(query, response):
    
    try:
        log.info('Evaluating Factual Correctness')
        sample = SingleTurnSample(
            user_input=query,
            response=response,
            reference=settings.REFERENCE_ANSWER,
        )
        async def main():
            llm = get_llm()
            evaluator_llm = LangchainLLMWrapper(llm)
            # AnswerCorrectness weights semantic similarity and factual correctness
            correctness = FactualCorrectness(llm=evaluator_llm)
            result = await correctness.single_turn_ascore(sample)
            return result
        
        return asyncio.run(main())
    except Exception as e:
        log.error("Error during evaluating Factual Correctness", error=str(e))
        return e


def evaluate_context_recall(query,response,retrieved_context):
    try:
        log.info('Evaluating Contextual Recall')
        sample = SingleTurnSample(
            user_input=query,
            response=response,
            reference=settings.REFERENCE_ANSWER,
            retrieved_contexts=retrieved_context,
        )
        async def main():
            llm = get_llm()
            evaluator_llm = LangchainLLMWrapper(llm)
            recall = LLMContextRecall(llm=evaluator_llm)
            result = await recall.single_turn_ascore(sample)
            return result
        
        return asyncio.run(main())
    except Exception as e:
        log.error("Error during evaluating Contextual Recall", error=str(e))
        return e


def evaluate_faithfulness(query,response,retrieved_context):

    try:
        log.info('Evaluating Faithfulness')
        sample = SingleTurnSample(
            user_input=query,
            response=response,
            retrieved_contexts=retrieved_context, 
        )
        async def main():
            llm = get_llm()
            evaluator_llm = LangchainLLMWrapper(llm)
            faithfulness = Faithfulness(llm=evaluator_llm)
            result = await faithfulness.single_turn_ascore(sample)
            return result
        
        return asyncio.run(main())
    except Exception as e:
        log.error("Error during evaluating faithfulness", error=str(e))
        return e


def evaluate_context_precision(query,response,retrieved_context):

    try:
        log.info('Evaluating Context Precision')
        sample = SingleTurnSample(
            user_input=query,
            response=response,
            retrieved_contexts=retrieved_context, 
        )
        async def main():
            llm = get_llm()
            evaluator_llm = LangchainLLMWrapper(llm)
            context_precision = LLMContextPrecisionWithoutReference(llm=evaluator_llm)
            result = await context_precision.single_turn_ascore(sample)
            return result
        
        return asyncio.run(main())
    except Exception as e:
        log.error("Error during evaluating Context Precision", error=str(e))
        return e

def evaluate_response_relevancy(query,response,embeddings,retrieved_context):

    try:
        sample = SingleTurnSample(
            user_input=query,
            response=response,
            retrieved_contexts= retrieved_context
        )

        async def main():
            llm = get_llm()
            evaluator_llm = LangchainLLMWrapper(llm)
            embedding_model = embeddings
            evaluator_embeddings = LangchainEmbeddingsWrapper(embedding_model)
            scorer = ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings)
            result = await scorer.single_turn_ascore(sample)
            return result
        return asyncio.run(main())
    
    except Exception as e:
        log.error("Error during evaluating response relevancy", error=str(e))
        return e


def evaluate_llm_judge(query, response, retrieved_context):
    llm = get_llm()

    context_str = "\n".join([f"- {c}" for c in retrieved_context])

    prompt = PromptTemplate(
        input_variables=["query", "context_str", "response"],
        template="""
                You are an expert Evaluator. Your task is to judge the RELEVANCY of an Answer based on a User Question and the Provided Context.

                ### Evaluation Criteria:
                1. **Directness**: Does the answer directly address the user's question?
                2. **Grounding**: Is the answer supported by the retrieved context?
                3. **Completeness**: Does it provide all necessary details found in the context to answer the question?
                4. **Precision**: Does it avoid irrelevant fluff?

                ### Input Data:
                **User Question:** {query}
                **Retrieved Context:** {context_str}
                **Generated Answer:** {response}

                ### Output Format:
                You must respond ONLY in the following JSON format:
                {{
                    "relevancy_percentage": <integer between 0 and 100>,
                    "explanation": "<short 2-sentence explanation>",
                    "hallucination_detected": <true/false>
                }}
                """
                    )

    try:
        # chain = prompt | llm | StrOutputParser()
        chain = prompt | llm | JsonOutputParser()

        raw_result = chain.invoke({
            "query": query,
            "context_str": context_str,
            "response": response
        })

        return raw_result

    except Exception as e:
        log.error("Error during evaluating llm-as-a-judge", error=str(e))
        return e
    

# if __name__ == "__main__":

#     question = "what is the revenue increase in FY24?"
#     answer = "The revenue increase in FY24 is calculated by comparing the revenue figures of FY2024 and FY2023. ..- Revenue in FY2023: USD 110.0 million.- Revenue in FY2024: USD 120.0 million..To find the increase:..Revenue Increase = Revenue in FY2024 - Revenue in FY2023  .Revenue Increase = USD 120.0 million - USD 110.0 million  .Revenue Increase = USD 10.0 million..Thus, the revenue increase in FY24 is USD 10.0 million."
#     retrieved_context = ['through automation, cost optimization initiatives, and deleveraging of the balance sheet. Management focused on strengthening\ninternal controls, improving working capital efficiency, and mitigating interest rate and foreign exchange risks.\nFINANCIAL HIGHLIGHTS: Revenue increased to USD 120.0 million in FY2024 compared to USD 110.0 million in FY2023 and USD\n98.0 million in FY2022. Gross profit for FY2024 amounted to USD 42.0 million, with gross margins stabilizing despite inflationary\npressures. Net income increased to USD 15.0 million in FY2024.\nIncome Statement (USD)\nFY2022\nFY2023\nFY2024\nRevenue\n98,000,000\n110,000,000\n120,000,000\nCOGS\n62,000,000\n70,000,000\n78,000,000\nGross Profit\n36,000,000\n40,000,000\n42,000,000\nOperating Income\n17,800,000\n18,500,000\n18,500,000\nNet Income\n10,800,000']
    # print(evaluate_context_precision(question, answer, retrieved_context))
    # print(evaluate_faithfulness(question, answer, retrieved_context))
    # print(evaluate_context_recall(question,answer,retrieved_context))
    # print(evaluate_factual_correctness(question, answer))
    # print(evaluate_hallucination(question,answer, retrieved_context))
    # print(evaluate_llm_judge(question, answer, retrieved_context))