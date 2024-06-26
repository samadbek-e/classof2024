import asyncio
import logging
import sys
from hashlib import sha256

from aiogram import Bot, Dispatcher, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram.exceptions import TelegramBadRequest
from aiogram.handlers.callback_query import CallbackQueryHandler


from firebase_helpers import addWishes, isUserExist, setupStudentAccount
from keyboards import alumnisIDSelectorButtons
from data import elevenA, elevenB, elevenD
#Components

TOKEN = "7187072054:AAESdIeKZlaPPOuzJRWIkYe-QSsqs_pw7aA"

# All handlers should be attached to the Router
main_router = Router()

# State
class BotState(StatesGroup):
    chooseAlumni = State()
    wish = State()



@main_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    h = sha256()
    user = message.from_user.id
    h.update(f"{user}".encode('utf-8'))

    hexcoded = h.hexdigest()
    if not isUserExist(hexcoded):
        setupStudentAccount(hexcoded)
        await wish(message, state)
    else:
        await wish(message, state)
    await message.answer()




@main_router.message(Command("wish"))
async def wish(message: Message, state: FSMContext) -> None:

    userID = message.from_user.id

    await message.answer(elevenA)
    await message.answer(elevenB)
    await message.answer(elevenD)

    await message.answer("Pastdan bitiruvchi raqamini bosing 👇 yoki raqamni yozib jo'nating", reply_markup=alumnisIDSelectorButtons())
    await state.set_state(BotState.chooseAlumni)

    

@main_router.message(BotState.chooseAlumni)
async def goFetch(message: Message, state: FSMContext) -> None:

    await message.answer("Xabaringizni yuboring 💬")
    await state.update_data(chooseAlumni=message.text)
    await state.set_state(BotState.wish)

@main_router.message(BotState.wish)
async def goFetch(message: Message, state: FSMContext) -> None:
   h = sha256()
   wish = message.text
   h.update(f"{message.from_user.id}".encode("utf-8"))
   student_id = h.hexdigest()
   data = await state.get_data()
   alumniID = data.get("chooseAlumni", "<Something unexpected>")
   addWishes(alumniID, student_id, wish)

   await message.answer("Xabaringiz yuborildi✅.\nYana xabar yo'llash kerak bo'lgan odamlar bo'lsa /wish bosing")

   await state.clear()

# @main_router.message()
# # help command

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)

    await dp.start_polling(bot)

    while True:
        await asyncio.sleep(1000)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())