from src.utils.DateFormat import DateFormat

class PermissionDetailsModel():
    def __init__(self, id, permission_id, reason, return_time) -> None:
        self.id = id
        self.permission_id = permission_id
        self.reason = reason
        self.return_time = return_time

    def to_json(self):
        return {
            'id': self.id,
            'permission_id': self.permission_id,
            'reason': self.reason,
            'return_time': self.return_time,
        }


# class ViewAdditionalPermissionModel():
#     # permission_id, permission_date, start_time, return_time, reason, status, end_time, additional_reason, additional_time
#     def __init__(self, permission_id, permission_date, start_time, return_time, reason, status, end_time, additional_reason, additional_time) -> None:
#         self.permission_id = permission_id
#         self.permission_date = permission_date
#         self.start_time = start_time
#         self.return_time = return_time,
#         self.reason = reason,
#         self.status = status,
#         self.end_time = end_time,
#         self.additional_reason = additional_reason,
#         self.additional_time = additional_time,

#     def to_json(self):
#         return {
#             'permission_id': self.permission_id,
#             'permission_date' : DateFormat.convert_date(self.permission_date),
#             'start_time' : DateFormat.convert_time(self.start_time),
#             'return_time' : DateFormat.convert_time(self.return_time),
#             'reason' : self.reason,
#             'status' : self.status,
#             'end_time' : DateFormat.convert_time(self.end_time),
#             'additional_reason' : self.additional_reason,
#             'additional_time' : DateFormat.convert_time(self.additional_time),
#         }