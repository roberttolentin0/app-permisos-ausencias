import traceback
from datetime import time
from datetime import datetime
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
                query = """
                            SELECT id, dni, permission_date, start_time, end_time, reason, status, observation, validator_id, created_at, updated_at
                            FROM public.permissions p
                        """
                cursor.execute(query)
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

    @classmethod
    def get_permisssion(cls, id):
        try:
            connection = get_connection()
            permission = None
            with connection.cursor() as cursor:
                query = f"""
                            SELECT id, dni, permission_date, start_time, end_time, reason, status, observation, validator_id, create_at, update_at
                            FROM public.permissions p
                            WHERE id = {id}
                        """
                cursor.execute(query)
                resultset = cursor.fetchall()
                for row in resultset:
                    print('row', row)
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
            connection.close()
            return permission.to_json()
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def create_permission(cls, permission):
        print('create_permission', permission.to_json())
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                start_time= datetime.strptime(permission.start_time, "%H:%M").time()
                end_time= datetime.strptime(permission.end_time, "%H:%M").time()
                cursor.execute("""INSERT INTO permissions
                                (dni, permission_date, start_time, end_time, reason, status, observation, validator_id, created_at)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (permission.dni,
                                 permission.permission_date,
                                 start_time,
                                 end_time,
                                 permission.reason,
                                 permission.status, permission.observation, permission.validator_id, datetime.now()))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())