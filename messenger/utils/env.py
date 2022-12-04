import os

from dotenv import load_dotenv

load_dotenv()


def getenv(env):
    return os.getenv(env)
