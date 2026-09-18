require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { ApolloServer } = require('@apollo/server');
const { expressMiddleware } = require('@apollo/server/express4');

const connectDB = require('./src/config/db');
const trabajadorRoutes = require('./src/routes/trabajador.routes');
const typeDefs = require('./src/graphql/typeDefs');
const resolvers = require('./src/graphql/resolvers');

const PORT = process.env.PORT || 4000;

async function startServer() {
  // 1. Conexion a MongoDB
  await connectDB();

  // 2. Instancia de Express
  const app = express();
  app.use(cors());
  app.use(bodyParser.json());

  // 3. Rutas REST
  app.use('/trabajador', trabajadorRoutes);

  // 4. Servidor Apollo (GraphQL) montado en la misma app Express
  const apolloServer = new ApolloServer({
    typeDefs,
    resolvers,
  });

  await apolloServer.start();

  app.use(
    '/graphql',
    cors(),
    bodyParser.json(),
    expressMiddleware(apolloServer)
  );

  // 5. Ruta raiz informativa
  app.get('/', (req, res) => {
    res.json({
      mensaje: 'API de Trabajadores activa',
      rest: '/trabajador',
      graphql: '/graphql',
    });
  });

  // 6. Manejo de rutas no encontradas
  app.use((req, res) => {
    res.status(404).json({ error: 'Ruta no encontrada' });
  });

  app.listen(PORT, () => {
    console.log(`Servidor corriendo en el puerto ${PORT}`);
    console.log(`REST disponible en:     http://localhost:${PORT}/trabajador`);
    console.log(`GraphQL disponible en:  http://localhost:${PORT}/graphql`);
  });
}

startServer().catch((err) => {
  console.error('Error al iniciar el servidor:', err);
  process.exit(1);
});
