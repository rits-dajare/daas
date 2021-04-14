class FontColors:
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    RESET: str = '\033[0m'


def LOAD_FILE_MSG(file_name: str) -> str:
    result: str = f'Loaded {FontColors.YELLOW}{file_name}{FontColors.RESET}'
    return result


def ACCURACY_MSG(accuracy: float) -> str:
    result: str = f'Accuracy {FontColors.YELLOW}{accuracy * 100:3.1f}%{FontColors.RESET}'
    return result


def MEASURE_ACCURACY_MSG(n_samples: int) -> str:
    result: str = f'Measure accuracy with {n_samples} samples...'
    return result


def N_SAMPLES_INPUT_GUIDE(default_samples: int, max_samples: int) -> str:
    result: str = f'How many samples? {FontColors.GREEN}{default_samples} (1-{max_samples}){FontColors.RESET} : '
    return result


def APPLIED_RULE(dajare: str, rule_name: str):
    result: str = f'Applied rule ({dajare}) : {FontColors.GREEN}{rule_name}{FontColors.RESET}'
    return result
