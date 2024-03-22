class Permission():
    def __init__(self, id, dni, permission_date, start_time, return_time, reason, status, observation, validator_id, end_time = None) -> None:
        self.id = id
        self.dni = dni
        self.permission_date = permission_date
        self.start_time = start_time
        self.return_time = return_time
        self.end_time = end_time
        self.reason = reason
        self.status = status
        self.observation = observation
        self.validator_id = validator_id

    def to_json(self):
        return {
            'id': self.id,
            'dni': self.dni,
            'permission_date': self.permission_date,
            'start_time': self.start_time,
            'return_time': self.return_time,
            'end_time': self.end_time,
            'reason': self.reason,
            'status': self.status,
            'observation': self.observation,
            'validator_id': self.validator_id
        }