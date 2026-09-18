const Trabajador = require('../models/Trabajador');

// Convierte una fecha a formato YYYY-MM-DD para exponerla como String
const formatearFecha = (fecha) => {
  if (!fecha) return null;
  const d = new Date(fecha);
  return d.toISOString().split('T')[0];
};

// Adapta el documento de Mongoose al tipo Trabajador de GraphQL
const formatearTrabajador = (trabajador) => ({
  id: trabajador._id.toString(),
  nombre: trabajador.nombre,
  apellido: trabajador.apellido,
  cedula: trabajador.cedula,
  cargo: trabajador.cargo,
  departamento: trabajador.departamento,
  fechaIngreso: formatearFecha(trabajador.fechaIngreso),
});

const resolvers = {
  Query: {
    obtenerTrabajadores: async () => {
      const trabajadores = await Trabajador.find();
      return trabajadores.map(formatearTrabajador);
    },

    obtenerTrabajador: async (_padre, { id }) => {
      const trabajador = await Trabajador.findById(id);
      if (!trabajador) {
        throw new Error('Trabajador no encontrado');
      }
      return formatearTrabajador(trabajador);
    },
  },

  Mutation: {
    crearTrabajador: async (_padre, args) => {
      try {
        const nuevoTrabajador = new Trabajador(args);
        const guardado = await nuevoTrabajador.save();
        return formatearTrabajador(guardado);
      } catch (error) {
        if (error.code === 11000) {
          throw new Error('Ya existe un trabajador registrado con esa cedula de identidad');
        }
        throw new Error(`Error al crear el trabajador: ${error.message}`);
      }
    },

    actualizarTrabajador: async (_padre, { id, ...datos }) => {
      try {
        const actualizado = await Trabajador.findByIdAndUpdate(id, datos, {
          new: true,
          runValidators: true,
        });

        if (!actualizado) {
          throw new Error('Trabajador no encontrado');
        }

        return formatearTrabajador(actualizado);
      } catch (error) {
        if (error.code === 11000) {
          throw new Error('Ya existe un trabajador registrado con esa cedula de identidad');
        }
        throw new Error(`Error al actualizar el trabajador: ${error.message}`);
      }
    },

    eliminarTrabajador: async (_padre, { id }) => {
      const eliminado = await Trabajador.findByIdAndDelete(id);
      if (!eliminado) {
        throw new Error('Trabajador no encontrado');
      }
      return formatearTrabajador(eliminado);
    },
  },
};

module.exports = resolvers;
