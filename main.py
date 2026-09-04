import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# تۆکنی بۆتەکەت
TOKEN = '8516962952:AAEJb9r_IIJ0KYMpYH58usIm_mb2jjC_k6E'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "بۆتێک بۆ دەرهێنانی کۆدی سایتەکان ♻️\n\n"
        "ته‌نها لینکی وێبسایتم بۆ بنێره 🍂\n\n"
        "منیش کۆدیت بۆ دە نێرمەوە 🗿"
    )
    await update.message.reply_text(welcome_text)

async def fetch_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    # چێککردنی دروستیی لینکەکە
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    status_msg = await update.message.reply_text("چاودێڕوان بە کۆدی سایەتەکەت بۆ دە نێرم... 🌐")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        filename = "index.html"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
            
        with open(filename, 'rb') as file:
            await update.message.reply_document(
                document=file,
                filename="index.html",
                caption=f"لینکی سایت {url}\n\nHTML CSS JS کۆدی"
            )
            
        await status_msg.delete()
        
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        await update.message.reply_text("کێشەیەک ڕوویدا! دڵنیابەوە لە دروستیی لینکەکە یان ڕەنگە سایتی داواکراو ڕێگە بە دەرهێنانی کۆد نەدات.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_code))
    
    print("بۆتەکە چالاک بوو...")
    app.run_polling()
