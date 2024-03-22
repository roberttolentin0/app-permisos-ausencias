class ValidatorModel():
    def __init__(self, id, type, dni) -> None:
        self.id = id
        self.type = type
        self.dni = dni

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'dni': self.dni
        }