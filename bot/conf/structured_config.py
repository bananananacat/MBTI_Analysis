from dataclasses import dataclass, field
from hydra.core.config_store import ConfigStore

@dataclass
class Bot:
    greetings: str = (
        f"Hello, it's a tests for our ml project, welcome!\n"
        f"/start - start bot\n"
        f"/test message - predict mbti class by message"
    )
    wrong_msg: str = "There is no meaningful message :("


@dataclass
class Files:
    model: str = "compiled/finalized_model.pkl"
    vocab: str = "compiled/new_vocab.txt"


@dataclass
class Config:
    bot: Bot = field(default_factory=Bot)
    files: Files = field(default_factory=Files)


TOKEN = "7110867946:AAGaB6AqkE6s2pDEpjozRXSPCazN2Q4r7vA"

mbti_map_r = dict(
    zip(
        range(16), 
        ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
    )
)


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
