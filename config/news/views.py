from django.shortcuts import render
import requests
# Create your views here.

dataFilter = ("AI OR artificial intelligence OR ChatGPT OR GPT-4 OR OpenAI")
#     'AI OR "artificial intelligence" OR "generative AI" OR AGI OR "artificial general intelligence" '
#     'OR ML OR "machine learning" OR "deep learning" OR "neural network" OR "transformer model" '
#     'OR LLM OR "large language model" OR "foundation model" OR "multimodal model" OR "AI agent" OR "autonomous agent" OR RAG OR "retrieval augmented generation" '
#     'OR "vector database" OR "prompt engineering" OR "guardrails" OR "fine-tuning" OR SFT OR "inference" OR "distillation" OR RLHF OR DPO OR "model alignment" OR "safety spec" OR "AI safety" OR "AI regulation" OR "model weights" OR "open-weight" OR "open source AI" '
#     'OR ChatGPT OR "GPT-4" OR "GPT-4o" OR "GPT-4.1" OR "GPT-5" '
#     'OR Claude OR "Claude 3" OR "Claude 3.5" OR "Claude 3.7" '
#     'OR Llama OR "Llama 3" OR "Llama 3.1" OR "Llama 2" '
#     'OR Gemini OR "Gemini 1.5" OR "Gemini 2.0" OR PaLM OR "PaLM 2" '
#     'OR Mistral OR "Mixtral 8x7B" OR "Mixtral 8x22B" '
#     'OR "Command R" OR "Command R+" OR Cohere '
#     'OR Qwen OR "Qwen2" OR "Qwen2.5" OR Yi OR "Yi-34B" OR DeepSeek OR "DeepSeek-V3" OR "DeepSeek-R1" '
#     'OR DBRX OR "Snowflake Arctic" OR "Arctic LLM" '
#     'OR Falcon OR MPT OR Pythia OR Phi OR "Phi-3" '
#     'OR Grok OR "Grok-2" '
#     'OR Sora OR "Stable Diffusion" OR SDXL OR "Stable Diffusion 3" OR Midjourney OR "DALL-E" OR "DALL·E" OR Imagen OR Veo OR "Dream Machine" OR "Runway Gen-3" OR Pika '
#     'OR "OpenAI" OR "Anthropic" OR "Google DeepMind" OR DeepMind OR Google OR Microsoft OR Meta OR "Mistral AI" OR xAI OR "Stability AI" OR "Hugging Face" OR Runway OR "Perplexity AI" OR "Character AI" OR ElevenLabs OR Databricks OR Snowflake OR NVIDIA OR "Adept AI" OR "Reka AI"'
# )



def get_news(request):
    api_key = "8c14b086b0d0441c9f8087ec07564101"

    url = f"https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",                   
        "category": "technology",
        "q": "AI",
        "pageSize": 50,
        "apiKey": api_key,
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        print(data)  # API'den gelen tüm JSON
        print(data.get("articles", []))  # sadece sources listesi

        return render(request, 'web/home.html', {"articles":data.get("articles", [])})
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"API isteği başarısız oldu: {e}")
    

    

    

