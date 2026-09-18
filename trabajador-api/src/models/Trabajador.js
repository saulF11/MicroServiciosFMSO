const mongoose = require('mongoose');

const trabajadorSchema = new mongoose.Schema(
  {
    nombre: {
      type: String,
      required: [true, 'El nombre es obligatorio'],
      trim: true,
    },
    apellido: {
      type: String,
      required: [true, 'El apellido es obligatorio'],
      trim: true,
    },
    cedula: {
      type: String,
      required: [true, 'La cedula de identidad es obligatoria'],
      unique: true,
      trim: true,
    },
    cargo: {
      type: String,
      required: [true, 'El cargo es obligatorio'],
      trim: true,
    },
    departamento: {
      type: String,
      required: [true, 'El departamento es obligatorio'],
      trim: true,
    },
    fechaIngreso: {
      type: Date,
      required: [true, 'La fecha de ingreso es obligatoria'],
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model('Trabajador', trabajadorSchema);
