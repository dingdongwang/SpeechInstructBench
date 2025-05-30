from .adjust import AdjustEvaluator
from .open import OpenEvaluator
from .close import CloseEvaluator

evaluator_mapping = {
    # 'harm': HarmEvaluator,
    'adjust': AdjustEvaluator,
    'open': OpenEvaluator,
    'close': CloseEvaluator,
}