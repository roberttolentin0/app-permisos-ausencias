import traceback
from datetime import datetime
# Database
from src.database.db_postgres import PGConnection
# Logger
from src.utils.Logger import Logger
from src.utils.DateFormat import DateFormat
# Models
from src.models.PermissionDetailsModel import PermissionDetailsModel
# from src.models.AdditionalPermissionModel import ViewAdditionalPermissionModel

connectionDB = PGConnection()

class PermissionDetailsService():

    @classmethod
    def get_last_details_by_permission_id(cls, permission_id):
        try:
            connection = connectionDB.connect()
            additional_permission = None
            with connection.cursor() as cursor:
                query = f"""
                            SELECT id, permission_id, reason, return_time
                            FROM public.permission_details
                            WHERE permission_id = {permission_id}  ORDER BY id desc LIMIT 1
                        """
                cursor.execute(query)
                resultset = cursor.fetchall()
                for row in resultset:
                    print('row', row)
                    additional_permission = PermissionDetailsModel(
                        int(row[0]),
                        int(row[1]),
                        row[2],
                        DateFormat.convert_time(row[3]),
                    )
            connection.close()
            return additional_permission.to_json()
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def get_details_by_permission_id(cls, permission_id):
        try:
            connection = connectionDB.connect()
            details_permissions = []
            with connection.cursor() as cursor:
                query = f"""
                            SELECT id, permission_id, reason, return_time
                            FROM public.permission_details
                            WHERE permission_id = {permission_id}  ORDER BY id desc
                        """
                cursor.execute(query)
                resultset = cursor.fetchall()
                for row in resultset:
                    print('row', row)
                    additional_permission = PermissionDetailsModel(
                        int(row[0]),
                        int(row[1]),
                        row[2],
                        DateFormat.convert_time(row[3]),
                    )
                    details_permissions.append(additional_permission.to_json())
            connection.close()
            return details_permissions
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def create_permission_detail(cls, permission_detail):
        print('create_permission_detail', permission_detail.to_json())
        try:
            connection = connectionDB.connect()
            with connection.cursor() as cursor:
                new_return_time= datetime.strptime(permission_detail.return_time, "%H:%M").time()
                cursor.execute("""INSERT INTO public.permission_details
                                (permission_id, reason, return_time, created_at)
                                VALUES (%s, %s, %s, %s)""",
                                (permission_detail.permission_id,
                                 permission_detail.reason,
                                 new_return_time,
                                 datetime.now()))
                affected_rows = cursor.rowcount
                connection.commit()
            connectionDB.close()
            return affected_rows
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())