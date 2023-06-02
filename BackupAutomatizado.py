import subprocess
import boto3

# Configurações de conexão com o banco de dados PostgreSQL
db_params = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "123",
    "container_name": "my-postgres"  # Nome do container Docker PostgreSQL
}

# Comando pg_dump para gerar o backup
command = f"docker exec {db_params['container_name']} pg_dump --dbname=postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']} > backup.sql"

# Executar o comando pg_dump dentro do contêiner Docker
result = subprocess.run(command, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    # Configuração do cliente do Amazon S3
    s3 = boto3.client("s3", aws_access_key_id="AKIAWPRVN7STBIHB4HXR", aws_secret_access_key="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")

    # Fazer upload do arquivo de backup para o S3
    bucket_name = "magabucket"
    backup_filename = "backup.sql"
    
    with open("backup.sql", "rb") as file:
        s3.upload_fileobj(file, bucket_name, backup_filename)

    print("Backup do banco de dados gerado e armazenado no Amazon S3 com sucesso!")
else:
    print("Ocorreu um erro ao gerar o backup do banco de dados.")

print("Validação: Verifique se o backup do banco de dados foi gerado e armazenado no Amazon S3.")