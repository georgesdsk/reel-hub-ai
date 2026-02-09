import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from src.domain.use_cases.ingest_video import IngestVideoUseCase
from src.domain.use_cases.search_videos import SearchVideosUseCase
from src.domain.ports.video_repository import IVideoRepository
from src.domain.ports.message_queue import IMessageQueue
from src.domain.entities.video import Video
from .validators import URLValidator
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

class TelegramBotAdapter:
    def __init__(self, ingest_use_case, search_use_case, repository, queue, rate_limiter):
        self.ingest = ingest_use_case
        self.search = search_use_case
        self.repo = repository
        self.queue = queue
        self.rate_limiter = rate_limiter
        self.bot = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("👋 ¡Hola! Soy VideoMind Bot. Envíame un enlace de Instagram o TikTok.")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📖 Comandos: /recent, /search, /stats, /categories, /help")

    async def recent_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        videos = await self.repo.list(telegram_user_id=user_id, limit=5, sort_by="saved_at", order="desc")
        if not videos:
            await update.message.reply_text("No tienes vídeos aún.")
            return
        response = "🕒 Últimos vídeos:\n" + "\n".join([f"🎬 {v.title or 'Sin título'}\n🔗 {v.url}" for v in videos])
        await update.message.reply_text(response, disable_web_page_preview=True)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        stats = await self.repo.get_statistics(telegram_user_id=user_id)
        response = f"📊 Estadísticas:\nTotal: {stats['total_videos']}\nEste mes: {stats['videos_last_month']}"
        await update.message.reply_text(response)

    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = " ".join(context.args)
        if not query:
            await update.message.reply_text("Uso: /search <texto>")
            return
        user_id = update.effective_user.id
        videos = await self.search.execute(query_text=query, telegram_user_id=user_id, limit=5)
        if not videos:
            await update.message.reply_text("No hay resultados.")
            return
        response = f"🔍 Resultados:\n" + "\n".join([f"🎬 {v.title or 'Sin título'}\n🔗 {v.url}" for v in videos])
        await update.message.reply_text(response, disable_web_page_preview=True)

    async def categories_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        categories = await self.repo.get_categories_with_count(telegram_user_id=user_id)
        response = "📁 Categorías:\n" + "\n".join([f"- {c['name']}: {c['count']}" for c in categories])
        await update.message.reply_text(response)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if not text: return
        is_valid, source, clean_url = URLValidator.validate(text)
        if not is_valid: return
        user_id = update.effective_user.id
        if not await self.rate_limiter.is_allowed(user_id):
            await update.message.reply_text("⚠️ Rate limit excedido.")
            return
        await self.rate_limiter.increment(user_id)
        note = URLValidator.extract_note(text, clean_url)
        try:
            video = await self.ingest.execute(url=clean_url, source=source, user_note=note, telegram_user_id=user_id)
            if video.processing_status == "completed":
                await update.message.reply_text("ℹ️ Ya guardado.")
                return
            job_id = await self.queue.enqueue(video.id)
            video.job_id = job_id
            await self.repo.save(video)
            await update.message.reply_text(f"✅ ¡Guardado! Procesando... ID: #{job_id}", disable_web_page_preview=True)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data.startswith("retry_"):
            video_id = query.data.split("_")[1]
            job_id = await self.queue.enqueue(video_id)
            await query.edit_message_text(f"🔄 Reintentando... Job: {job_id}")

    def setup_handlers(self, application):
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("recent", self.recent_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("search", self.search_command))
        application.add_handler(CommandHandler("categories", self.categories_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(CallbackQueryHandler(self.handle_callback_query))
        self.bot = application.bot
