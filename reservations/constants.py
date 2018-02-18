FUTURE = 1
INHOUSE = 2
CHECKEDOUT = 3
STATES_CHOICES = (
    (FUTURE, 'future reservation'),
    (INHOUSE, 'guest is in-house'),
    (CHECKEDOUT, 'guest checked out')
)
STANDARD = 1
KING = 2
DELUXE = 3
ROOM_CHOICES = (
    (STANDARD, 'Standard Room'),
    (KING, 'King Room'),
    (DELUXE, 'Deluxe Room')
)