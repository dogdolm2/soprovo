import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
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

API_TOKEN = 'BOT_TOKEN'

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
                photo_id TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS likes (
                liker_id INTEGER,
                liked_id INTEGER,
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


# Keyboards
# Correct ReplyKeyboardMarkup creation
menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="View Profiles")],  # Each row is a list of buttons
        [KeyboardButton(text="Update Profile")]
    ],
    resize_keyboard=True
)


# Command: /start
@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Welcome to Matchmaker Bot! Use /register to create your profile.", reply_markup=menu_kb)


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



# Step 1: Get name
@router.message(RegisterProfile.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Напиши о себе, желательно упомяни возраст и корпус лицея")
    await state.set_state(RegisterProfile.bio)


# Step 2: Get bio
@router.message(RegisterProfile.bio)
async def get_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await message.answer("Какую фотку поставить тебе на анкету?")
    await state.set_state(RegisterProfile.photo)


# Step 3: Save profile
@router.message(RegisterProfile.photo, F.photo)
async def save_profile(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    name = data.get("name")
    bio = data.get("bio")
    username = message.from_user.username or "No username"
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_id,
        caption=f"Твоя анкета:\n{name} - {bio}",
    )
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (user_id, username, name, bio, photo_id) VALUES (?, ?, ?, ?, ?)
        """, (message.from_user.id, username, name, bio, photo_id))
        conn.commit()

    await state.clear()
    await message.answer("Теперь можешь знакомиться, нажми на кнопку внизу.", reply_markup=menu_kb)


# Viewing Profiles
@router.message(F.text == "View Profiles")
async def view_profiles(message: Message):
    user_id = message.from_user.id

    # Initialize the user's profile index if not set
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

        await show_profile(message, profile)
    else:
        await message.answer("Пока нет анкет, кроме тебя")


async def show_profile(message: Message, profile):
    user_id, name, bio, photo_id, username = profile

    # Inline keyboard for actions
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👍 Like", callback_data=f"like_{user_id}"),
            InlineKeyboardButton(text="⏩ Next", callback_data="next")
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
        cursor.execute("INSERT OR IGNORE INTO likes (liker_id, liked_id) VALUES (?, ?)", (liker_id, liked_id))
        # Check if it's a mutual like
        cursor.execute("SELECT 1 FROM likes WHERE liker_id = ? AND liked_id = ?", (liked_id, liker_id))
        is_mutual = cursor.fetchone()

        # Fetch user details for both users if mutual like
        if is_mutual:
            cursor.execute("SELECT username, name, bio, photo_id FROM users WHERE user_id = ?", (liker_id,))
            liker_profile = cursor.fetchone()

            cursor.execute("SELECT username, name, bio, photo_id FROM users WHERE user_id = ?", (liked_id,))
            liked_profile = cursor.fetchone()

    if is_mutual and liker_profile and liked_profile:
        # Extract details
        liker_username, liker_name, liker_bio, liker_photo = liker_profile
        liked_username, liked_name, liked_bio, liked_photo = liked_profile

        # Send match notification with profile details to both users
        match_message_liker = (
            f"Есть взаимная симпатия!\n"
            f"{liked_name} - "
            f"{liked_bio}\n"
            f"Можешь начинать общаться: @{liked_username}" if liked_username != "No username" else "No username available"
        )
        match_message_liked = (
            f"Есть взаимная симпатия!\n"
            f"{liker_name} - "
            f"{liker_bio}\n"
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
    else:
        # If no match yet, just confirm the like
        await callback.message.answer("Листай дальше, скажем, если лайк взаимный")

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
        await callback.message.answer("No profiles available yet.")

    # Acknowledge the callback query
    await callback.answer()


# Command: Update Profile
@router.message(F.text == "Update Profile")
async def update_profile(message: Message, state: FSMContext):
    await register_command(message, state)


# Main entry point
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
