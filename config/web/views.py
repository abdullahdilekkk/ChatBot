from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms, utils 


# Create your views here.
def home (request):
    return render (request, "web/home.html")
    

#Boş bu chat objesi oluşturduk 
def new_chat(request):
    s = models.ChatSession.objects.create()
    return redirect("chat", pk=s.pk)


def chat_view(request, pk):
    # eğer DB de pk = pk objesi varsa s e o gelri yoksa 404
    s = get_object_or_404(models.ChatSession, pk = pk)

    if request.method == "POST":    #html de Post medodu ile alıyoruz oradan buraya geliyor
        form = forms.ChatForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data["user_input"]
            if user_text:
                ai_text = utils.get_ai_response(user_text, s.messages)
                    
                models.Message.objects.create(session=s, sender="human", text=user_text)
                models.Message.objects.create(session=s, sender="ai", text=ai_text)
            if not ai_text:
                ai_text="*****Ai den yanıt alınamadı*****"
                
        return redirect("chat", pk=s.pk)
    
    form = forms.ChatForm()
    chat_history = s.messages.order_by("created")
    return render(request, "web/chat.html", {"form": form, "chat_history": chat_history, "session": s})