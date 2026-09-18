const express = require('express');
const app = express();

const usuarios = [
  { id: 1, nombre: "Saul Flores", email: "saul@example.com" },
  { id: 2, nombre: "Ana Gomez", email: "ana@example.com" }
];

app.get('/usuarios', (req, res) => res.json(usuarios));
app.get('/usuarios/:id', (req, res) => {
  const u = usuarios.find(user => user.id === parseInt(req.params.id));
  if (!u) return res.status(404).json({ error: "Usuario no encontrado" });
  res.json(u);
});

app.listen(3000, () => console.log('Servicio REST escuchando en http://localhost:3000'));
