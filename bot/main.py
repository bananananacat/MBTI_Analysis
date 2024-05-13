from aiogram import types, executor, Dispatcher, Bot
import hydra
import pickle
import pandas as pd

from nltk.stem.porter import *
from sklearn.utils._testing import ignore_warnings

from conf.structured_config import Config, TOKEN, mbti_map_r
from preprocessing import *


bot = Bot(TOKEN)
dp = Dispatcher(bot)


@ignore_warnings(category=UserWarning)
def predicted(msg: str) -> str:
    stemmer = SnowballStemmer('english')
    vocab = open(cfg.files.vocab, "r")
    
    df = pd.DataFrame([msg], index=['0'], columns=["text"])
    df["text"] = df["text"].apply(reg_handling)
    df["text"] = df["text"].apply(applying_stemmer, args=(stemmer,))
    df["text"] = df["text"].apply(applying_vocab, args=(content,))
    
    
    if not len(df["text"][0].strip()) or df["text"][0].strip() == "test":
        return cfg.bot.wrong_msg
    
    res: int = 0
    with open("compiled/finalized_model.pkl", 'rb') as f:
        pipeline = pickle.load(f)
        res = pipeline.predict(df["text"])[0][0]
    
    return mbti_map_r[int(res)]


@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id ,
        text=cfg.bot.greetings,
        parse_mode='HTML'
    )


@dp.message_handler(commands=['test'])
async def predicting(message: types.Message):
    msg = message.text

    await bot.send_message(
        chat_id=message.from_user.id ,
        text=predicted(msg),
        parse_mode='HTML'
    )


@hydra.main(config_name="config", version_base=None)
def main(config: Config) -> None:
    global cfg, content
    
    cfg = config
    vocab = open(cfg.files.vocab, "r")
    content = list(map(lambda x: x.strip(), vocab.readlines()))
    vocab.close()

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True
    )


if __name__ == '__main__':
    main()
