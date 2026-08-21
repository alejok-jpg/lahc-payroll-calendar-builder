from enum import Enum
from dataclasses import dataclass
from typing import List, Dict

class ProcessType(Enum):
    MONTHLY = "Monthly Payroll"
    BIWEEKLY = "Biweekly Payroll"
    OFF_CYCLE = "Off-Cycle Payroll"
    BONUS = "Bonus / Incentive"
    TERMINATION = "Termination / Settlement"

@dataclass
class ActivityRule:
    activity: str
    offset_bh: int  # Offset en días hábiles respecto al Pay Day (0)

# Matriz de SLAs estándar
PROCESS_RULES: Dict[ProcessType, List[ActivityRule]] = {
    ProcessType.MONTHLY: [
        ActivityRule("CUT_OFF", -7),
        ActivityRule("RUN", -6),
        ActivityRule("REPORTS", -5),
        ActivityRule("REQUEST_SIGN_OFF", -3),
        ActivityRule("SEND_SIGN_OFF", -3),
        ActivityRule("APPROVE_SIGN_OFF", -3),
        ActivityRule("SEND_BANK_FILE", -2),
        ActivityRule("BANK_FILE_APPROVAL", -2),
        ActivityRule("GENERAL_LEDGER", -1),
        ActivityRule("OPEN_G2", -1),
        ActivityRule("PAY_DAY", 0),
    ],
    ProcessType.BIWEEKLY: [
        ActivityRule("CUT_OFF", -5),
        ActivityRule("RUN", -4),
        ActivityRule("REPORTS", -3),
        ActivityRule("REQUEST_SIGN_OFF", -2),
        ActivityRule("SEND_SIGN_OFF", -2),
        ActivityRule("APPROVE_SIGN_OFF", -2),
        ActivityRule("SEND_BANK_FILE", -1),
        ActivityRule("BANK_FILE_APPROVAL", -1),
        ActivityRule("GENERAL_LEDGER", -1),
        ActivityRule("PAY_DAY", 0),
    ],
    ProcessType.OFF_CYCLE: [
        ActivityRule("CUT_OFF", -4),
        ActivityRule("RUN", -3),
        ActivityRule("REPORTS", -2),
        ActivityRule("REQUEST_SIGN_OFF", -1),
        ActivityRule("SEND_SIGN_OFF", -1),
        ActivityRule("APPROVE_SIGN_OFF", -1),
        ActivityRule("SEND_BANK_FILE", -1),
        ActivityRule("PAY_DAY", 0),
    ],
    ProcessType.BONUS: [
        ActivityRule("CUT_OFF", -8),
        ActivityRule("RUN", -7),
        ActivityRule("REPORTS", -6),
        ActivityRule("REQUEST_SIGN_OFF", -4),
        ActivityRule("SEND_SIGN_OFF", -4),
        ActivityRule("APPROVE_SIGN_OFF", -4),
        ActivityRule("SEND_BANK_FILE", -2),
        ActivityRule("BANK_FILE_APPROVAL", -2),
        ActivityRule("GENERAL_LEDGER", -1),
        ActivityRule("PAY_DAY", 0),
    ],
    ProcessType.TERMINATION: [
        ActivityRule("CUT_OFF", -3),
        ActivityRule("RUN", -2),
        ActivityRule("REPORTS", -2),
        ActivityRule("REQUEST_SIGN_OFF", -1),
        ActivityRule("SEND_SIGN_OFF", -1),
        ActivityRule("APPROVE_SIGN_OFF", -1),
        ActivityRule("SEND_BANK_FILE", -1),
        ActivityRule("PAY_DAY", 0),
    ],
}