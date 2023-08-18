class Rules(object):
    class ObstructionType(Enum):
        """
        Enumerates the types of obstructions in the chess game
        """
        SELF_OBSTRUCTED = 'self obstructed'
        OPPONENT_OBSTRUCTED = 'opponent obstructed'
        UNOBSTRUCTED = 'unobstructed'

    @classmethod
    def detect_obstruction(cls, source, target, board):
        """
        Detect if the piece is obstructed
        """
        # make sure its not checking its self
        if source != target:
            # Same colour pieces
            if board[source].colour == board[target].colour:
                return cls.ObstructionType.SELF_OBSTRUCTED
            # opponent pieces
            elif board[source].colour != 'none':
                return cls.ObstructionType.OPPONENT_OBSTRUCTED
            else:
                return cls.ObstructionType.UNOBSTRUCTED

