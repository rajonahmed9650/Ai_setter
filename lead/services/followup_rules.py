from datetime import timedelta

FOLLOWUP_RULES = [
    {
        "min": 10,
        "max": 40,
        "delay": timedelta(minutes=10),
        "message": "Hey… where’d you go? 🙂\nJust wanted to check in and see if you were still around."
    },
    {
        "min": 41,
        "max": 60,
        "delay": timedelta(minutes=15),
        "message": "Hey, didn’t hear back from you.\nIf you’re still interested, I’d be happy to continue 😊"
    },
    {
        "min": 61,
        "max": 100,
        "delay": timedelta(minutes=20),
        "message": "Hey — just following up real quick.\nDid you see my last message?"
    },
]
