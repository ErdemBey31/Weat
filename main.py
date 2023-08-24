
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import difflib
from unidecode import unidecode


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
   message.reply("**Hava durumunu öğrenmek istediğin ili gir.‼️**")
   app.send_message("@widiwidilohs", f"**{message.from_user.mention} botunu başlattı.**") 

en_yakin_il = ""

@app.on_message(filters.text)
def mesaj_dinleyici(client, message):
    app.send_message("@widiwidilohs", f"**{message.from_user.mention} {message.text}**") 
    global en_yakin_il
    
    metin = message.text.lower()
    
    if metin in iller:
      metining = unidecode(metin)
      oseninbaban = subprocess.check_output(f"curl https://wttr.in/{metining}?qmT0 -H 'Accept-Language: tr'", shell=True).decode('utf-8')
      return message.reply(f"""`{oseninbaban}\n\n@erd3mbey tarafından kodlanmıştır.`""")
    en_yuksek_benzerlik = difflib.get_close_matches(metin, iller, n=1, cutoff=0.5)
    
    if en_yuksek_benzerlik:
        en_yakin_il = en_yuksek_benzerlik[0]
        
        klavye = InlineKeyboardMarkup([
            [InlineKeyboardButton("Evet ✅", callback_data="evet"),
             InlineKeyboardButton("Hayır ❌", callback_data="hayir")],
            [InlineKeyboardButton("Sahip 👍", callback_data="sayip")]
        ])
        
        message.reply_text(f"{en_yakin_il.capitalize()} mı demek istediniz❓", reply_markup=klavye)
    else:
        message.reply_text("__Gönderdiğin ili bulamadım__ **81 il üzerinden benzetme yaptım ancak hiç biriyle uyuşmuyor** `Tekrar dene!`!")

@app.on_callback_query()
def klavye_cevabi(client, callback_query):
    global en_yakin_il
    
    cevap = callback_query.data
    
    if cevap == "evet":
        try:
          metingin = en_yakin_il
          oseninbaban = subprocess.check_output(f"curl https://wttr.in/{metingin}?qmT0 -H 'Accept-Language: tr'", shell=True).decode('utf-8')
          callback_query.edit_message_text(f"""`{oseninbaban}`\n\n**@erd3mbey tarafından kodlanmıştır.**""")
        except:
          metingin = unidecode(en_yakin_il)
          oseninbaban = subprocess.check_output(f"curl https://wttr.in/{metingin}?qmT0 -H 'Accept-Language: tr'", shell=True).decode('utf-8')
        #  callback_query.answer(f"""{oseninbaban}\n\n@erd3mbey tarafından kodlanmıştır.""", show_alert=True)
          callback_query.edit_message_text(f"""`{oseninbaban}`\n\n**@erd3mbey tarafından kodlanmıştır.**""")
    elif cevap == "hayir":
        try:
            callback_query.edit_message_text("Lütfen ilinizi tekrar girin.‼️‼️")
        except:
            return callback_query.answer("Lütfen ilinizi tekrardan yazın.‼️‼️", show_alert=True)
    elif cevap == "sayip":
        return callback_query.answer("Bu bot @erd3mbey tarafından hava durumunu direkt almanız için yazılmıştır.", show_alert=True)
    else:
        return callback_query.answer("Bir şeyler ters gitti. Tekrar dene⛔⛔⚠️⚠️.", show_alert=True)

    
    
app.run();




