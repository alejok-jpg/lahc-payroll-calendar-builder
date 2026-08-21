from enum import Enum, auto
from typing import List, Dict

class ProcessType(Enum):
    MONTHLY = auto()
    TERMINATION = auto()
    ADVANCE = auto()
    OFF_CYCLE = auto()
    BIWEEKLY = auto()
    BONUS = auto()

class ActivityType(Enum):
    CUT_OFF = auto()
    RUN = auto()
    REPORTS = auto()
    REQUEST_SIGN_OFF = auto()
    SEND_SIGN_OFF = auto()
    APPROVE_SIGN_OFF = auto()
    SEND_BANK_FILE = auto()
    BANK_FILE_APPROVAL = auto()
    GENERAL_LEDGER = auto()
    OPEN_G2 = auto()
    PAY_DAY = auto()

# Definición de qué actividades aplican a cada proceso
PROCESS_ACTIVITIES: Dict[ProcessType, List[ActivityType]] = {
    ProcessType.MONTHLY: [
        ActivityType.CUT_OFF,
        ActivityType.RUN,
        ActivityType.REPORTS,
        ActivityType.REQUEST_SIGN_OFF,
        ActivityType.SEND_SIGN_OFF,
        ActivityType.APPROVE_SIGN_OFF,
        ActivityType.SEND_BANK_FILE,
        ActivityType.BANK_FILE_APPROVAL,
        ActivityType.GENERAL_LEDGER,
        ActivityType.OPEN_G2,
        ActivityType.PAY_DAY,
    ],
    ProcessType.TERMINATION: [
        ActivityType.CUT_OFF,
        ActivityType.RUN,
        ActivityType.REPORTS,
        ActivityType.REQUEST_SIGN_OFF,
        ActivityType.SEND_SIGN_OFF,
        ActivityType.APPROVE_SIGN_OFF,
        ActivityType.SEND_BANK_FILE,
        ActivityType.BANK_FILE_APPROVAL,
        ActivityType.GENERAL_LEDGER,
        ActivityType.PAY_DAY,
    ],
    ProcessType.ADVANCE: [
        ActivityType.CUT_OFF,
        ActivityType.RUN,
        ActivityType.SEND_BANK_FILE,
        ActivityType.BANK_FILE_APPROVAL,
        ActivityType.GENERAL_LEDGER,
        ActivityType.PAY_DAY,
    ],
    ProcessType.OFF_CYCLE: [
        ActivityType.CUT_OFF,
        ActivityType.RUN,
        ActivityType.REPORTS,
        ActivityType.SEND_BANK_FILE,
        ActivityType.BANK_FILE_APPROVAL,
        ActivityType.GENERAL_LEDGER,
        ActivityType.PAY_DAY,
    ],
    ProcessType.BIWEEKLY: [
        ActivityType.CUT_OFF,
        ActivityType.RUN,
        ActivityType.REPORTS,
        ActivityType.REQUEST_SIGN_OFF,
        ActivityType.SEND_SIGN_OFF,
        ActivityType.APPROVE_SIGN_OFF,
        ActivityType.SEND_BANK_FILE,
        ActivityType.BANK_FILE_APPROVAL,
        ActivityType.GENERAL_LEDGER,
        ActivityType.PAY_DAY,
    ],
    ProcessType.BONUS: [
        ActivityType.CUT_OFF,
        ActivityType.RUN,
        ActivityType.REPORTS,
        ActivityType.REQUEST_SIGN_OFF,
        ActivityType.SEND_SIGN_OFF,
        ActivityType.APPROVE_SIGN_OFF,
        ActivityType.SEND_BANK_FILE,
        ActivityType.BANK_FILE_APPROVAL,
        ActivityType.GENERAL_LEDGER,
        ActivityType.PAY_DAY,
    ],
}

def get_process_activities(process: ProcessType) -> List[ActivityType]:
    """Retorna la lista de actividades configuradas para un proceso determinado."""
    if process not in PROCESS_ACTIVITIES:
        raise KeyError(f"El proceso '{process}' no tiene actividades configuradas.")
    return PROCESS_ACTIVITIES[process]