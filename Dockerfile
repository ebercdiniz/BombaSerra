# Imagem base
FROM python:3.9

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de requirements
COPY requirements.txt /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do projeto
COPY . /app/

# Expor a porta do Django
EXPOSE 8001

# Rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]