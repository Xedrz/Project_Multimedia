"""
Modul untuk mengatur rintangan berupa emoji secara acak.
"""

import random

class ChallengeManager:
    """
    Kelas untuk menangani rintangan emoji.
    """
    def __init__(self):
        self.emojis = ["✋", "☝️", "✌️"]
        self.current = random.choice(self.emojis)

    def get_current_challenge(self):
        """
        Mendapatkan emoji rintangan saat ini.
        Returns:
            str: Emoji saat ini.
        """
        return self.current

    def new_challenge(self):
        """
        Mengambil emoji rintangan baru.
        Returns:
            str: Emoji baru.
        """
        self.current = random.choice(self.emojis)
        return self.current
