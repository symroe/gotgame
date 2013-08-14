RESULT_VOID = 0
RESULT_WON = 1
RESULT_LOST = 2
RESULT_DISPUTE = 3

GAME_RESULTS = (
    (RESULT_VOID, 'Void'),
    (RESULT_WON, 'Won'),
    (RESULT_LOST, 'Lost'),
    (RESULT_DISPUTE, 'Dispute'),
)

def valid_levels():
    start = 1
    for i in range(0,21):
        yield (start, start)
        start = start * 2
