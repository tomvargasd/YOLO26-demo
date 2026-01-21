# YOLO Demo - Detección en Tiempo Real

Aplicación Flask con YOLO para detección de objetos en tiempo real desde la cámara web.

## 🚀 Despliegue con Docker

### Construcción y ejecución

```bash
# Construir la imagen
docker-compose build

# Iniciar el servicio
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener el servicio
docker-compose down
```

### Acceso
- **HTTPS**: `https://localhost:5000` o `https://<tu-ip>:5000`
- Acepta el certificado autofirmado en el navegador

## 📦 Gestión de Modelos

Los modelos YOLO se almacenan en la carpeta `models/` que está montada como volumen.

### Agregar un nuevo modelo activo:

1. Coloca tu modelo `.pt` en la carpeta `models/`
2. Renómbralo con el prefijo `active_`, por ejemplo: `active_yolo26m.pt`
3. Reinicia el contenedor: `docker-compose restart`

**Nota**: Solo se carga el primer modelo que encuentre con el prefijo `active_*`.

### Cambiar de modelo:

```bash
# Renombrar el modelo actual (quitar active_)
mv models/active_yolo26m.pt models/yolo26m.pt

# Activar otro modelo
mv models/yolo26s.pt models/active_yolo26s.pt

# Reiniciar
docker-compose restart
```

## 🔧 Configuración

### FPS
Actualmente configurado a **8 FPS** para mejor rendimiento. Para cambiar:
- Edita `templates/index.html`, línea con `const FPS = 8;`

### SSL/HTTPS
Los certificados `cert.pem` y `key.pem` deben estar en la raíz del proyecto. Para generar nuevos:

```bash
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout key.pem -out cert.pem -days 365 \
  -subj "/CN=<tu-ip-o-dominio>"
```

## 📁 Estructura del Proyecto

```
yolo26-demo/
├── app.py                  # Aplicación Flask principal
├── requirements.txt        # Dependencias Python
├── Dockerfile             # Configuración Docker
├── docker-compose.yml     # Orquestación Docker
├── cert.pem              # Certificado SSL
├── key.pem               # Clave privada SSL
├── models/               # Modelos YOLO (volumen Docker)
│   └── active_yolo26m.pt # Modelo activo
└── templates/
    └── index.html        # Interfaz web
```

## 🎯 Características

- ✅ Detección YOLO en tiempo real
- ✅ Procesamiento a 8 FPS
- ✅ Interfaz web minimalista
- ✅ Soporte HTTPS
- ✅ Video vertical (9:16)
- ✅ Gestión dinámica de modelos
- ✅ Containerizado con Docker

## 🐳 Despliegue en Dockploy

1. Sube el proyecto a tu repositorio Git
2. En Dockploy, crea un nuevo servicio desde Git
3. Asegúrate de mapear el puerto `5000:5000`
4. Configura el volumen para `models/`
5. Agrega las variables de entorno si es necesario
6. Despliega
