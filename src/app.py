from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
from dotenv import load_dotenv
import os
import logging

from core.get_chat_history import get_chat_history
from core.save_message import save_message
from core.summarize import summarize

load_dotenv()

logging.basicConfig(format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def message_handler(update: Update, context: CallbackContext) -> None:
    """
    Save the message to the chat history.
    
    This function is called when the user sends a message.
    It saves the message to the chat history file.
    """

    is_edited = update.edited_message is not None
    message = update.edited_message if is_edited else update.message

    save_message(message, is_edited)


async def summarize_handler(update: Update, context: CallbackContext) -> None:
    """
    Generate a summary of the chat history.

    This function is called when the user sends the /summary command.
    It retrieves the chat history and sends it to the summarization model.
    Then, it sends the generated summary to the chat.
    """

    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message with the /summarize command to get a brief summary of the messages sent after it.")
        return
    
    chat_id = update.message.chat_id
    from_message_id = update.message.reply_to_message.message_id

    try:
        messages = get_chat_history(chat_id, from_message_id)

        if not messages or len(messages) == 0:
            await update.message.reply_text("No messages found to summarize. Most likely bot was just added to the chat.")
            return
        
    except Exception:
        await update.message.reply_text("Something went wrong while trying to retrieve the chat history.")
        logger.exception("Error while trying to retrieve the chat history.")
        return

    response_message = await update.message.reply_text("Generating summary... Please wait.")
    summary_generator = summarize(messages)

    for partial_response in summary_generator:
        try:
            await response_message.edit_text(partial_response)
        except Exception:
            pass


def error_handler(update: Update, context: CallbackContext):
    """
    Log the error.

    This function is called when an error occurs.
    It logs the error to the console.
    """

    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    app.add_handler(CommandHandler("summarize", summarize_handler))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == '__main__':
    main()
