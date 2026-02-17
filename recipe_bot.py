import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# ==================== НАСТРОЙКИ ====================
TOKEN = "8195675259:AAGCPViJnbJi6TgFT_zFg2_M9K4L059VgJE"  
DATA_FILE = "recipes_data.json"

# ==================== ДАННЫЕ РЕЦЕПТОВ ====================
# Если файл с данными не существует, создадим его
if not os.path.exists(DATA_FILE):
    recipes_data = {
        "categories": {
            "appetizers": [
                {"id": "bruschetta", "name": "Bruschetta", "description": "Italian appetizer with tomatoes and basil"},
                {"id": "spring_rolls", "name": "Spring Rolls", "description": "Vietnamese fresh rolls with shrimp"},
                {"id": "guacamole", "name": "Guacamole", "description": "Mexican avocado dip"}
            ],
            "main": [
                {"id": "pasta_carbonara", "name": "Pasta Carbonara", "description": "Classic Italian pasta with eggs and pancetta"},
                {"id": "sushi_rolls", "name": "Sushi Rolls", "description": "Japanese rolled sushi with fish and rice"},
                {"id": "beef_burger", "name": "Beef Burger", "description": "American classic burger with beef patty"}
            ],
            "desserts": [
                {"id": "tiramisu", "name": "Tiramisu", "description": "Italian coffee-flavored dessert"},
                {"id": "cheesecake", "name": "New York Cheesecake", "description": "Creamy American cheesecake"},
                {"id": "baklava", "name": "Baklava", "description": "Sweet Turkish pastry with nuts"}
            ]
        },
        "recipes": {
            "bruschetta": {
                "description": "A classic Italian appetizer consisting of grilled bread rubbed with garlic and topped with tomatoes, fresh basil, and olive oil.",
                "ingredients": "• Bread slices\n• Ripe tomatoes\n• Fresh basil\n• Garlic\n• Olive oil\n• Salt & pepper",
                "recipe": "1. Toast bread slices\n2. Rub with garlic\n3. Dice tomatoes and mix with chopped basil\n4. Add olive oil, salt, pepper\n5. Top bread with mixture"
            },
            "pasta_carbonara": {
                "description": "Traditional Roman pasta dish made with eggs, hard cheese, guanciale, and black pepper.",
                "ingredients": "• Spaghetti 400g\n• Guanciale 150g\n• Eggs 3\n• Pecorino cheese 100g\n• Black pepper",
                "recipe": "1. Cook pasta al dente\n2. Fry guanciale until crispy\n3. Mix eggs, cheese, and pepper\n4. Combine everything off heat\n5. Serve immediately"
            },
            "tiramisu": {
                "description": "Popular Italian dessert of coffee-soaked ladyfingers layered with mascarpone cream.",
                "ingredients": "• Ladyfingers\n• Mascarpone cheese\n• Eggs\n• Coffee\n• Cocoa powder\n• Sugar",
                "recipe": "1. Brew strong coffee\n2. Mix mascarpone with eggs and sugar\n3. Dip ladyfingers in coffee\n4. Layer with cream\n5. Dust with cocoa"
            }
        }
    }
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(recipes_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Created {DATA_FILE} with sample data")
else:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        recipes_data = json.load(f)
    print(f"✅ Loaded data from {DATA_FILE}")

# ==================== ИНИЦИАЛИЗАЦИЯ БОТА ====================
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==================== КЛАВИАТУРЫ ====================
def get_main_menu():
    """Клавиатура для главного меню"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📋 Menu", callback_data="show_categories"))
    return builder.as_markup()

def get_categories_keyboard():
    """Клавиатура с категориями блюд"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🥗 Appetizers", callback_data="category_appetizers"))
    builder.row(InlineKeyboardButton(text="🍝 Main Course", callback_data="category_main"))
    builder.row(InlineKeyboardButton(text="🍰 Desserts", callback_data="category_desserts"))
    return builder.as_markup()

def get_dishes_keyboard(category: str):
    """Клавиатура с блюдами конкретной категории"""
    builder = InlineKeyboardBuilder()
    
    dishes = recipes_data["categories"].get(category, [])
    
    for dish in dishes:
        builder.row(InlineKeyboardButton(
            text=f"🍽️ {dish['name']}", 
            callback_data=f"dish_{dish['id']}"
        ))
    
    # Кнопка "Назад" в категории
    builder.row(InlineKeyboardButton(
        text="⬅️ Back to Categories", 
        callback_data="show_categories"
    ))
    
    return builder.as_markup()

def get_dish_details_keyboard(dish_id: str, category: str):
    """Клавиатура для деталей блюда"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(
        text="📝 Ingredients", 
        callback_data=f"ingredients_{dish_id}"
    ))
    
    builder.row(InlineKeyboardButton(
        text="👨‍🍳 Recipe", 
        callback_data=f"recipe_{dish_id}"
    ))
    
    # Кнопка "Назад" к списку блюд в категории
    builder.row(InlineKeyboardButton(
        text=f"⬅️ Back to {category.capitalize()}", 
        callback_data=f"category_{category}"
    ))
    
    return builder.as_markup()

def get_back_to_dish_keyboard(dish_id: str, category: str):
    """Клавиатура для возврата к описанию блюда"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(
        text="⬅️ Back to Dish", 
        callback_data=f"dish_{dish_id}"
    ))
    
    builder.row(InlineKeyboardButton(
        text=f"⬅️ Back to {category.capitalize()}", 
        callback_data=f"category_{category}"
    ))
    
    return builder.as_markup()

