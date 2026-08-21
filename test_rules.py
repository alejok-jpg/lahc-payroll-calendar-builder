from rules import ACTIVITY_OFFSETS, get_offset
from processes import ActivityType

def test_rules():
    print("--- Reglas de Offsets Cargadas ---")
    for act, offset in ACTIVITY_OFFSETS.items():
        print(f"{act.name:<20} -> {offset:>2} BH")

if __name__ == "__main__":
    test_rules()