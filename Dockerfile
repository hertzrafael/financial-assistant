FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto (excluindo o que está no .dockerignore)
COPY . .

#RUN chmod +x ./entrypoint.sh

# Expõe a porta que a aplicação vai utilizar
EXPOSE 8000

#ENTRYPOINT ["/app/entrypoint.sh"]

# Comando para rodar a aplicação em produção
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers"]
