# Práctica 9: Despliegue en Kubernetes con Helm y GitOps

**Asignatura:** COM-600 Microservicios  
**Estudiante:** Flores Mosquera Saul Osvaldo  
**Código Universitario:** 35-5854  
**Carrera:** Ing. de Sistemas  
**Universidad:** Universidad Mayor, Real y Pontificia de San Francisco Xavier de Chuquisaca  
**Repositorio:** [https://github.com/saulF11/MicroServiciosFMSO.git](https://github.com/saulF11/MicroServiciosFMSO.git)

---

## 1. Arquitectura y Componentes

Esta práctica implementa el ciclo completo de entrega continua y GitOps para el microservicio `tareas-api`:
- **Clúster Kubernetes local:** Creado con `k3d` (k3s en contenedores Docker) con 1 nodo control-plane y 2 nodos de trabajo (agentes), exponiendo el puerto 80 del balanceador hacia el puerto 8080 del host.
- **Microservicio Node.js / Express:** Expone endpoints REST (`/tareas`), sondas de salud (`/salud`, `/salud/ready`, `/salud/live`) y lee variables de entorno desacopladas.
- **Manifiestos Declarativos (`k8s/`):** `Deployment`, `Service`, `Ingress` (Traefik) y `ConfigMap`.
- **Empaquetamiento Helm (`chart/`):** Plantillas parametrizadas con perfiles de configuración `values.yaml` y `values-prod.yaml`.
- **Flujo GitOps con Argo CD (`argocd/`):** Control de estado deseado con sincronización automática (`automated: { prune: true, selfHeal: true }`).

---

## 2. Requisitos Previos

- Linux (Fedora 42/44 x86_64) con Docker Engine 24+
- `k3d` v5.6+
- `kubectl` v1.29+
- `helm` v3.14+
- Acceso a Internet y repositorio Git

---

## 3. Instrucciones de Despliegue desde Cero (Reproducibilidad)

### Paso 1: Crear el Clúster Local
```bash
k3d cluster create com600 --agents 2 -p "8080:80@loadbalancer"
kubectl config use-context k3d-com600
kubectl get nodes -o wide
```

### Paso 2: Construir e Importar las Imágenes del Servicio
```bash
docker build -t ghcr.io/saulf11/tareas-api:1.0.0 ./app
docker build -t ghcr.io/saulf11/tareas-api:2.0.0 -f - ./app << 'EOF'
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
ENV APP_VERSION=2.0.0
EXPOSE 3000
CMD ["node", "server.js"]
EOF

# Importar imágenes locales al clúster k3d
k3d image import ghcr.io/saulf11/tareas-api:1.0.0 ghcr.io/saulf11/tareas-api:2.0.0 -c com600
```

### Paso 3: Despliegue Declarativo con Kubectl
```bash
# Crear el secreto requerido
kubectl create secret generic tareas-secret --from-literal=APP_CLAVE_API=clave-de-laboratorio-2026

# Aplicar todos los manifiestos
kubectl apply -f k8s/

# Probar acceso externo vía Ingress
curl -i http://tareas.localhost:8080/tareas
```

### Paso 4: Despliegue con Helm
```bash
# Limpiar manifiestos base
kubectl delete -f k8s/

# Instalar entorno base (laboratorio)
helm install tareas ./chart

# Instalar entorno de producción en paralelo
helm install tareas-prod ./chart -f chart/values-prod.yaml

# Verificar releases
helm list
```

### Paso 5: Despliegue GitOps con Argo CD
```bash
# Instalar Argo CD
kubectl create namespace argocd
kubectl apply --server-side --force-conflicts -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Obtener clave inicial del administrador
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

# Desplegar la Application de Argo CD
kubectl apply -f argocd/application.yaml

# Comprobar sincronización
kubectl -n argocd get application tareas
```

---

## 4. Estructura de Directorios

```
practica9-kubernetes/
├── app/
│   ├── Dockerfile
│   ├── package.json
│   └── server.js
├── argocd/
│   └── application.yaml
├── chart/
│   ├── Chart.yaml
│   ├── templates/
│   │   ├── deployment.yaml
│   │   ├── ingress.yaml
│   │   └── service.yaml
│   ├── values.yaml
│   └── values-prod.yaml
├── evidencias/
│   ├── captura_01.png ... captura_20.png
├── k8s/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── ingress.yaml
│   └── service.yaml
└── README.md
```
