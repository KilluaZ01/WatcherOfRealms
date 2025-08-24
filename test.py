import random
import string
from datetime import datetime

used_names = set()

def jumble_string(s):
    """Randomly shuffle or mutate parts of the input string"""
    chars = list(s)
    random.shuffle(chars)
    
    # Add random mutation (flip case, insert digits)
    for i in range(random.randint(1, 3)):
        pos = random.randint(0, len(chars)-1)
        chars[pos] = random.choice(string.ascii_letters + string.digits)
    return ''.join(chars)

def generate_unique_guest_name(index, prefix):
    """Generate a unique, jumbled guest name based on a prefix"""
    max_attempts = 1000

    for _ in range(max_attempts):
        base = f"{prefix}_{index}_{datetime.now().strftime('%f')[-4:]}"
        jumbled = jumble_string(base)
        if jumbled not in used_names:
            used_names.add(jumbled)
            print(f"[NameGen] Index={index}, Result={jumbled}")
            return jumbled
        
if __name__ == "__main__":
    generate_unique_guest_name(1, "A")
