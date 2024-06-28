from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import paramiko
import PyPDF2
from authApp.models import Servidor
from authApp.permissions import check_role


class SFTPFileList(APIView):
    permission_classes = (IsAuthenticated,)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def get(self, request):
        directory = request.query_params.get('route')

        if directory:
            # Configura la conexión SFTP
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.0.220', 8040, 'rafael_upc', 'rafael0321')

            sftp = ssh.open_sftp()

            # Verificar si el directorio existe
            try:
                sftp.listdir(directory)
                response = Response({'detail': f'La ruta {directory} es valida en el servidor.'},
                                    status=status.HTTP_200_OK)
            except FileNotFoundError:
                response = Response({'detail': f'No existe la ruta {directory} en el servidor.'},
                                    status=status.HTTP_202_ACCEPTED)

            sftp.close()
            ssh.close()
            return response
        else:
            try:
                # Configura la conexión SFTP
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect('192.168.0.220', 8040, 'rafael_upc', 'rafael0321')

                sftp = ssh.open_sftp()

                file_name = request.query_params.get('fileName')

                servidor = Servidor.objects.first()
                if not servidor:
                    return Response({'error': 'No se encontró una ruta en la base de datos'},
                                    status=status.HTTP_404_NOT_FOUND)

                # Cambia al directorio deseado en el servidor SFTP
                # sftp.chdir('/home/rafael/Documents/Files/')

                remote_directory = servidor.ruta

                sftp.chdir(remote_directory)

                # Abre el archivo en modo binario
                remote_file = sftp.open(file_name, 'rb')

                # Lee el contenido del archivo en binario
                file_content = remote_file.read()
                remote_file.close()

                # Cierra la conexión SFTP
                sftp.close()

                # Establece la respuesta HTTP con el contenido del archivo PDF
                response = HttpResponse(file_content, content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="{file_name}"'
                return response
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @check_role(['Administrador', 'Supervisor', 'Digitador'])
    def post(self, request):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.0.220', 8040, 'rafael_upc', 'rafael0321')

            sftp = ssh.open_sftp()

            # Obtén el archivo del formulario
            uploaded_file = request.FILES['file']

            servidor = Servidor.objects.first()
            if not servidor:
                return Response({'error': 'No se encontró una ruta en la base de datos'},
                                status=status.HTTP_404_NOT_FOUND)

            # Directorio donde se guardarán los archivos
            # remote_directory = '/home/rafael/Documents/Files/'

            remote_directory = servidor.ruta

            # Verificar si el directorio existe, si no, crearlo
            try:
                sftp.listdir(remote_directory)
            except FileNotFoundError:
                sftp.mkdir(remote_directory)

            # Verificar si el archivo ya existe en el directorio FTP
            file_exists = False
            remote_files = sftp.listdir(remote_directory)
            if uploaded_file.name in remote_files:
                file_exists = True

            if file_exists:
                sftp.close()
                return Response({'existing': True}, status=status.HTTP_200_OK)
            else:
                # Guardar el archivo en el servidor SFTP
                remote_pdf_path = remote_directory + uploaded_file.name
                with sftp.file(remote_pdf_path, 'wb') as remote_file:
                    for chunk in uploaded_file.chunks():
                        remote_file.write(chunk)

                # Obtener el número de páginas si es un PDF
                if uploaded_file.name.lower().endswith('.pdf'):
                    with sftp.open(remote_pdf_path, 'rb') as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        num_pages = len(pdf_reader.pages)
                        # file_stats = sftp.stat(remote_pdf_path)
                        # file_size = file_stats.st_size
                        # print('Peso en bytes: ',file_size)
                    sftp.close()
                    return Response({'name': uploaded_file.name, 'pages': num_pages}, status=status.HTTP_201_CREATED)
                else:
                    sftp.close()
                    return Response({'message': 'El archivo no es un PDF'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
