
from aiogram import types
from aiogram.filters import Command
from sqlmodel import Session, select

from src.keyboards.page_change import build_pages_keyboard
from src.models.chat import Chat
from src.page_builder import build_pages
from src.routers import main_router
from src.constants import engine
from src.routing.main.page_change_action import get_holiday_message
        

@main_router.message(Command('holidays'))
async def process_holidays(message: types.Message) -> None:

    with Session(engine) as session:
        chat = session.exec(select(Chat).where(
            Chat.id == message.chat.id)).one()
        chat.uses += 1
        session.add(chat)
        session.commit()

    pages = await build_pages(chat_id=message.chat.id)
    message_text = get_holiday_message(page_index=0, pages=pages)
    keyboard = build_pages_keyboard(current_page_index=0, max_page_index=len(pages))

    await message.answer(text=message_text, reply_markup=keyboard)
