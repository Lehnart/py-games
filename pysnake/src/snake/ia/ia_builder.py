from snake.ia.pathfinding.pathfinding_ia import PathFindingIA
from snake.ia.simple.simple_l1_ia import SimpleL1IA
from snake.ia.simple.simple_l2_ia import SimpleL2IA

class IABuilder:
    mapper = {"simple_l1": SimpleL1IA, "simple_l2": SimpleL2IA, "path_finding_ia": PathFindingIA}

    @staticmethod
    def from_name(ia_name, snake_game, controller):
        return IABuilder.mapper[ia_name](snake_game, controller)
