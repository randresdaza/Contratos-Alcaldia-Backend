from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from authApp.permissions import check_role


class ReporteView(APIView):
    permission_classes = (IsAuthenticated,)

    @check_role(['Administrador', 'Supervisor'])
    def get(self, request):
        from_date = request.query_params.get('fromDate')
        to_date = request.query_params.get('toDate')

        if from_date and to_date:
            # Ejecutar la consulta SQL con el rango de fechas
            with connection.cursor() as cursor:
                cursor.execute(f"""
                            WITH Documentos AS (
                                SELECT
                                    r.fecha,
                                    r.usuario_id,
                                    u.username,
                                    u.name,
                                    COUNT(*) AS nro_documentos
                                FROM
                                    public."authApp_reporte" r
                                INNER JOIN
                                    public."authApp_user" u ON r.usuario_id = u.id
                                WHERE
                                    r.documento_id IS NOT NULL
                                    AND r.fecha >= '{from_date}' AND r.fecha <= '{to_date}'
                                GROUP BY
                                    r.fecha, r.usuario_id, u.username, u.name
                                ORDER BY r.fecha DESC
                            ),
                            Contratos AS (
                                SELECT
                                    r.fecha,
                                    r.usuario_id,
                                    u.username,
                                    u.name,
                                    COUNT(*) AS nro_contratos
                                FROM
                                    public."authApp_reporte" r
                                INNER JOIN
                                    public."authApp_user" u ON r.usuario_id = u.id
                                WHERE
                                    r.contrato_id IS NOT NULL
                                    AND r.fecha >= '{from_date}' AND r.fecha <= '{to_date}'
                                GROUP BY
                                    r.fecha, r.usuario_id, u.username, u.name
                                ORDER BY r.fecha DESC
                            )
                            SELECT
                                COALESCE(d.fecha, c.fecha) AS fecha,
                                COALESCE(d.usuario_id, c.usuario_id) AS usuario_id,
                                COALESCE(d.username, c.username) AS username,
                                COALESCE(d.name, c.name) AS name,
                                COALESCE(c.nro_contratos, 0) AS nro_contratos,                                
                                COALESCE(d.nro_documentos, 0) AS nro_documentos
                            FROM
                                Documentos d
                            FULL JOIN
                                Contratos c ON d.fecha = c.fecha AND d.usuario_id = c.usuario_id
                """)

                # Obtener los resultados de la consulta
                results = cursor.fetchall()

                # Serializar los resultados
                serialized_results = [
                    {'fecha': row[0], 'usuario_id': row[1], 'username': row[2], 'name': row[3],
                     'nro_contratos': row[4],
                     'nro_documentos': row[5]} for row in results]
                return Response(serialized_results, status=status.HTTP_200_OK)
        else:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    WITH Documentos AS (
                        SELECT
                            r.fecha,
                            r.usuario_id,
                            u.username,
                            u.name,
                            COUNT(*) AS nro_documentos
                        FROM
                            public."authApp_reporte" r
                        INNER JOIN
                            public."authApp_user" u ON r.usuario_id = u.id
                        WHERE
                            r.documento_id IS NOT NULL
                        GROUP BY
                            r.fecha, r.usuario_id, u.username, u.name
                        ORDER BY r.fecha DESC
                    ),
                    Contratos AS (
                        SELECT
                            r.fecha,
                            r.usuario_id,
                            u.username,
                            u.name,
                            COUNT(*) AS nro_contratos
                        FROM
                            public."authApp_reporte" r
                        INNER JOIN
                            public."authApp_user" u ON r.usuario_id = u.id
                        WHERE
                            r.contrato_id IS NOT NULL
                        GROUP BY
                            r.fecha, r.usuario_id, u.username, u.name
                        ORDER BY r.fecha DESC
                    )
                    SELECT
                        COALESCE(d.fecha, c.fecha) AS fecha,
                        COALESCE(d.usuario_id, c.usuario_id) AS usuario_id,
                        COALESCE(d.username, c.username) AS username,
                        COALESCE(d.name, c.name) AS name,
                        COALESCE(c.nro_contratos, 0) AS nro_contratos,
                        COALESCE(d.nro_documentos, 0) AS nro_documentos
                    FROM
                        Documentos d
                    FULL JOIN
                        Contratos c ON d.fecha = c.fecha AND d.usuario_id = c.usuario_id
                """)

                # Obtener los resultados de la consulta
                results = cursor.fetchall()

                # Serializar los resultados
                serialized_results = [{'fecha': row[0], 'usuario_id': row[1], 'username': row[2], 'name': row[3],
                                       'nro_contratos': row[4], 'nro_documentos': row[5]} for row in results]
                return Response(serialized_results, status=status.HTTP_200_OK)
