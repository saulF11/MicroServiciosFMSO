const Trabajador = require('../models/Trabajador');

// GET /trabajador -> Obtener todos los trabajadores
exports.obtenerTrabajadores = async (req, res) => {
  try {
    const trabajadores = await Trabajador.find();
    res.status(200).json(trabajadores);
  } catch (error) {
    res.status(500).json({
      error: 'Error al obtener los trabajadores',
      detalle: error.message,
    });
  }
};

// GET /trabajador/:id -> Obtener un trabajador por id
exports.obtenerTrabajadorPorId = async (req, res) => {
  try {
    const trabajador = await Trabajador.findById(req.params.id);

    if (!trabajador) {
      return res.status(404).json({ error: 'Trabajador no encontrado' });
    }

    res.status(200).json(trabajador);
  } catch (error) {
    res.status(500).json({
      error: 'Error al obtener el trabajador',
      detalle: error.message,
    });
  }
};

// POST /trabajador -> Crear un nuevo trabajador
exports.crearTrabajador = async (req, res) => {
  try {
    const { nombre, apellido, cedula, cargo, departamento, fechaIngreso } = req.body;

    if (!nombre || !apellido || !cedula || !cargo || !departamento || !fechaIngreso) {
      return res.status(400).json({
        error: 'Todos los campos son obligatorios: nombre, apellido, cedula, cargo, departamento, fechaIngreso',
      });
    }

    const nuevoTrabajador = new Trabajador({
      nombre,
      apellido,
      cedula,
      cargo,
      departamento,
      fechaIngreso,
    });

    const trabajadorGuardado = await nuevoTrabajador.save();
    res.status(201).json(trabajadorGuardado);
  } catch (error) {
    if (error.code === 11000) {
      return res.status(409).json({
        error: 'Ya existe un trabajador registrado con esa cedula de identidad',
      });
    }
    res.status(500).json({
      error: 'Error al crear el trabajador',
      detalle: error.message,
    });
  }
};

// PUT /trabajador/:id -> Actualizar un trabajador existente
exports.actualizarTrabajador = async (req, res) => {
  try {
    const { id } = req.params;
    const datosActualizados = req.body;

    const trabajadorActualizado = await Trabajador.findByIdAndUpdate(
      id,
      datosActualizados,
      {
        new: true,
        runValidators: true,
      }
    );

    if (!trabajadorActualizado) {
      return res.status(404).json({ error: 'Trabajador no encontrado' });
    }

    res.status(200).json(trabajadorActualizado);
  } catch (error) {
    if (error.code === 11000) {
      return res.status(409).json({
        error: 'Ya existe un trabajador registrado con esa cedula de identidad',
      });
    }
    res.status(500).json({
      error: 'Error al actualizar el trabajador',
      detalle: error.message,
    });
  }
};

// DELETE /trabajador/:id -> Eliminar un trabajador
exports.eliminarTrabajador = async (req, res) => {
  try {
    const { id } = req.params;
    const trabajadorEliminado = await Trabajador.findByIdAndDelete(id);

    if (!trabajadorEliminado) {
      return res.status(404).json({ error: 'Trabajador no encontrado' });
    }

    res.status(200).json({
      mensaje: 'Trabajador eliminado correctamente',
      trabajador: trabajadorEliminado,
    });
  } catch (error) {
    res.status(500).json({
      error: 'Error al eliminar el trabajador',
      detalle: error.message,
    });
  }
};
