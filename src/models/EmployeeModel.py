class Employee():
    def __init__(self, dni, full_name) -> None:
        self.dni = dni
        self.full_name = full_name

    def to_json(self):
        return {
            'dni': self.dni,
            'full_name': self.full_name,
        }