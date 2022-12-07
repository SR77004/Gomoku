
def minimax(state, depth=2):

    def max_play(state, alpha, beta, d):
        if state.is_terminal() or d >= depth:
            return state.heuristic_value
        node_value = float('-inf')
        for i, move in enumerate(state.available_moves):
            node_value = max(node_value, min_play(state.next_state(move),
                                                  alpha, beta, d+1))
            if node_value >= beta:

                return node_value
            alpha = max(alpha, node_value)

        return node_value

    def min_play(state, alpha, beta, d):
        if state.is_terminal() or d >= depth:
            return state.heuristic_value
        node_value = float('inf')
        for i, move in enumerate(state.available_moves):
            node_value = min(node_value, max_play(state.next_state(move),
                                                  alpha, beta, d+1))
            if node_value <= alpha:

                return node_value
            beta = min(beta, node_value)

        return node_value

    alpha = float('-inf')
    beta = float('inf')
    node_value = float('-inf')
    next_move = state.available_moves[0]
    for i, move in enumerate(state.available_moves):
        neighbor_value = min_play(state.next_state(move), alpha, beta, 1)

        if neighbor_value > node_value:
            node_value = neighbor_value
            next_move = move
        alpha = max(alpha, node_value)
    return next_move