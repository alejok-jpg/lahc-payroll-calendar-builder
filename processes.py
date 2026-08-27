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
    offset_bh: int          # Días hábiles respecto a Pay Day
    default_time: str = "18:00"
    owner: str = "ADP"     # Owner: Client o ADP

# Matriz operativa con SLAs, Horarios y Responsables (Owners)
PROCESS_RULES: Dict[ProcessType, List[ActivityRule]] = {
    ProcessType.MONTHLY: [
        ActivityRule("CUT_OFF", -7, "18:00", "Client"),
        ActivityRule("RUN", -6, "18:00", "ADP"),
        ActivityRule("REPORTS", -5, "18:00", "ADP"),
        ActivityRule("RUN 2", -4, "18:00", "ADP"),
        ActivityRule("REPORTS R-2", -4, "18:00", "ADP"),
        ActivityRule("REQUEST_SIGN_OFF", -3, "12:00", "Client"),
        ActivityRule("SEND_SIGN_OFF", -3, "15:00", "ADP"),
        ActivityRule("APPROVE_SIGN_OFF", -3, "18:00", "Client"),
        ActivityRule("SEND_BANK_FILE", -2, "12:00", "ADP"),
        ActivityRule("BANK_FILE_APPROVAL", -2, "16:00", "Client"),
        ActivityRule("GENERAL_LEDGER", -1, "18:00", "ADP"),
        ActivityRule("OPEN_G2", -1, "18:00", "ADP"),
        ActivityRule("PAY_DAY", 0, "09:00", "Client"),
        ActivityRule("LEGAL REPORTS", 2, "18:00", "ADP"),
        ActivityRule("LEGAL REPORTS 2", 5, "18:00", "ADP"),
    ],
    ProcessType.BIWEEKLY: [
        ActivityRule("CUT_OFF", -5, "18:00", "Client"),
        ActivityRule("RUN", -4, "18:00", "ADP"),
        ActivityRule("REPORTS", -3, "18:00", "ADP"),
        ActivityRule("RUN 2", -3, "18:00", "ADP"),
        ActivityRule("REPORTS R-2", -3, "18:00", "ADP"),
        ActivityRule("REQUEST_SIGN_OFF", -2, "12:00", "Client"),
        ActivityRule("SEND_SIGN_OFF", -2, "15:00", "ADP"),
        ActivityRule("APPROVE_SIGN_OFF", -2, "18:00", "Client"),
        ActivityRule("SEND_BANK_FILE", -1, "12:00", "ADP"),
        ActivityRule("BANK_FILE_APPROVAL", -1, "16:00", "Client"),
        ActivityRule("GENERAL_LEDGER", -1, "18:00", "ADP"),
        ActivityRule("PAY_DAY", 0, "09:00", "Client"),
        ActivityRule("LEGAL REPORTS", 2, "18:00", "ADP"),
        ActivityRule("LEGAL REPORTS 2", 5, "18:00", "ADP"),
    ],
    ProcessType.OFF_CYCLE: [
        ActivityRule("CUT_OFF", -4, "18:00", "Client"),
        ActivityRule("RUN", -3, "18:00", "ADP"),
        ActivityRule("REPORTS", -2, "18:00", "ADP"),
        ActivityRule("REQUEST_SIGN_OFF", -1, "12:00", "Client"),
        ActivityRule("SEND_SIGN_OFF", -1, "15:00", "ADP"),
        ActivityRule("APPROVE_SIGN_OFF", -1, "18:00", "Client"),
        ActivityRule("SEND_BANK_FILE", -1, "12:00", "ADP"),
        ActivityRule("PAY_DAY", 0, "09:00", "Client"),
    ],
    ProcessType.BONUS: [
        ActivityRule("CUT_OFF", -8, "18:00", "Client"),
        ActivityRule("RUN", -7, "18:00", "ADP"),
        ActivityRule("REPORTS", -6, "18:00", "ADP"),
        ActivityRule("REQUEST_SIGN_OFF", -4, "12:00", "Client"),
        ActivityRule("SEND_SIGN_OFF", -4, "15:00", "ADP"),
        ActivityRule("APPROVE_SIGN_OFF", -4, "18:00", "Client"),
        ActivityRule("SEND_BANK_FILE", -2, "12:00", "ADP"),
        ActivityRule("BANK_FILE_APPROVAL", -2, "16:00", "Client"),
        ActivityRule("GENERAL_LEDGER", -1, "18:00", "ADP"),
        ActivityRule("PAY_DAY", 0, "09:00", "Client"),
    ],
    ProcessType.TERMINATION: [
        ActivityRule("TERMINATION_REQUEST", 0, "12:00", "Client"),
        ActivityRule("RUN", 1, "18:00", "ADP"),
        ActivityRule("REPORTS", 1, "18:00", "ADP"),
        ActivityRule("REQUEST_SIGN_OFF", 2, "12:00", "Client"),
        ActivityRule("APPROVE_SIGN_OFF", 2, "15:00", "Client"),
        ActivityRule("SEND_BANK_FILE", 2, "17:00", "ADP"),
        ActivityRule("PAY_DAY", 3, "09:00", "Client"),
    ],
}