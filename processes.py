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
    offset_bh: int          # Días hábiles
    default_time: str = "18:00"

# Matriz operativa con SLAs
PROCESS_RULES: Dict[ProcessType, List[ActivityRule]] = {
    ProcessType.MONTHLY: [
        ActivityRule("CUT_OFF", -7, "18:00"),
        ActivityRule("RUN", -6, "18:00"),
        ActivityRule("REPORTS", -5, "18:00"),
        ActivityRule("RUN 2", -4, "18:00"),
        ActivityRule("REPORTS R-2", -4, "18:00"),
        ActivityRule("REQUEST_SIGN_OFF", -3, "12:00"),
        ActivityRule("SEND_SIGN_OFF", -3, "15:00"),
        ActivityRule("APPROVE_SIGN_OFF", -3, "18:00"),
        ActivityRule("SEND_BANK_FILE", -2, "12:00"),
        ActivityRule("BANK_FILE_APPROVAL", -2, "16:00"),
        ActivityRule("GENERAL_LEDGER", -1, "18:00"),
        ActivityRule("OPEN_G2", -1, "18:00"),
        ActivityRule("PAY_DAY", 0, "09:00"),
    ],
    ProcessType.BIWEEKLY: [
        ActivityRule("CUT_OFF", -5, "18:00"),
        ActivityRule("RUN", -4, "18:00"),
        ActivityRule("REPORTS", -3, "18:00"),
        ActivityRule("REQUEST_SIGN_OFF", -2, "12:00"),
        ActivityRule("SEND_SIGN_OFF", -2, "15:00"),
        ActivityRule("APPROVE_SIGN_OFF", -2, "18:00"),
        ActivityRule("SEND_BANK_FILE", -1, "12:00"),
        ActivityRule("BANK_FILE_APPROVAL", -1, "16:00"),
        ActivityRule("GENERAL_LEDGER", -1, "18:00"),
        ActivityRule("PAY_DAY", 0, "09:00"),
    ],
    ProcessType.OFF_CYCLE: [
        ActivityRule("CUT_OFF", -4, "18:00"),
        ActivityRule("RUN", -3, "18:00"),
        ActivityRule("REPORTS", -2, "18:00"),
        ActivityRule("REQUEST_SIGN_OFF", -1, "12:00"),
        ActivityRule("SEND_SIGN_OFF", -1, "15:00"),
        ActivityRule("APPROVE_SIGN_OFF", -1, "18:00"),
        ActivityRule("SEND_BANK_FILE", -1, "12:00"),
        ActivityRule("PAY_DAY", 0, "09:00"),
    ],
    ProcessType.BONUS: [
        ActivityRule("CUT_OFF", -8, "18:00"),
        ActivityRule("RUN", -7, "18:00"),
        ActivityRule("REPORTS", -6, "18:00"),
        ActivityRule("REQUEST_SIGN_OFF", -4, "12:00"),
        ActivityRule("SEND_SIGN_OFF", -4, "15:00"),
        ActivityRule("APPROVE_SIGN_OFF", -4, "18:00"),
        ActivityRule("SEND_BANK_FILE", -2, "12:00"),
        ActivityRule("BANK_FILE_APPROVAL", -2, "16:00"),
        ActivityRule("GENERAL_LEDGER", -1, "18:00"),
        ActivityRule("PAY_DAY", 0, "09:00"),
    ],
    # Para TERMINATION el cálculo inicia en TERMINATION_REQUEST (0) hacia adelante
    ProcessType.TERMINATION: [
        ActivityRule("TERMINATION_REQUEST", 0, "12:00"),
        ActivityRule("RUN", 1, "18:00"),
        ActivityRule("REPORTS", 1, "18:00"),
        ActivityRule("REQUEST_SIGN_OFF", 2, "12:00"),
        ActivityRule("APPROVE_SIGN_OFF", 2, "15:00"),
        ActivityRule("SEND_BANK_FILE", 2, "17:00"),
        ActivityRule("PAY_DAY", 3, "09:00"),
    ],
}