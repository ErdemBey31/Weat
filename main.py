
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import difflib
from weather import Weather, Unit

# Türkiye'nin 81 ili
iller = [
    "adana", "adıyaman", "afyonkarahisar", "ağrı", "amasya", "ankara", "antalya", "artvin", "aydın", "balıkesir",
    "bilecik", "bingöl", "bitlis", "bolu", "burdur", "bursa", "çanakkale", "çankırı", "çorum", "denizli", "diyarbakır",
    "edirne", "elazığ", "erzincan", "erzurum", "eskişehir", "gaziantep", "giresun", "gümüşhane", "hakkari", "hatay",
    "ısparta", "mersin", "istanbul", "izmir", "kars", "kastamonu", "kayseri", "kırklareli", "kırşehir", "kocaeli",
    "konya", "kütahya", "malatya", "manisa", "kahramanmaraş", "mardin", "muğla", "muş", "nevşehir", "niğde", "ordu",
    "rize", "sakarya", "samsun", "siirt", "sinop", "sivas", "tekirdağ", "tokat", "trabzon", "tunceli", "şanlıurfa",
    "uşak", "van", "yozgat", "zonguldak", "aksaray", "bayburt", "karaman", "kırıkkale", "batman", "şırnak", "bartın",
    "ardahan", "ığdır", "yalova", "karabük", "kilis", "osmaniye", "düzce"
]


api_id = "22414322"
api_hash = "d4ae0d06f838826fbcf1fa2dbe6b8f91"
bot_token = "6633926828:AAFZWjM0GaDfqCopl_SeX2KHd6sDQs4DKfA"

app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@app.on_message(filters.text)
def mesaj_dinleyici(client, message):
    
    metin = message.text.lower()
    
    en_yuksek_benzerlik = difflib.get_close_matches(metin, iller, n=1, cutoff=0.5)
    
    if en_yuksek_benzerlik:
        en_yakin_il = en_yuksek_benzerlik[0]
        

        klavye = InlineKeyboardMarkup([
            [InlineKeyboardButton("Evet", callback_data="evet"),
             InlineKeyboardButton("Hayır", callback_data="hayir")]
        ])
        
        
        message.reply_text(f"{en_yakin_il.capitalize()} mı demek istediniz?", reply_markup=klavye)
    else:

        message.reply_text("Sonuçlar bekleniyor!!.")


@app.on_callback_query()
def klavye_cevabi(client, callback_query):
    
    cevap = callback_query.data
    
    if cevap == "evet":
        istenenil = en_yakin_il.capitalize()   
        callback_query.answer("API isteği gönderilir ve hava durumu bilgisi alınır.")
    elif cevap == "hayir":
        return callback_query.answer("Lütfen ilinizi tekrardan yazın.")
        
    weather = Weather(unit=Unit.CELSIUS)

# Konumu belirtin
    konum = weather.lookup_by_location('Ankara')

# Bugünkü hava durumu bilgilerini alın
    bugun = konum.forecast[0]
    bugun_tarih = bugun.date
    bugun_durum = bugun.text
    bugun_maks_sicaklik = bugun.high
    bugun_min_sicaklik = bugun.low

# Yarınki hava durumu bilgilerini alın
    yarin = konum.forecast[1]
    yarin_tarih = yarin.date
    yarin_durum = yarin.text
    yarin_maks_sicaklik = yarin.high
    yarin_min_sicaklik = yarin.low

# Sonuçları yazdırın
    callback_query.answer(f"""
    Bugün: {bugun_tarih}
    Durum: {bugun_durum}
    Maksimum Sıcaklık: {bugun_maks_sicaklik}
    Minimum Sıcaklık: {bugun_min_sicaklik}
    
    ----------------
    
    Yarın: {yarin_tarih}
    Durum: {yarin_durum}
    Maks Sıcaklık: {yarin_maks_sicaklik}
    Minimum sıcaklık: {yarin_min_sicaklik}""")

    
app.run();




