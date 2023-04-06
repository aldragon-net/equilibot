import logging

from dotenv import dotenv_values
from telegram.ext import ApplicationBuilder


from bot.handlers.root import base_handler

# from service.schemas.models import SWProblem, SWSolution
# from service.service import isw_rsw_parameters

config = dotenv_values(".env")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()


application.add_handler(base_handler)

application.run_polling()
