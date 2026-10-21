const express = require("express");
const app = express();
const port = process.env.PORT || 3000;
const version = process.env.APP_VERSION || "1.0.0";

app.use(express.json());

let tareas = [
  { id: 1, titulo: "Configurar cluster k3d", completada: true, fecha: new Date().toISOString() },
  { id: 2, titulo: "Crear manifiestos de Kubernetes", completada: true, fecha: new Date().toISOString() },
  { id: 3, titulo: "Configurar Ingress y Service", completada: false, fecha: new Date().toISOString() },
  { id: 4, titulo: "Implementar GitOps con Argo CD", completada: false, fecha: new Date().toISOString() }
];

let dependenciaActiva = true;

// Endpoint raíz
app.get("/", (req, res) => {
  res.json({
    mensaje: "API de Tareas - Microservicios COM-600",
    version,
    entorno: process.env.APP_ENTORNO || "desarrollo",
    hostname: process.env.HOSTNAME || "localhost"
  });
});

// Endpoint /tareas
app.get("/tareas", (req, res) => {
  const limite = parseInt(process.env.APP_PAGINA_TAM || "20", 10);
  res.json({
    version,
    entorno: process.env.APP_ENTORNO || "default",
    total: tareas.length,
    limite,
    datos: tareas.slice(0, limite)
  });
});

app.post("/tareas", (req, res) => {
  const { titulo } = req.body;
  if (!titulo) {
    return res.status(400).json({ error: "El título es obligatorio" });
  }
  const nuevaTarea = {
    id: tareas.length + 1,
    titulo,
    completada: false,
    fecha: new Date().toISOString()
  };
  tareas.push(nuevaTarea);
  res.status(201).json(nuevaTarea);
});

// Endpoint /salud (para sondas del laboratorio)
app.get("/salud", (req, res) => {
  res.status(200).json({
    estado: "ok",
    version,
    tiempoActivo: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Sonda de Liveness (el proceso responde)
app.get("/salud/live", (req, res) => {
  res.status(200).json({ status: "alive", uptime: process.uptime() });
});

// Sonda de Readiness (verifica dependencias)
app.get("/salud/ready", (req, res) => {
  if (!dependenciaActiva) {
    return res.status(503).json({ status: "not_ready", error: "Dependencia fuera de servicio" });
  }
  res.status(200).json({ status: "ready", dependencia: "ok" });
});

// Control manual de dependencia para Ejercicio 2
app.post("/admin/dependencia", (req, res) => {
  const { estado } = req.query;
  if (estado === "down") {
    dependenciaActiva = false;
  } else {
    dependenciaActiva = true;
  }
  res.json({ dependenciaActiva });
});

app.listen(port, () => {
  console.log(`[tareas-api v${version}] corriendo en puerto ${port} (entorno: ${process.env.APP_ENTORNO || 'default'})`);
});
