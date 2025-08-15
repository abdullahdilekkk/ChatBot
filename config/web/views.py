from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms, utils 
from django.contrib.auth.decorators import login_required
from . import models
# Create your views here.

#BURASI HOME U GÖSTERMEK İÇİN KULLANILIYOR İSTERSEK KULLANICI 
#GİRİŞ YAPMAMIŞSA LOGİN PAGE YE YAPMIŞSSA HOME A DA GÖNDEREBİLİRDİK 
def home (request):
    return render (request, "web/home.html")
    



def _sessions_for(request):
    # Kullanıcının sohbetleri, son mesaja göre sıralı (yoksa oluşturulma tarihine göre)
    if not request.user.is_authenticated:
        #kULLANICI GİRİŞ YAPMADIYSA OBJEYİ NON İŞARETLER
        return models.ChatSession.objects.none()
    #KULLANICI GİRİŞ YAPTIYSA REQUEST DEN USER I ÇEKER VE ONU TARİHE GÖRE SIRALAR
    return models.ChatSession.objects.filter(user=request.user).order_by("-created")




#GİRİŞ YAPMIŞSA BU METOD ÇALIŞIR SADECE 
@login_required
def new_chat(request):
    #USER I ALIP ONA ÖZELBİR NESNE OLUŞTURDUK HER KULLANICININ AYRI CHATİ OLSUN DİYE 
    s = models.ChatSession.objects.create(user = request.user)
    #MODELDEN OTOMATİK OLUŞTURULUP GELEN PK İLE O OBJENİN ANAHTARINI ALMIŞ OLDUK BÖYLECE HER CHAT OBJESİNE 
    #BENZERSİZ, KENDİNE ÖZEL CHAT E SAYİP OLUCAK VE KAYITLARI TUTABİLİCEK ESKİ KONUŞMALARI O PK YA EŞLEMİŞ OLUCAZ 
    #Oluşturduğun nesnenin pk’sini ancak create() işleminden sonra öğreniyorsun BU YÜZDEN PARAMETRE OLARAK ALMIYORUZ DA İÇERDE OLUŞUYOR
    return redirect("chat", pk=s.pk)





@login_required
def chat_view(request, pk):
    # USERA ÖZEL CHAT SAYFASI OLMASI GEREKTİĞİ İÇİN PK YI ALDIK
    s = get_object_or_404(models.ChatSession, pk = pk, user=request.user)
    #SON USERIN CHATİNE ULAŞMAK İÇİN İÇERDE OBJEYİ AÇARKEN KONTROL EDİLİR

    if request.method == "POST":
        #REQUESTİN METHODUN POST MU GET Mİ DİYE BAKMAK GEREKİR GETSE BU İŞLEMLER YAPILMAMALI BOŞ GELİR ÇÜNKÜ    
        form = forms.ChatForm(request.POST)
        #REQUESTTEN GELEN BİLGİLERİ BİR FORM A DOLDURMAMIZ ZORUNLU DEĞİL AMA USER_İNPUTUN FAYDALARINI 
        #KULLANMAK İÇİN KULLANIRIZ BUNU (TEMİZLİK VB.)
        #ŞU ŞEKİLLERDE YAPILABİLİR :

        #1)KENDİN FORM DOSYANI AÇIP FORM SINIFI YAZARAK BU KODDA OLDUĞU GİBİ
            # from django import forms
            # class ChatForm(forms.Form):
            #     user_input = forms.CharField(widget=forms.Textarea)

        #2)VİEW İÇİNDE BİR FORM TANIMLAYARAK 
            #***YUKARIDAKİ KODUN AYNISINI VİEW DA YAPARAK***

        #3)DİREKT USER_İNPUT TAN GEÇEREK 
            #if request.method == "POST":
               # user_input = request.POST.get("user_input")

        if form.is_valid():
            user_text = form.cleaned_data["user_input"]
            #YUKARIDA DA DEDİĞİM GİBİ BİZ ZATEN HER TÜRLÜ USER_İNPUTTAN ALIYORUZ SADECE FORM MODELİ İLE DAHA DÜZGÜN OLMASINI SAĞLIYORUZ
                #FORMDA USER_İNPUTU BİZ YAZDIK FAKAT DİREKT GET İLE ÇEKSEK DE O ADLA ÇEKİLİR YANİ TUTARLI İSMLER KULLANILMALI
            #FORM İÇİNDE GELEN DEFAULT BİRÇOK METHODDAN BİRİ OLAN CLEANED_DATA POSTU TEMİZ ŞEKİLDE VERİYOR 
            if user_text:
                #BOŞ İSE GEREKSİZ Aİ YE İSTEK ATILMASIN DİYE BU KONTROL VAR
                ai_text = utils.get_ai_response(user_text, s.messages)
                #AI İLE KONUŞAN YARDIMCI METODUM OLAN GET_Aİ_... YA VERİYORUZ S.MESSAGE GEÇMİŞ MESAJLARI VERMEEMİZİN NEDENİ
                #EĞER GEÇMİŞİ VERMEZSEK Aİ HER MESAYI SIFIRDANMIŞ GİBİ DÜŞÜNÜR   
                models.Message.objects.create(session=s, sender="human", text=user_text)
                models.Message.objects.create(session=s, sender="ai", text=ai_text)
                #YENİ MESSAGE KAYDI OLUŞTURUYORUZ Kİ SONRADAN BUNLARIN S.MESSAGENSİNİ KULLANABİLİRİZ
            if not ai_text:
                ai_text="*****Ai den yanıt alınamadı*****"

            if not s.title:
                s.title = user_text[:24]
                #BURADA AMAÇ TİTLE BOŞ DA OLABİLİR BOŞSA GİRMEZ İF DEN AMA BOŞSA 
                #USER_TEXTİN İL 12 İNDİSİNDEKİLER TİTLE A VERİLİR (O ANKİ SOHBET NESNESİNİN)
                s.save(update_fields=["title"])
                #SAVE() NORMALDE TÜM YAKITLARI DB YE YAZAR AMA İÇİNDE 
                #update_fields YAZINCA BELİRLİ KAYITI YAZAR SADECE 

        return redirect("chat", pk=s.pk)
        #SAYFAYI HER YENİ MESAJDAN SONRA YENİLEMEMİZ GEREK Kİ HATA VERMESİN PK DA HANGİ SOHBETİ GETİRECEĞİNİ BİLMEK İÇİN
    

    #OTOMATİK GET YAPILDIĞI İÇİN YENİLENİYOR SAYFA HEP VE MESAJLAR ESKİ MESAJLAR ÖYLE SIRALANIYOR 
    # HEM SOLDA HEM DE SAĞDAKİ MESAJLAR 
    form = forms.ChatForm()
    #GET İSTEĞİ GELDİĞİ İÇİN BOŞ FORM ALIR
    chat_history = s.messages.order_by("created")
    
    sessions = _sessions_for(request) 
    return render(request, "web/chat.html", {"form": form, "chat_history": chat_history, "session": s, "sessions": sessions})
# session şu anki mesaj objesi sessions ise tüm mesajların listesi
#sessions = Giriş yapan kullanıcının tüm sohbet oturumlarını (ChatSession) döner
#chat_history = Sadece tek bir sohbet içindeki mesajları tutar