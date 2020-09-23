from rx import operators as ops
from more_itertools import take

class IntentReader:

    def __init__(self, gaia_sdk):
        self._gaia_sdk = gaia_sdk

    def read(self, identity_id: str) -> [str]:
        """
        Reads 5 intents from a given identity and returns a list of qualifiers.
        """

        def config(x):
            x.identity_id()
            x.qualifier()

        result = self._gaia_sdk.retrieve_intents(identity_id, config) \
            .pipe(ops.to_list()).run()

        items = list(map(lambda intent: intent.qualifier, result))

        return take(5, items)