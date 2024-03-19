import traceback
from datetime import datetime
# Database
from src.database.db_postgres import PGConnection
from src.utils.Logger import Logger
from src.utils.DateFormat import DateFormat
# Models
from src.models.PermissionModel import Permission

connectionDB = PGConnection()


class PermissionService():

    @classmethod
    def get_permisssions(cls):
        try:
            connection = connectionDB.connect()
            permissions = []
            with connection.cursor() as cursor:
                query = """
                            SELECT id, dni, permission_date, start_time, return_time, reason, status, observation, validator_id, created_at, updated_at, end_time
                            FROM public.permissions p
                        """
                cursor.execute(query)
                resultset = cursor.fetchall()
                for row in resultset:
                    # print('row', row)
                    end_time = DateFormat.convert_time(row[11]) if row[11] is not None else '00:00'
                    permission = Permission(
                        int(row[0]),
                        row[1],
                        DateFormat.convert_date(row[2]),
                        DateFormat.convert_time(row[3]),
                        DateFormat.convert_time(row[4]),
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        end_time,
                    )
                    permissions.append(permission.to_json())
            connectionDB.close()
            return permissions
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def get_permisssion(cls, id):
        try:
            connection = connectionDB.connect()
            permission = None
            with connection.cursor() as cursor:
                query = f"""
                            SELECT id, dni, permission_date, start_time, end_time, reason, status, observation, validator_id, created_at, updated_at
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
            connectionDB.close()
            return permission.to_json()
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def get_permisssion_by_dni(cls, dni):
        try:
            connection = connectionDB.connect()
            permission = []
            with connection.cursor() as cursor:
                query = f"""
                            SELECT id, dni, permission_date, start_time, return_time, reason, status, observation, validator_id, created_at, updated_at, end_time
                            FROM fun_get_last_permission_by_dni('{dni}');
                        """
                cursor.execute(query)
                resultset = cursor.fetchall()
                for row in resultset:
                    print('row', row)
                    end_time = DateFormat.convert_time(row[9]) if row[9] is not None else '00:00'
                    permission = Permission(
                        int(row[0]),
                        row[1],
                        DateFormat.convert_date(row[2]),
                        DateFormat.convert_time(row[3]),
                        DateFormat.convert_time(row[4]),
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        end_time,
                    )
            connectionDB.close()
            return permission.to_json()
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def create_permission(cls, permission):
        print('create_permission', permission.to_json())
        try:
            connection = connectionDB.connect()
            with connection.cursor() as cursor:
                start_time= datetime.strptime(permission.start_time, "%H:%M").time()
                return_time= datetime.strptime(permission.return_time, "%H:%M").time()
                cursor.execute("""INSERT INTO permissions
                                (dni, permission_date, start_time, return_time, reason, status, observation, validator_id, created_at)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (permission.dni,
                                 permission.permission_date,
                                 start_time,
                                 return_time,
                                 permission.reason,
                                 permission.status,
                                 permission.observation,
                                 permission.validator_id,
                                 datetime.now()))
                affected_rows = cursor.rowcount
                connection.commit()
            connectionDB.close()
            return affected_rows
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def update_status_permission(cls, id, status, observation = None):
        print('accept_permission')
        try:
            connection = connectionDB.connect()
            with connection.cursor() as cursor:
                if observation is not None:
                    print('rechazar')
                    cursor.execute("""UPDATE public.permissions
                                        SET status=%s, observation=%s, validator_id='1', updated_at=%s
                                        WHERE id = %s;
                                """,(status, observation, datetime.now(), id))
                else:
                    print('aceptar')
                    cursor.execute("""UPDATE public.permissions
                                    SET status=%s, validator_id='1', updated_at=%s
                                    WHERE id = %s;
                                """,(status, datetime.now(), id))

                affected_rows = cursor.rowcount
                connection.commit()
            connectionDB.close()
            return affected_rows
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def end_time_permission(cls, id):
        print('end_permission')
        try:
            connection = connectionDB.connect()
            curr_time = datetime.now().strftime("%H:%M:%S")
            with connection.cursor() as cursor:
                print('Finalizar')
                cursor.execute("""UPDATE public.permissions
                                        SET status='FINALIZADO', end_time=%s, validator_id='1', updated_at=%s
                                        WHERE id = %s;
                                """,(curr_time, datetime.now(), id))
                affected_rows = cursor.rowcount
                connection.commit()
            connectionDB.close()
            return affected_rows
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())