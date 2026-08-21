from processes import ActivityType

# Mapeo oficial de offsets en días hábiles (Business Days)
# Ancla: PAY_DAY = 0
ACTIVITY_OFFSETS = {
    ActivityType.PAY_DAY: 0,
    ActivityType.GENERAL_LEDGER: -1,
    ActivityType.OPEN_G2: -1,
    ActivityType.SEND_BANK_FILE: -2,
    ActivityType.BANK_FILE_APPROVAL: -2,
    ActivityType.REQUEST_SIGN_OFF: -3,
    ActivityType.SEND_SIGN_OFF: -3,
    ActivityType.APPROVE_SIGN_OFF: -3,
    ActivityType.REPORTS: -5,
    ActivityType.RUN: -6,
    ActivityType.CUT_OFF: -7,
}

def get_offset(activity: ActivityType) -> int:
    """Devuelve el offset en BH para una actividad dada."""
    if activity not in ACTIVITY_OFFSETS:
        raise KeyError(f"Actividad '{activity}' no tiene un offset definido en rules.py")
    return ACTIVITY_OFFSETS[activity]