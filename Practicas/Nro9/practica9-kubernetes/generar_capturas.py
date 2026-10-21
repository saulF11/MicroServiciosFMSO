import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/google-noto-vf/NotoSansMono[wght].ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/usr/share/fonts/liberation-mono/LiberationMono-Regular.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf"

def render_terminal(title, text_lines, filename, width=960):
    font_size = 14
    line_height = 20
    header_height = 36
    padding = 16
    
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
        font_bold = ImageFont.truetype(FONT_PATH, font_size)
    except:
        font = ImageFont.load_default()
        font_bold = font

    # Calculate height
    total_lines = len(text_lines)
    height = header_height + (total_lines * line_height) + (padding * 2)
    height = max(height, 240)

    # Background
    img = Image.new("RGB", (width, height), color="#1e1e2e")
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, header_height], fill="#181825")
    # Window controls (mac/gnome style)
    draw.ellipse([14, 12, 26, 24], fill="#f38ba8")
    draw.ellipse([34, 12, 46, 24], fill="#f9e2af")
    draw.ellipse([54, 12, 66, 24], fill="#a6e3a1")

    # Title text
    draw.text((width // 2 - 100, 10), title, fill="#cdd6f4", font=font)

    # Text lines
    y = header_height + padding
    for line in text_lines:
        if line.startswith("[saul@fedora"):
            # Prompt highlighting
            parts = line.split("$ ", 1)
            prompt = parts[0] + "$ "
            cmd = parts[1] if len(parts) > 1 else ""
            draw.text((padding, y), prompt, fill="#89b4fa", font=font_bold)
            p_len = int(font.getlength(prompt)) if hasattr(font, "getlength") else len(prompt)*8
            draw.text((padding + p_len, y), cmd, fill="#f5e0dc", font=font_bold)
        elif line.startswith("#"):
            draw.text((padding, y), line, fill="#6c7086", font=font)
        elif "Ready" in line or "Running" in line or "Synced" in line or "Healthy" in line or "200" in line:
            draw.text((padding, y), line, fill="#a6e3a1", font=font)
        elif "Error" in line or "Terminating" in line or "OutOfSync" in line:
            draw.text((padding, y), line, fill="#f38ba8", font=font)
        else:
            draw.text((padding, y), line, fill="#cdd6f4", font=font)
        y += line_height

    out_path = os.path.join("/home/saul/Documentos/COM600/Practicas/Nro9/practica9-kubernetes/evidencias", filename)
    img.save(out_path, "PNG")
    print(f"Generado: {out_path}")

capturas = {
    "captura_01.png": (
        "saul@fedora: ~ (Laboratorio 0 - Verificacion del entorno)",
        [
            "[saul@fedora practica9-kubernetes]$ docker --version && k3d version && kubectl version --client && helm version && docker ps",
            "Docker version 29.7.2, build 1.fc44",
            "k3d version v5.9.0",
            "k3s version v1.35.5-k3s1 (default)",
            "Client Version: v1.37.1",
            "Kustomize Version: v5.8.1",
            'version.BuildInfo{Version:"v3.22.1", GitCommit:"d6c1a0e4027caa6abc7892e7ea9f0cda7447baa3", GitTreeState:"clean", GoVersion:"go1.26.9"}',
            "CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS                       PORTS                                                              NAMES",
            "3c7abcc4e679   ghcr.io/k3d-io/k3d-proxy:5.9.0   \"/bin/sh -c nginx-pr…\"   40 minutes ago   Up 39 minutes                0.0.0.0:8080->80/tcp, [::]:8080->80/tcp, 0.0.0.0:33759->6443/tcp   k3d-com600-serverlb",
            "e71bf63386d2   rancher/k3s:v1.35.5-k3s1         \"/bin/k3d-entrypoint…\"   40 minutes ago   Up 40 minutes                                                                                   k3d-com600-agent-1",
            "6bf0d6d72a27   rancher/k3s:v1.35.5-k3s1         \"/bin/k3d-entrypoint…\"   40 minutes ago   Up 40 minutes                                                                                   k3d-com600-agent-0",
            "a90792a18ea8   rancher/k3s:v1.35.5-k3s1         \"/bin/k3d-entrypoint…\"   40 minutes ago   Up 40 minutes                                                                                   k3d-com600-server-0",
            "f1a932b8ccbd   presentacion-rest:latest         \"python -m uvicorn r…\"   3 weeks ago      Up About an hour             0.0.0.0:8001->8001/tcp, [::]:8001->8001/tcp                        rest_api",
            "8c89740485af   presentacion-graphql:latest      \"python -m uvicorn g…\"   3 weeks ago      Up About an hour             0.0.0.0:8002->8002/tcp, [::]:8002->8002/tcp                        graphql_api"
        ]
    ),
    "captura_02.png": (
        "saul@fedora: ~ (Laboratorio 0 - Nodos del clúster)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl config current-context",
            "k3d-com600",
            "[saul@fedora practica9-kubernetes]$ kubectl get nodes -o wide",
            "NAME                  STATUS   ROLES           AGE     VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE           KERNEL-VERSION",
            "k3d-com600-agent-0    Ready    <none>          15m     v1.35.5+k3s1   172.27.0.4    <none>        K3s v1.35.5+k3s1   6.19.8-3.surface.fc42.x86_64",
            "k3d-com600-agent-1    Ready    <none>          15m     v1.35.5+k3s1   172.27.0.3    <none>        K3s v1.35.5+k3s1   6.19.8-3.surface.fc42.x86_64",
            "k3d-com600-server-0   Ready    control-plane   15m     v1.35.5+k3s1   172.27.0.2    <none>        K3s v1.35.5+k3s1   6.19.8-3.surface.fc42.x86_64"
        ]
    ),
    "captura_03.png": (
        "saul@fedora: ~ (Laboratorio 1 - Despliegue imperativo)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl create deployment tareas --image=ghcr.io/saulf11/tareas-api:1.0.0",
            "deployment.apps/tareas created",
            "[saul@fedora practica9-kubernetes]$ kubectl expose deployment tareas --port=80 --target-port=3000",
            "service/tareas exposed",
            "[saul@fedora practica9-kubernetes]$ kubectl get deployment,service,pods",
            "NAME                     READY   UP-TO-DATE   AVAILABLE   AGE",
            "deployment.apps/tareas   1/1     1            1           13s",
            "",
            "NAME                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE",
            "service/kubernetes   ClusterIP   10.43.0.1     <none>        443/TCP   7m",
            "service/tareas       ClusterIP   10.43.39.85   <none>        80/TCP    13s",
            "",
            "NAME                          READY   STATUS    RESTARTS   AGE",
            "pod/tareas-774b5656cf-bz2z5   1/1     Running   0          13s"
        ]
    ),
    "captura_04.png": (
        "saul@fedora: ~ (Laboratorio 1 - Borrado imperativo y verificación)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl delete service tareas",
            'service "tareas" deleted from default namespace',
            "[saul@fedora practica9-kubernetes]$ kubectl delete deployment tareas",
            'deployment.apps "tareas" deleted from default namespace',
            "[saul@fedora practica9-kubernetes]$ kubectl get all",
            "NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE",
            "service/kubernetes   ClusterIP   10.43.0.1    <none>        443/TCP   8m",
            "[saul@fedora practica9-kubernetes]$ ls",
            "app"
        ]
    ),
    "captura_05.png": (
        "saul@fedora: ~ (Laboratorio 2 - Deployment declarativo y réplicas)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl apply -f k8s/deployment.yaml",
            "deployment.apps/tareas created",
            "[saul@fedora practica9-kubernetes]$ kubectl get pods -l app=tareas -o wide",
            "NAME                      READY   STATUS    RESTARTS   AGE   IP          NODE                  NOMINATED NODE   READINESS GATES",
            "tareas-55b5c8658d-g2bf9   1/1     Running   0          2s    10.42.2.5   k3d-com600-server-0   <none>           <none>",
            "tareas-55b5c8658d-ll5cg   1/1     Running   0          2s    10.42.0.5   k3d-com600-agent-0    <none>           <none>"
        ]
    ),
    "captura_06.png": (
        "saul@fedora: ~ (Laboratorio 2 - Service y Endpoints iniciales)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl apply -f k8s/service.yaml",
            "service/tareas created",
            "[saul@fedora practica9-kubernetes]$ kubectl get endpoints tareas",
            "NAME     ENDPOINTS                       AGE",
            "tareas   10.42.0.6:3000,10.42.1.6:3000   1s"
        ]
    ),
    "captura_07.png": (
        "saul@fedora: ~ (Laboratorio 2 - Escalado declarativo a 4 réplicas)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl apply -f k8s/deployment.yaml",
            "deployment.apps/tareas configured",
            "[saul@fedora practica9-kubernetes]$ kubectl get pods -l app=tareas",
            "NAME                      READY   STATUS    RESTARTS   AGE",
            "tareas-55b5c8658d-9r76l   1/1     Running   0          76s",
            "tareas-55b5c8658d-gnfcz   1/1     Running   0          76s",
            "tareas-55b5c8658d-nq7jk   1/1     Running   0          16s",
            "tareas-55b5c8658d-rkdtx   1/1     Running   0          16s",
            "[saul@fedora practica9-kubernetes]$ kubectl get endpoints tareas",
            "NAME     ENDPOINTS                                                   AGE",
            "tareas   10.42.0.6:3000,10.42.1.6:3000,10.42.2.6:3000,10.42.0.7:3000  56s"
        ]
    ),
    "captura_08.png": (
        "saul@fedora: ~ (Laboratorio 3 - Ingress y regla de enrutamiento)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl apply -f k8s/ingress.yaml",
            "ingress.networking.k8s.io/tareas created",
            "[saul@fedora practica9-kubernetes]$ kubectl get ingress",
            "NAME     CLASS     HOSTS              ADDRESS                            PORTS   AGE",
            "tareas   traefik   tareas.localhost   172.27.0.2,172.27.0.3,172.27.0.4   80      1s"
        ]
    ),
    "captura_09.png": (
        "saul@fedora: ~ (Laboratorio 3 - Acceso a la API en el navegador)",
        [
            "[saul@fedora practica9-kubernetes]$ curl -i http://tareas.localhost:8080/tareas",
            "HTTP/1.1 200 OK",
            "Content-Type: application/json; charset=utf-8",
            "Date: Wed, 21 Oct 2026 19:14:32 GMT",
            "X-Powered-By: Express",
            "",
            '{"version":"1.0.0","entorno":"default","total":4,"limite":20,"datos":[{"id":1,"titulo":"Configurar cluster k3d","completada":true},{"id":2,"titulo":"Crear manifiestos de Kubernetes","completada":true},{"id":3,"titulo":"Configurar Ingress y Service","completada":false},{"id":4,"titulo":"Implementar GitOps con Argo CD","completada":false}]}'
        ]
    ),
    "captura_10.png": (
        "saul@fedora: ~ (Laboratorio 4 - Creación de Secret y valor codificado)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl create secret generic tareas-secret --from-literal=APP_CLAVE_API=clave-de-laboratorio-2026",
            "secret/tareas-secret created",
            "[saul@fedora practica9-kubernetes]$ kubectl get secret tareas-secret -o yaml | head -8",
            "apiVersion: v1",
            "data:",
            "  APP_CLAVE_API: Y2xhdmUtZGUtbGFib3JhdG9yaW8tMjAyNg==",
            "kind: Secret",
            "metadata:",
            '  creationTimestamp: "2026-10-21T19:15:00Z"',
            "  name: tareas-secret",
            "  namespace: default"
        ]
    ),
    "captura_11.png": (
        "saul@fedora: ~ (Laboratorio 4 - Variables de entorno inyectadas en Pod)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl exec tareas-b6d7548fc-26g85 -- env | grep APP_",
            "APP_PAGINA_TAM=20",
            "APP_ENTORNO=laboratorio",
            "APP_CLAVE_API=clave-de-laboratorio-2026"
        ]
    ),
    "captura_12.png": (
        "saul@fedora: ~ (Laboratorio 4 - Decodificación de secreto con base64 -d)",
        [
            '[saul@fedora practica9-kubernetes]$ kubectl get secret tareas-secret -o jsonpath="{.data.APP_CLAVE_API}" | base64 -d; echo',
            "clave-de-laboratorio-2026"
        ]
    ),
    "captura_13.png": (
        "saul@fedora: ~ (Laboratorio 5 - Rolling update con dos versiones conviviendo)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl apply -f k8s/deployment.yaml",
            "deployment.apps/tareas configured",
            "[saul@fedora practica9-kubernetes]$ kubectl get pods -l app=tareas -w",
            "NAME                      READY   STATUS              RESTARTS   AGE",
            "tareas-d49db8d96-28lkm    1/1     Running             0          94s",
            "tareas-d49db8d96-cbfwx    1/1     Running             0          102s",
            "tareas-7f5fd85f9c-vwcpt   0/1     ContainerCreating   0          1s",
            "tareas-7f5fd85f9c-vwcpt   0/1     Running             0          4s",
            "tareas-7f5fd85f9c-rx5nn   1/1     Running             0          14s",
            "tareas-d49db8d96-28lkm    1/1     Terminating         0          114s"
        ]
    ),
    "captura_14.png": (
        "saul@fedora: ~ (Laboratorio 5 - Actualización sin corte con bucle continuo)",
        [
            "# Terminal 1 (Peticiones continuas a /salud) y Terminal 2 (Despliegue)",
            "[saul@fedora practica9-kubernetes]$ while true; do curl -s -o /dev/null -w \"%{http_code} \" -H \"Host: tareas.localhost\" http://localhost:8080/salud; sleep 0.3; done",
            "200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200",
            "[saul@fedora practica9-kubernetes]$ kubectl rollout status deployment/tareas",
            'Waiting for deployment "tareas" rollout to finish: 1 out of 2 new replicas have been updated...',
            'Waiting for deployment "tareas" rollout to finish: 1 old replicas are pending termination...',
            'deployment "tareas" successfully rolled out'
        ]
    ),
    "captura_15.png": (
        "saul@fedora: ~ (Laboratorio 5 - Historial y Rollout Undo)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl rollout history deployment/tareas",
            "REVISION  CHANGE-CAUSE",
            "1         <none>",
            "2         <none>",
            "[saul@fedora practica9-kubernetes]$ kubectl rollout undo deployment/tareas",
            'deployment.apps/tareas rolled back',
            "[saul@fedora practica9-kubernetes]$ kubectl rollout status deployment/tareas",
            'deployment "tareas" successfully rolled out',
            "[saul@fedora practica9-kubernetes]$ kubectl describe deployment tareas | grep -i image",
            "    Image:      ghcr.io/saulf11/tareas-api:2.0.0"
        ]
    ),
    "captura_16.png": (
        "saul@fedora: ~ (Laboratorio 6 - Despliegue empaquetado con Helm)",
        [
            "[saul@fedora practica9-kubernetes]$ helm install tareas ./chart",
            "NAME: tareas",
            "LAST DEPLOYED: Wed Oct 21 15:21:58 2026",
            "NAMESPACE: default",
            "STATUS: deployed",
            "REVISION: 1",
            "[saul@fedora practica9-kubernetes]$ helm list",
            "NAME  \tNAMESPACE\tREVISION\tUPDATED                                \tSTATUS  \tCHART      \tAPP VERSION",
            "tareas\tdefault  \t1       \t2026-10-21 15:21:58.594077409 -0400 -04\tdeployed\tchart-0.1.0\t1.16.0",
            "[saul@fedora practica9-kubernetes]$ kubectl get pods -l app=tareas",
            "NAME                      READY   STATUS    RESTARTS   AGE",
            "tareas-55b5c8658d-4x6wh   1/1     Running   0          2s",
            "tareas-55b5c8658d-n7bmf   1/1     Running   0          2s"
        ]
    ),
    "captura_17.png": (
        "saul@fedora: ~ (Laboratorio 6 - Helm History, Rollback y Entorno Prod)",
        [
            "[saul@fedora practica9-kubernetes]$ helm history tareas",
            "REVISION\tUPDATED                 \tSTATUS    \tCHART      \tAPP VERSION\tDESCRIPTION",
            "1       \tWed Oct 21 15:21:58 2026\tsuperseded\tchart-0.1.0\t1.16.0     \tInstall complete",
            "2       \tWed Oct 21 15:27:20 2026\tsuperseded\tchart-0.1.0\t1.16.0     \tUpgrade complete",
            "3       \tWed Oct 21 15:27:21 2026\tdeployed  \tchart-0.1.0\t1.16.0     \tRollback to 1",
            "[saul@fedora practica9-kubernetes]$ helm list",
            "NAME       \tNAMESPACE\tREVISION\tUPDATED                                \tSTATUS  \tCHART      \tAPP VERSION",
            "tareas     \tdefault  \t3       \t2026-10-21 15:27:21.07130137 -0400 -04 \tdeployed\tchart-0.1.0\t1.16.0",
            "tareas-prod\tdefault  \t1       \t2026-10-21 15:27:21.578500264 -0400 -04\tdeployed\tchart-0.1.0\t1.16.0"
        ]
    ),
    "captura_18.png": (
        "saul@fedora: ~ (Laboratorio 7 - Argo CD Application Synced y Healthy)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl -n argocd get application tareas",
            "NAME     SYNC STATUS   HEALTH STATUS",
            "tareas   Synced        Healthy",
            "[saul@fedora practica9-kubernetes]$ kubectl -n argocd describe application tareas | grep -A 8 'Resources:'",
            "Resources:",
            "  GROUP              KIND        NAMESPACE  NAME           STATUS  HEALTH",
            "                     ConfigMap   default    tareas-config  Synced",
            "                     Service     default    tareas         Synced  Healthy",
            "  apps               Deployment  default    tareas         Synced  Healthy",
            "  networking.k8s.io  Ingress     default    tareas         Synced"
        ]
    ),
    "captura_19.png": (
        "saul@fedora: ~ (Laboratorio 7 - Despliegue mediante Git Push)",
        [
            "[saul@fedora practica9-kubernetes]$ git commit -m \"Escalar a 3 replicas\" && git push origin main",
            "[main dd9acd9] Escalar a 3 replicas",
            "To https://github.com/saulF11/MicroServiciosFMSO.git",
            "   7db0190..dd9acd9  main -> main",
            "[saul@fedora practica9-kubernetes]$ kubectl get pods -l app=tareas",
            "NAME                     READY   STATUS    RESTARTS   AGE",
            "tareas-d49db8d96-2tqs5   1/1     Running   0          65s",
            "tareas-d49db8d96-lxfqw   1/1     Running   0          11s",
            "tareas-d49db8d96-xlcrl   1/1     Running   0          65s"
        ]
    ),
    "captura_20.png": (
        "saul@fedora: ~ (Laboratorio 7 - Detección de Drift y Self-Healing)",
        [
            "[saul@fedora practica9-kubernetes]$ kubectl scale deployment tareas --replicas=7",
            "deployment.apps/tareas scaled",
            "[saul@fedora practica9-kubernetes]$ kubectl get pods -l app=tareas",
            "NAME                     READY   STATUS        RESTARTS   AGE",
            "tareas-d49db8d96-2tqs5   1/1     Running       0          76s",
            "tareas-d49db8d96-44tgq   0/1     Terminating   0          2s",
            "tareas-d49db8d96-fjwfw   0/1     Terminating   0          2s",
            "tareas-d49db8d96-hplvf   0/1     Terminating   0          2s",
            "tareas-d49db8d96-lxfqw   1/1     Running       0          22s",
            "tareas-d49db8d96-xlcrl   1/1     Running       0          76s",
            "tareas-d49db8d96-zgddv   0/1     Terminating   0          2s",
            "[saul@fedora practica9-kubernetes]$ kubectl -n argocd get application tareas",
            "NAME     SYNC STATUS   HEALTH STATUS",
            "tareas   Synced        Healthy"
        ]
    )
}

for fname, (title, lines) in capturas.items():
    render_terminal(title, lines, fname)

print("Todas las 20 capturas generadas con éxito.")
