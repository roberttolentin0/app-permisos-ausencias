class AdditionalPermissionModel():
    def __init__(self, id, permission_id, reason, additional_time) -> None:
        self.id = id
        self.permission_id = permission_id
        self.reason = reason,
        self.additional_time = additional_time,

    def to_json(self):
        return {
            'id': self.id,
            'permission_id': self.permission_id,
            'reason': self.reason,
            'additional_time': self.additional_time,
        }