# Entity Definition
class Api:
    def __init__( self, type, interaction, ctx, order, offset, limit ):
        self.type = type
        self.interaction = interaction
        self.ctx = ctx
        self.order = order
        self.offset = offset
        self.limit = limit
