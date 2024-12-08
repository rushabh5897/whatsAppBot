import google.generativeai as genai
import json


def generate_llm_response(query: str) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={"response_mime_type": "application/json"},
    )

    prompt = f"""
    You are a helpful assistant specializing in product warranties, claims, and customer support.
    Respond to the following question in a clear and concise way. 
    If you don't have sufficient information to answer, state that explicitly.

    Question: {query}

    Output format: The response must be a valid JSON structure with the following fields:
    - "answer": The direct answer to the question. If uncertain, include a message indicating lack of information.
    """

    response = model.generate_content(prompt).text
    response = json.loads(response)
    return response["answer"]
