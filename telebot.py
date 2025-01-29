import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
import sqlite3

API_TOKEN = '7708888353:AAEkycjJE8GuOQ_rsfmsp5LBWEZeuRCyfHsN'

# Initialize bot, dispatcher, and router
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)
# User indices for cycling through profiles
user_indices = {}


# SQLite Database
db_file = "matchmaking.db"


# Update the `users` table to store usernames
def init_db():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                name TEXT,
                bio TEXT,
                photo_id TEXT,
                gender TEXT,
                looking_for TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS likes (
                liker_id INTEGER,
                liked_id INTEGER,
                notified BOOLEAN DEFAULT 0,
                UNIQUE(liker_id, liked_id)
            )
        """)
        conn.commit()


init_db()


# FSM States
class RegisterProfile(StatesGroup):
    name = State()
    bio = State()
    photo = State()
    gender = State()
    looking_for = State()


# Keyboards
# Correct ReplyKeyboardMarkup creation
menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Смотреть анкеты")],  # Each row is a list of buttons
        [KeyboardButton(text="Заполнить анкету заново")]
    ],
    resize_keyboard=True
)


# Command: /start
@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Напиши /register для регистрации и начала знакомств.", reply_markup=menu_kb)


# Command: /register
@router.message(Command("register"))
async def register_command(message: Message, state: FSMContext):
    if not message.from_user.username:
        await message.answer(
            "You need a Telegram username to register! Please set a username in your Telegram settings and try again."
        )
        return
    await message.answer("Как тебя называть?")
    await state.set_state(RegisterProfile.name)

@router.message(RegisterProfile.name)
async def get_name(message: Message, state: FSMContext):
    if message.text == "Смотреть анкеты" or message.text == "Заполнить анкету заново":
        await message.answer("Как тебя называть?")
        await state.set_state(RegisterProfile.name)
    await state.update_data(name=message.text)
    await message.answer("Напиши немного о себе. Желательно укажи корпус")
    await state.set_state(RegisterProfile.bio)

@router.message(RegisterProfile.bio)
async def get_bio(message: Message, state: FSMContext):
    if message.text == "Смотреть анкеты" or message.text == "Заполнить анкету заново":
        await message.answer("Напиши немного о себе. Желательно укажи корпус")
        await state.set_state(RegisterProfile.bio)
    await state.update_data(bio=message.text)
    await message.answer("Какое фото поставить на анкету?")
    await state.set_state(RegisterProfile.photo)

@router.message(RegisterProfile.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    if photo_id == "" or photo_id is None:
        await message.answer("Какое фото поставить на анкету?")
        await state.set_state(RegisterProfile.photo)
    await state.update_data(photo_id=photo_id)
    await message.answer("Твой пол: Male, Female?")
    await state.set_state(RegisterProfile.gender)

@router.message(RegisterProfile.gender)
async def get_gender(message: Message, state: FSMContext):
    if message.text != "Male" and message.text != "Female":
        await message.answer("Твой пол: Male, Female")
        await state.set_state(RegisterProfile.gender)
    else:
        await state.update_data(gender=message.text)
        await message.answer("Кого ищешь: Male, Female, Any")
        await state.set_state(RegisterProfile.looking_for)

@router.message(RegisterProfile.looking_for)
async def get_looking_for(message: Message, state: FSMContext):
    if message.text != "Male" and message.text != "Female" and message.text != "Any":
        await message.answer("Кого ищешь: Male, Female, Any")
        await state.set_state(RegisterProfile.looking_for)
    else:
        await state.update_data(looking_for=message.text)
        data = await state.get_data()
        name = data.get("name")
        bio = data.get("bio")
        photo_id = data.get("photo_id")
        gender = data.get("gender")
        looking_for = data.get("looking_for")
        username = message.from_user.username or "No username"

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO users (user_id, username, name, bio, photo_id, gender, looking_for)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (message.from_user.id, username, name, bio, photo_id, gender, looking_for))
            conn.commit()

        await state.clear()
        await message.answer("Можешь начинать знакомится, нажми кнопку внизу!", reply_markup=menu_kb)


# Viewing Profiles
@router.message(F.text == "Смотреть анкеты")
async def view_profiles(message: Message):
    user_id = message.from_user.id

    # Initialize the user's profile index if not set
    if user_id not in user_indices:
        user_indices[user_id] = 0

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        # Fetch the user's gender preferences
        cursor.execute("SELECT gender, looking_for FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        if not user_data:
            await message.answer("Сначала нужно зарегестрироваться: /register.")
            return

        user_gender, looking_for = user_data

        # Fetch profiles based on gender preferences
        if looking_for.lower() == "any":
            cursor.execute("SELECT user_id, name, bio, photo_id, username FROM users WHERE user_id != ? AND (looking_for = ? OR looking_for = ?)", (user_id, user_gender, "Any",))
        else:
            cursor.execute("""
                SELECT user_id, name, bio, photo_id, username
                FROM users
                WHERE user_id != ? AND gender = ? AND (looking_for = ? OR looking_for = ?)
            """, (user_id, looking_for, user_gender, "Any",))
        profiles = cursor.fetchall()

    if profiles:
        # Get the current profile based on the user's index
        current_index = user_indices[user_id]
        profile = profiles[current_index]

        # Update the index for the next profile
        user_indices[user_id] = (current_index + 1) % len(profiles)

        await show_profile(message, profile)
    else:
        await message.answer("Пока подходящих анкет нет.")


async def show_profile(message: Message, profile):
    user_id, name, bio, photo_id, username = profile

    # Inline keyboard for actions
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❤️", callback_data=f"like_{user_id}"),
            InlineKeyboardButton(text="👎", callback_data="next")
        ]
    ])
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_id,
        caption=f"{name} - {bio}",
        reply_markup=keyboard
    )


# Handling Likes and Matches
@router.callback_query(F.data.startswith("like_"))
async def handle_like(callback: CallbackQuery):
    liked_id = int(callback.data.split("_")[1])
    liker_id = callback.from_user.id

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        # Register the like
        cursor.execute("""
            INSERT OR IGNORE INTO likes (liker_id, liked_id)
            VALUES (?, ?)
        """, (liker_id, liked_id))

        # Check if it's a mutual like and no notification was sent
        cursor.execute("""
            SELECT 1 FROM likes
            WHERE liker_id = ? AND liked_id = ? AND notified = 0
        """, (liked_id, liker_id))
        is_mutual = cursor.fetchone()

        if is_mutual:
            # Fetch user details for both users
            cursor.execute("""
                SELECT username, name, bio, photo_id FROM users WHERE user_id = ?
            """, (liker_id,))
            liker_profile = cursor.fetchone()

            cursor.execute("""
                SELECT username, name, bio, photo_id FROM users WHERE user_id = ?
            """, (liked_id,))
            liked_profile = cursor.fetchone()

            # Extract details
            if liker_profile and liked_profile:
                liker_username, liker_name, liker_bio, liker_photo = liker_profile
                liked_username, liked_name, liked_bio, liked_photo = liked_profile

                # Notify both users
                match_message_liker = (
                    f"Есть взаимная симпатия!\n"
                    f"{liked_name} - {liked_bio}\n"
                    f"Можешь начинать общаться: @{liked_username}" if liked_username != "No username" else "No username available"
                )
                match_message_liked = (
                    f"Есть взаимная симпатия!\n"
                    f"{liker_name} - {liker_bio}\n"
                    f"Можешь начинать общаться: @{liker_username}" if liker_username != "No username" else "No username available"
                )

                # Send profile details to the liker
                await bot.send_photo(
                    chat_id=liker_id,
                    photo=liked_photo,
                    caption=match_message_liker
                )

                # Send profile details to the liked person
                await bot.send_photo(
                    chat_id=liked_id,
                    photo=liker_photo,
                    caption=match_message_liked
                )

                # Mark the mutual like as notified
                cursor.execute("""
                    UPDATE likes
                    SET notified = 1
                    WHERE (liker_id = ? AND liked_id = ?) OR (liker_id = ? AND liked_id = ?)
                """, (liker_id, liked_id, liked_id, liker_id))
                conn.commit()

        else:
            # If no match yet, just confirm the like
            await callback.message.answer("Листай дальше, скажем, если лайк взаимный.")

    # Acknowledge the callback query
    await callback.answer()

@router.callback_query(F.data == "next")
async def handle_next(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Check if the user index is initialized
    if user_id not in user_indices:
        user_indices[user_id] = 0

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, bio, photo_id, username FROM users WHERE user_id != ?", (user_id,))
        profiles = cursor.fetchall()

    if profiles:
        # Get the current profile based on the user's index
        current_index = user_indices[user_id]
        profile = profiles[current_index]

        # Update the index for the next profile
        user_indices[user_id] = (current_index + 1) % len(profiles)

        # Show the next profile
        await show_profile(callback.message, profile)
    else:
        await callback.message.answer("Пока никого больше нет.")

    # Acknowledge the callback query
    await callback.answer()


# Command: Update Profile
@router.message(F.text == "Заполнить анкету заново")
async def update_profile(message: Message, state: FSMContext):
    await register_command(message, state)


# Main entry point
async def main():
    await dp.start_polling(bot)

asyncio.run(main())
