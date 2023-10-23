import datetime

from sqlmodel import Session, select
from aiogram.exceptions import TelegramForbiddenError

from src.constants import engine, bot
from src.keyboards.page_change import build_pages_keyboard
from src.models.chat import Chat
from src.utility.page_builder import build_pages
from src.utility.print_timestamp_builder import print_with_timestamp
from src.routing.main.page_change_action import get_holiday_message


async def send_scheluded_holidays_message():
    hour = datetime.datetime.now().hour
    success = 0
    with Session(engine) as session:
        chats = session.exec(select(Chat).where(Chat.mailing_time == hour).where(Chat.mailing_enabled).where(Chat.banned == False)).all()
        for chat in chats:
            pages = await build_pages(chat_id=chat.id)
            message_text = get_holiday_message(page_index=0, pages=pages)
            keyboard = build_pages_keyboard(current_page_index=0, max_page_index=len(pages))
            
            try:
                await bot.send_message(chat_id=chat.id, text=message_text, reply_markup=keyboard)
            except TelegramForbiddenError:
                chat.banned = True
                print_with_timestamp(f'Chat {chat.id} is banned')
                
            if not chat.banned:
                success += 1
                chat.uses += 1
            session.add(chat)
            
        if len(chats) != 0:
            print_with_timestamp(f'At hour {hour}: {success} / {len(chats)} scheduled messages was send.')
        session.commit()
