# Database
from src.database.db_postgres import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.AdditionalPermissionModel import AdditionalPermissionModel


class AdditionalPermissionService():

    @classmethod
    def get_permisssions(cls):
        try:
            connection = get_connection()
            additional_permissions = []
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, permission_id, reason, additional_time, created_at ROM public.additional_permissions')
                resultset = cursor.fetchall()
                for row in resultset:
                    # print('row', row)
                    additional_permission = AdditionalPermissionModel(
                        int(row[0]),
                        row[1],
                        row[2],
                        row[3],
                    )
                    additional_permissions.append(additional_permission.to_json())
            connection.close()
            return additional_permissions
        except Exception as e:
            Logger.add_to_log("error", str(e))
            # Logger.add_to_log("error", traceback.format_exc())