# ==================== ОБРАБОТЧИКИ КОМАНД ====================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👨‍🍳 *Welcome to nations of Russia Recipes Bot!*\n\n"
        "I'm your personal chef assistant. Here you can find delicious recipes from different cuisines around the world.\n\n"
        "Explore recipes by categories, learn about ingredients, and cook amazing dishes!"
    )
    
    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

# ==================== ОБРАБОТЧИКИ КНОПОК ====================
@dp.callback_query(F.data == "show_categories")
async def show_categories(callback: types.CallbackQuery):
    """Показываем категории блюд"""
    categories_text = (
        "📚 *Recipe Categories*\n\n"
        "Here you can find various recipes from different cuisines. "
        "Choose a category to see available dishes:"
    )
    
    await callback.message.edit_text(
        categories_text,
        parse_mode="Markdown",
        reply_markup=get_categories_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("category_"))
async def show_category_dishes(callback: types.CallbackQuery):
    """Показываем блюда выбранной категории"""
    category = callback.data.replace("category_", "")
    
    # Названия категорий для красивого отображения
    category_names = {
        "appetizers": "🥗 Appetizers",
        "main": "🍝 Main Course", 
        "desserts": "🍰 Desserts"
    }
    
    category_name = category_names.get(category, category.capitalize())
    
    dishes = recipes_data["categories"].get(category, [])
    
    if not dishes:
        await callback.message.edit_text(
            f"No dishes found in {category_name} category.",
            reply_markup=get_categories_keyboard()
        )
        await callback.answer()
        return
    
    # Формируем текст с блюдами
    dishes_text = f"{category_name}\n\n"
    dishes_text += "Available dishes:\n"
    
    for i, dish in enumerate(dishes, 1):
        dishes_text += f"\n{i}. *{dish['name']}*"
        if 'description' in dish:
            dishes_text += f" - {dish['description']}"
    
    await callback.message.edit_text(
        dishes_text,
        parse_mode="Markdown",
        reply_markup=get_dishes_keyboard(category)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("dish_"))
async def show_dish_details(callback: types.CallbackQuery):
    """Показываем детали выбранного блюда"""
    dish_id = callback.data.replace("dish_", "")
    
    # Находим блюдо в данных
    dish_info = None
    dish_category = None
    
    # Ищем блюдо в категориях
    for category, dishes in recipes_data["categories"].items():
        for dish in dishes:
            if dish["id"] == dish_id:
                dish_info = dish
                dish_category = category
                break
        if dish_info:
            break
    
    if not dish_info:
        await callback.message.edit_text(
            "Dish not found. Please try another one.",
            reply_markup=get_categories_keyboard()
        )
        await callback.answer()
        return
    
    # Получаем полное описание из recipes
    full_description = recipes_data["recipes"].get(dish_id, {}).get(
        "description", 
        dish_info.get("description", "No detailed description available.")
    )
    
    dish_text = (
        f"🍽️ *{dish_info['name']}*\n\n"
        f"{full_description}\n\n"
        f"Choose what you want to see:"
    )
    
    await callback.message.edit_text(
        dish_text,
        parse_mode="Markdown",
        reply_markup=get_dish_details_keyboard(dish_id, dish_category)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("ingredients_"))
async def show_ingredients(callback: types.CallbackQuery):
    """Показываем ингредиенты блюда"""
    dish_id = callback.data.replace("ingredients_", "")
    
    ingredients = recipes_data["recipes"].get(dish_id, {}).get("ingredients", "Ingredients not specified.")
    
    # Находим название блюда
    dish_name = "Unknown Dish"
    dish_category = None
    
    for category, dishes in recipes_data["categories"].items():
        for dish in dishes:
            if dish["id"] == dish_id:
                dish_name = dish["name"]
                dish_category = category
                break
    
    ingredients_text = (
        f"📝 *{dish_name} - Ingredients*\n\n"
        f"{ingredients}\n\n"
        f"Would you like to see the recipe?"
    )
    
    await callback.message.edit_text(
        ingredients_text,
        parse_mode="Markdown",
        reply_markup=get_back_to_dish_keyboard(dish_id, dish_category)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("recipe_"))
async def show_recipe(callback: types.CallbackQuery):
    """Показываем рецепт приготовления"""
    dish_id = callback.data.replace("recipe_", "")
    
    recipe = recipes_data["recipes"].get(dish_id, {}).get("recipe", "Recipe not available.")
    
    # Находим название блюда
    dish_name = "Unknown Dish"
    dish_category = None
    
    for category, dishes in recipes_data["categories"].items():
        for dish in dishes:
            if dish["id"] == dish_id:
                dish_name = dish["name"]
                dish_category = category
                break
    
    recipe_text = (
        f"👨‍🍳 *{dish_name} - Recipe*\n\n"
        f"{recipe}\n\n"
        f"🍴 *Bon Appétit!* 🍴"
    )
    
    await callback.message.edit_text(
        recipe_text,
        parse_mode="Markdown",
        reply_markup=get_back_to_dish_keyboard(dish_id, dish_category)
    )
    await callback.answer()

# ==================== ЗАПУСК БОТА ====================
async def main():
    print("🚀 Recipe Bot is starting...")
    print("✅ Bot is ready! Go to Telegram and test it.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")

