import asyncio
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from models import get_db, create_tables
from database import DatabaseManager
from config import Config
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create database tables
create_tables()

class FinanceBot:
    def __init__(self):
        self.application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, self.handle_webapp_data))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        # Create or get user from database
        db = next(get_db())
        db_manager = DatabaseManager(db)
        db_user = db_manager.get_or_create_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Welcome message
        welcome_text = f"""
🎉 Добро пожаловать в Финансовый менеджер, {user.first_name}!

Этот бот поможет вам вести учет доходов и расходов, управлять кошельками и анализировать ваши финансы.

💡 Основные возможности:
• 📊 Учет доходов и расходов
• 💳 Управление кошельками
• 🏷️ Категории трат
• 💰 Источники дохода
• 📈 Детальная отчетность
• 💱 Поддержка валют: BYN, RUB, USD

Нажмите кнопку ниже, чтобы открыть веб-приложение:
        """
        
        # Create web app button
        keyboard = [
            [InlineKeyboardButton(
                "📱 Открыть приложение", 
                web_app=WebAppInfo(url=f"{Config.WEBAPP_URL}?user_id={user.id}")
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 <b>Справка по командам:</b>

/start - Запустить бота и открыть приложение
/menu - Показать главное меню
/help - Показать эту справку

💡 <b>Как использовать:</b>

1. Нажмите кнопку "Открыть приложение" в главном меню
2. В веб-приложении вы можете:
   • Добавлять доходы и расходы
   • Создавать кошельки в разных валютах
   • Настраивать категории трат
   • Добавлять источники дохода
   • Просматривать отчеты и аналитику

📱 <b>Поддерживаемые валюты:</b>
• BYN (Белорусский рубль)
• RUB (Российский рубль)
• USD (Доллар США)

🔒 <b>Безопасность:</b>
Все ваши данные хранятся локально и доступны только вам.
        """
        
        keyboard = [
            [InlineKeyboardButton(
                "📱 Открыть приложение", 
                web_app=WebAppInfo(url=f"{Config.WEBAPP_URL}?user_id={update.effective_user.id}")
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            help_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu command"""
        menu_text = """
📱 <b>Главное меню</b>

Выберите действие:
        """
        
        keyboard = [
            [InlineKeyboardButton(
                "📊 Открыть приложение", 
                web_app=WebAppInfo(url=f"{Config.WEBAPP_URL}?user_id={update.effective_user.id}")
            )],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            menu_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def handle_webapp_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle web app data"""
        try:
            # Get data from web app
            data = update.effective_message.web_app_data.data
            user = update.effective_user
            
            # Process the data if needed
            # For now, just acknowledge receipt
            await update.message.reply_text(
                "✅ Данные получены! Проверьте веб-приложение для обновлений.",
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Error handling web app data: {e}")
            await update.message.reply_text(
                "❌ Произошла ошибка при обработке данных. Попробуйте еще раз.",
                parse_mode='HTML'
            )
    
    async def send_notification(self, user_id: int, message: str):
        """Send notification to user"""
        try:
            await self.application.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Error sending notification to {user_id}: {e}")
    
    def run(self):
        """Run the bot"""
        logger.info("Starting Finance Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    if not Config.TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not set in environment variables")
        return
    
    bot = FinanceBot()
    bot.run()

if __name__ == '__main__':
    main() 