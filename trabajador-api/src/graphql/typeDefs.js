const typeDefs = `#graphql
  type Trabajador {
    id: ID!
    nombre: String!
    apellido: String!
    cedula: String!
    cargo: String!
    departamento: String!
    fechaIngreso: String!
  }

  type MensajeEliminacion {
    mensaje: String!
    trabajador: Trabajador
  }

  type Query {
    obtenerTrabajadores: [Trabajador!]!
    obtenerTrabajador(id: ID!): Trabajador
  }

  type Mutation {
    crearTrabajador(
      nombre: String!
      apellido: String!
      cedula: String!
      cargo: String!
      departamento: String!
      fechaIngreso: String!
    ): Trabajador!

    actualizarTrabajador(
      id: ID!
      nombre: String
      apellido: String
      cedula: String
      cargo: String
      departamento: String
      fechaIngreso: String
    ): Trabajador!

    eliminarTrabajador(id: ID!): Trabajador!
  }
`;

module.exports = typeDefs;
