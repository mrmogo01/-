from flask import Flask, request, render_template
import vk_api
from vk_api.utils import get_random_id
import gspread
from google.oauth2.service_account import Credentials
import os

app = Flask(__name__)

# Установите необходимые области доступа
scopes = ['https://www.googleapis.com/auth/spreadsheets']

# Авторизация с использованием файла учетных данных
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Откройте таблицу по URL
sheet_api = client.open_by_url(
    'https://docs.google.com/spreadsheets/d/1bhtd05Tj3Zdeoy3TkF8W3Zkc-522CzrEmq-YWWcUqq4/edit?gid=0#gid=0')

# Выберите лист таблицы
worksheet = sheet_api.sheet1

# Авторизация в VK
vk_session = vk_api.VkApi(token='vk1.a._N29TFCYZHEUo7bpJg6vjj01NJeV9JwBZCQTDHWk-MkqPUGdR5OuIUylqGjSp3k_Ez4n8kPhGP6aCXmUZyeMq5c3M0wJ-mdmjBhhpCcfiZ9PDsdxRStbMnsY00Kcbi2IXiysBiD0B59oJUmX58JDLCgckl_msc5bCurcPsu8b6aqU7tv6XPU6lkZo1a4nWJr4PyckmPBzXmDOJ-7xnnhbA')
vk = vk_session.get_api()

@app.route('/', methods=['GET', 'POST'])
def send_message():
    chat_data = worksheet.get_all_records()  # Получаем все данные из таблицы
    chat_options = [{'id': chat['description'], 'text': chat['name']} for chat in chat_data]  # Формируем список для Select2

    if request.method == 'POST':
        message = request.form['message']
        chat_ids = request.form.getlist('chat_id')  # Получаем список выбранных ID чатов

        feedback = []
        for chat_id in chat_ids:
            if chat_id.isdigit():
                vk.messages.send(
                    chat_id=int(chat_id),
                    message=message,
                    random_id=get_random_id()
                )
                feedback.append(f"Сообщение отправлено в чат ID: {chat_id}")
            else:
                feedback.append("Некорректный ID чата: " + chat_id)

        return render_template('index.html', feedback=feedback, chat_options=chat_options)
    return render_template('index.html', feedback='', chat_options=chat_options)


if __name__ == '__main__':
    app.run(debug=True)
