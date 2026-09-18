const express = require('express');
const router = express.Router();

const {
  obtenerTrabajadores,
  obtenerTrabajadorPorId,
  crearTrabajador,
  actualizarTrabajador,
  eliminarTrabajador,
} = require('../controllers/trabajador.controller');

// GET /trabajador
router.get('/', obtenerTrabajadores);

// GET /trabajador/:id (extra, util para pruebas)
router.get('/:id', obtenerTrabajadorPorId);

// POST /trabajador
router.post('/', crearTrabajador);

// PUT /trabajador/:id
router.put('/:id', actualizarTrabajador);

// DELETE /trabajador/:id
router.delete('/:id', eliminarTrabajador);

module.exports = router;
