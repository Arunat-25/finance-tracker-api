from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from pydantic import EmailStr

from app.common.config import settings

conf = ConnectionConfig(
   MAIL_USERNAME="arunatmanikov13@gmail.com", # адрес для аутентификации на SMTP сервере
   MAIL_PASSWORD="fcgp xczh wjgf jehh", # сгенерированный двухфакторный пароль для аутентификации
   MAIL_FROM="arunatmanikov13@gmail.com", # адрес отправителя, который будет видеть получатель
   MAIL_PORT=587, # порт для SMPT сервера google
   MAIL_SERVER="smtp.gmail.com", # адрес SMTP сервера
   MAIL_SSL_TLS=False, # Не используем устаревший SSL
   MAIL_STARTTLS = True, # Современное шифрование
   USE_CREDENTIALS = True, # Обязательная авторизация на SMTP сервере
   VALIDATE_CERTS=True, # по умолчанию тоже True
   MAIL_FROM_NAME="Finance api tracker",
)


async def send_email(email: EmailStr, verification_token: str):
   message = MessageSchema(
      subject="Подтверждение email’а",  # Тема письма
      recipients=[email],
      body=f"Кликните по ссылке и подтвердите email {settings.APP_URL}/auth/confirm-email?token={verification_token}\n"
           f"(или скопируйте и вставьте в браузер)",
      subtype=MessageType.plain
   )
   fm = FastMail(conf)
   return await fm.send_message(message)



