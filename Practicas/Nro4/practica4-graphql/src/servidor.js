const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');
const pool = require('./db');

const typeDefs = `#graphql
  type DetalleVenta {
    id: ID!
    producto: String!
    cantidad: Int!
    precioUnitario: Float!
  }

  type Venta {
    id: ID!
    clienteId: Int!
    fecha: String!
    total: Float!
    detalle: [DetalleVenta!]!
  }

  type Query {
    ventas: [Venta!]!
    venta(id: Int!): Venta
  }
`;

const resolvers = {
  Query: {
    ventas: async () => {
      const [filas] = await pool.query('SELECT id, cliente_id AS clienteId, fecha, total FROM ventas');
      return filas;
    },
    venta: async (_, { id }) => {
      const [filas] = await pool.query('SELECT id, cliente_id AS clienteId, fecha, total FROM ventas WHERE id = ?', [id]);
      return filas[0] || null;
    }
  },
  Venta: {
    detalle: async (padre) => {
      console.log(`[SQL Log] Consultando detalle para venta ID: ${padre.id}`);
      const [filas] = await pool.query(
        'SELECT id, producto, cantidad, precio_unitario AS precioUnitario FROM detalle_venta WHERE venta_id = ?',
        [padre.id]
      );
      return filas;
    }
  }
};

async function iniciarServidor() {
  const server = new ApolloServer({ typeDefs, resolvers });
  const { url } = await startStandaloneServer(server, { listen: { port: 4005 } });
  console.log(`Servidor GraphQL listo en ${url}`);
}

iniciarServidor();
