"""
Ollama ile konuşmak için basit yardımcılar.
Gereken: pip install ollama
Not: Ollama uygulaması açık ve model indirili olmalı: `ollama pull llama3.1:8b`

BU ŞEKİLDE OLLAMA ALIR  llama yı kullanırken böyle kullnaıyoruz
            {"role": "system", "content": "-"},
            {"role": "user", "content": "-"},
            {"role": "assistant", "content": "-p"} 

"""
import os, ollama, requests 
from types import SimpleNamespace

#işletim sistemindeki environment variable’dan "OLLAMA_MODEL" isimli değişkeni okumaya çalışır.
#Eğer o değişken tanımlı değilse, "llama3.1:8b" varsayılan değer olarak kullanılır.

if os.getenv("USE_CLOUD_API", "0") == "1":  # 0 olduğunda lokal ollama çalışır 1 ise bluta geçer

    def _cloud_chat(model, messages):
        r = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY','')}",
                "Content-Type": "application/json"
                },
            json={"model": "openai/gpt-oss-20b",
                  "messages": messages,
                  "temperature": 0.6,   #0 → deterministik, 1 → daha yaratıcı
                  "max_tokens": 512},   #Cevabın üst token sınırı.
            timeout=60
        )
        return {"message": {"content": r.json()["choices"][0]["message"]["content"]}}
    
                # GELEN OPENAI APİLERİ ŞU ŞEKİLDE GELİR 
                # {
                # "choices": [
                #     {
                #     "index": 0,
                #     "message": { "role": "assistant", "content": "Merhaba!" },
                #     "finish_reason": "stop"
                #     }
                #     // ... (isteyerek birden fazla üretirsen başka choice'lar da gelebilir)
                # ]
                # }

MODEL_NAME = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")


def get_ai_response(user_text, history_queryset) -> str :

    history = history_queryset.order_by("created")  #sıralı olarak tarihi listele 


    messages = [
        {"role": "system", "content": "Sen her zaman Türkçe konuş, mantıklı cevaplar ver ve sohbet eder gibi konuş."},
    ]

    for m in history:
        if m.sender.lower() == "human":
            messages.append({"role":"user", "content":m.text})
        
        elif m.sender.lower() == "ai":
            messages.append({"role":"assistant", "content":m.text})
    
    #en son mesajı verelim     
    messages.append({"role": "user", "content": user_text})
    response = _cloud_chat(model=MODEL_NAME, messages=messages)

    return response["message"]["content"]





