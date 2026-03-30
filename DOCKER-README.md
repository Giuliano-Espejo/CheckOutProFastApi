# 🐳 Docker Setup: PostgreSQL + pgAdmin

Este proyecto levanta un entorno simple con **PostgreSQL 15** y **pgAdmin 4** usando Docker Compose, ideal para desarrollo local.

---

## 📦 Servicios incluidos

### 🗄️ PostgreSQL (`db`)

* Imagen: `postgres:15`
* Puerto: `5432`
* Base de datos: `midb`
* Usuario: `admin`
* Password: `admin123`
* Persistencia de datos mediante volumen Docker

### 🛠️ pgAdmin (`pgadmin`)

* Imagen: `dpage/pgadmin4`
* URL: http://localhost:8080
* Email: `admin@mail.com`
* Password: `admin123`
* Dependiente del servicio de base de datos

---

## 🚀 Cómo levantar el proyecto

1. Asegurate de tener Docker y Docker Compose instalados.
2. En la carpeta donde está el archivo `docker-compose.yml`, ejecutar:

```bash
docker compose up -d
```

3. Verificar que los contenedores estén corriendo:

```bash
docker ps
```

---

## 🌐 Accesos

* **PostgreSQL**

  * Host: `localhost`
  * Puerto: `5432`
  * Usuario: `admin`
  * Password: `admin123`
  * Base de datos: `midb`

* **pgAdmin**

  * URL: http://localhost:8080
  * Email: `admin@mail.com`
  * Password: `admin123`

---

## 🔗 Conectar pgAdmin a PostgreSQL

1. Ingresar a pgAdmin desde el navegador.
2. Crear un nuevo servidor:

   * **Name:** (cualquiera, por ejemplo `local-db`)
   * **Host:** `db` (nombre del servicio en Docker)
   * **Port:** `5432`
   * **Username:** `admin`
   * **Password:** `admin123`

---

## 💾 Volúmenes

* `postgres_data`: almacena los datos de PostgreSQL de forma persistente.

---

## 🧹 Detener el entorno

```bash
docker compose down
```

Para eliminar también los volúmenes:

```bash
docker compose down -v
```