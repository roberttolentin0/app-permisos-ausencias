# Database
from src.database.db_postgres import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.PermissionModel import Permission


class PermissionService():

    @classmethod
    def get_permisssions(cls):
        try:
            connection = get_connection()
            permissions = []
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, dni, permission_date, start_time, end_time, reason, status, observation, validator_id, create_at, update_at FROM public.permissions')
                resultset = cursor.fetchall()
                for row in resultset:
                    # print('row', row)
                    permission = Permission(
                        int(row[0]),
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8]
                    )
                    permissions.append(permission.to_json())
            connection.close()
            return permissions
        except Exception as e:
            Logger.add_to_log("error", str(e))
            # Logger.add_to_log("error", traceback.format_exc())