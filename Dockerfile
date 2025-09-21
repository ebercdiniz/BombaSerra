# Imagem base
FROM python:3.11-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de requirements
COPY requirements.txt /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do projeto
COPY . /app/

# Definir variável de ambiente para produção
ENV DJANGO_SETTINGS_MODULE=BombaSerra.settings
ENV PYTHONUNBUFFERED=1

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor a porta do Django
EXPOSE 8001

# Rodar o servidor Django
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8001", "BombaSerra.wsgi:application"]
