# Usar uma imagem Python leve
FROM python:3.10-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar o código para dentro da imagem
COPY . /app

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta do Flask
EXPOSE 5000

# Comando para rodar o servidor
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server.server:app"]
