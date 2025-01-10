# from fastapi import APIRouter, HTTPException
# import openai

# # Router setup
# router = APIRouter(
#     prefix="/chatbot",
#     tags=["Chatbot"],
# )

# # Ensure to replace with your actual OpenAI API key
# openai.api_key = "your_openai_api_key"

# @router.post("/dtc-explanation")
# def explain_dtc(dtc_code: str):
#     """
#     Provide an explanation for a Diagnostic Trouble Code (DTC).
#     """
#     try:
#         # Example prompt for OpenAI GPT model
#         prompt = f"Explain the diagnostic trouble code (DTC): {dtc_code}"
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=prompt,
#             max_tokens=150
#         )
#         return {"dtc_code": dtc_code, "explanation": response.choices[0].text.strip()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
