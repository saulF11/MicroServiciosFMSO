FROM node:20-alpine

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero los manifiestos para aprovechar la cache de Docker
COPY package*.json ./

RUN npm install --production

# Copiamos el resto del codigo fuente
COPY . .

# Puerto en el que escucha la app (debe coincidir con PORT)
EXPOSE 4000

CMD ["node", "server.js"]
