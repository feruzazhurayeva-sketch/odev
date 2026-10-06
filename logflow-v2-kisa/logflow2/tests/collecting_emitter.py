from logflow.emitter import Emitter


class CollectingEmitter(Emitter):
    """Test dublori: stage'in yaydigi ogeleri listeye toplar (dosya/sink gerekmez)."""

    def __init__(self) -> None:
        self.items = []

    def emit(self, item) -> None:
        self.items.append(item)
