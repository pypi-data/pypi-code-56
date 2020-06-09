from procspec.parse import register_proc
import json

@register_proc("Patchwise")
class PatchwiseProcessor:
    def __init__(self, **kwargs):
        self.args = kwargs

    def __call__(self, **kwargs):
        pass

import modelhouse
@register_proc("ApplyModel")
class ApplyModelProcessor:
    def __init__(self, path, **kwargs):
        self.model = modelhouse.load_model(path, params=json.dumps(kwargs))

    def __call__(self, args):
        return self.model(**args)

