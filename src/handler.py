import logging
import os

from gaia_sdk.api.GaiaCredentials import HMACCredentials
from gaia_sdk.gaia import Gaia
from src.adder import Adder
from src.intent_reader import IntentReader

api_key = os.environ["GAIA_API_KEY"]
api_secret = os.environ["GAIA_API_SECRET"]
url = os.environ["GAIA_URL"]

gaia_sdk = Gaia.connect(url, HMACCredentials(api_key, api_secret))

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("skill")

intent_reader = IntentReader(gaia_sdk)


def evaluate(payload: dict, context: dict) -> dict:
    log.info(f"received a message: {payload}")
    log.info(f"context: {context}")

    if context["namespace"] == "intents.incoming":
        identity_id = payload["identityId"]
        return {'@intents': {'qualifiers': intent_reader.read(identity_id)}}
    elif context["namespace"] == "echo.incoming":
        return {'@echo': {'response': payload["text"]}}
    elif context["namespace"] == "adder.incoming":
        result = Adder.add(payload['a'], payload['b'])
        return {'@adder': {'result': result}}
    else:
        raise Exception("Can not handle this kind of message")


def on_started(context):
    log.info("on_started triggered")