
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import difflib
import urllib.parse
import subprocess
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
@app.on_message(filters.command("start"))
def start(client, message):
  message.reply("**Hava durumunu öğrenmek istediğin ili gir.**")

en_yakin_il = ""

@app.on_message(filters.text)
def mesaj_dinleyici(client, message):
    global en_yakin_il
    
    med = message.text.lower()
    metin = urllib.parse.quote(med)
    if metin in iller:
      oseninbaban = subprocess.check_output(f"curl https://wttr.in/{metin}?qmT0 -H 'Accept-Language: tr'", shell=True).decode('utf-8')
      return message.reply(f"""`{oseninbaban}`""")
    en_yuksek_benzerlik = difflib.get_close_matches(metin, iller, n=1, cutoff=0.5)
    
    if en_yuksek_benzerlik:
        en_yakin_il = en_yuksek_benzerlik[0]
        
        klavye = InlineKeyboardMarkup([
            [InlineKeyboardButton("Evet", callback_data="evet"),
             InlineKeyboardButton("Hayır", callback_data="hayir")]
        ])
        
        message.reply_text(f"{en_yakin_il.capitalize()} mı demek istediniz?", reply_markup=klavye)
    else:
        message.reply_text("Geçersiz!")

@app.on_callback_query()
def klavye_cevabi(client, callback_query):
    global en_yakin_il
    
    cevap = callback_query.data
    
    if cevap == "evet":
        oseninbaban = subprocess.check_output(f"curl https://wttr.in/{en_yakin_il}?qmT0 -H 'Accept-Language: tr'", shell=True).decode('utf-8')
        callback_query.answer(f"""`{oseninbaban}`""", show_alert=True)
    elif cevap == "hayir":
        try:
            callback_query.edit_message_text("Lütfen ilinizi tekrar girin.")
        except:
            return callback_query.answer("Lütfen ilinizi tekrardan yazın.", show_alert=True)

    
    
app.run();




