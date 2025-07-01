import os
import json
import telebot
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        BOT_TOKEN = os.getenv("BOT_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")

        if not BOT_TOKEN or not CHAT_ID:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Server configuration error"}).encode())
            return

        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = json.loads(post_data)

            name = form_data.get("name")
            contact = form_data.get("contact_method")
            message = form_data.get("message", "Клиент не оставил сообщения.")

            text_message = (
                f"🔔 Новая запись на консультацию с сайта!\n\n"
                f"👤 **Имя:** {name}\n"
                f"📞 **Контакт:** {contact}\n\n"
                f"📝 **Сообщение:**\n{message}"
            )

            bot = telebot.TeleBot(BOT_TOKEN)
            bot.send_message(CHAT_ID, text_message, parse_mode="Markdown")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Заявка успешно отправлена!"}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
        return