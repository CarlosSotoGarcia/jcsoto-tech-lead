#!/usr/bin/env python3
"""Generado por Loom (ADR-0054) para el Proyecto PILOTO E1c ITZ Inventarios (Claude cuenta normal CLI). No lo edites a mano: regenéralo
desde la plataforma. No contiene credenciales: quien lo ejecuta (GitHub Actions o Cloud Build) se
autentica con gcloud antes, así que aquí solo se construye y se despliega. Solo usa la biblioteca
estándar de Python 3 y funciona igual en Linux, macOS y Windows."""

import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime

PROJECT_ID = "itz-inventario"
REGION = "us-central1"
REPO = "inventarios"


def ejecutar(*comando: str) -> None:
    """Corre un comando y detiene el release si falla (shutil.which resuelve gcloud.cmd/npm.cmd en Windows)."""
    print("+", " ".join(comando), flush=True)
    subprocess.run([shutil.which(comando[0]) or comando[0], *comando[1:]], check=True)


def etiqueta_de_release() -> str:
    if os.environ.get("RELEASE_TAG"):
        return os.environ["RELEASE_TAG"]
    try:
        salida = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
        )
        return salida.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return datetime.now().strftime("%Y%m%d%H%M%S")


TAG = etiqueta_de_release()


# --- Configuración del despliegue (la fija Loom al generar este script; no lleva secretos) ---------------------
BD = {'instancia': 'inventarios-db',
 'nombre': 'inventarios',
 'usuario': 'inventarios',
 'tier': 'db-f1-micro',
 'version': 'POSTGRES_15'}
"""Base de datos administrada (Cloud SQL) que se crea y conecta, o None."""
VARIABLES = {'SPRING_PROFILES_ACTIVE': 'prod',
 'ADMIN_EMAIL': 'jnc.soga@gmail.com',
 'ADMIN_NOMBRE': 'Administrador',
 'ADMIN_PASSWORD_HASH': '$2a$10$hGRa1zQRIGkUGFbnx1b9ZuaHCJPqsASrULkQtzRBUqlWciAG/IEFW',
 'APP_CORS_ALLOWED_ORIGINS': '{URL_FRONTEND}'}
"""Variables de entorno sin secretos que recibe el servicio. «{URL_BACKEND}» y «{URL_FRONTEND}» se reemplazan por las URL."""
SECRETOS_GENERADOS = ['JWT_SECRET']
"""Variables de entorno cuyo valor es un secreto aleatorio guardado en Secret Manager (p. ej. JWT_SECRET)."""
PUBLICO = True
"""El servicio acepta llamadas sin autenticación de GCP (la autenticación es la de la propia aplicación)."""
FRONTEND = {'hosting': 'cloud_run', 'servicio': 'inventarios-web'}
"""Frontend: {"hosting": "firebase_hosting" | "cloud_run", "servicio": nombre} o None. Sirve para conocer su URL antes de desplegar (CORS)."""
WIF = {'dueno': 'CarlosSotoGarcia',
 'repo': 'loom-piloto-e1c-claude-cli',
 'pool': 'loom-github',
 'proveedor': 'github',
 'cuenta': 'loom-release-deployer'}
"""Despliegue automático con GitHub Actions + Workload Identity Federation (ADR-0081), o None."""
TRIGGER = None
"""Trigger de Cloud Build que reejecuta este script en cada cambio de la rama base (o tag), o None."""
JDBC = True
"""La aplicación conecta con JDBC: además de DB_HOST, DB_PORT y DB_NAME se entrega DB_URL."""


def gcloud(*args: str, entrada: str | None = None, capturar: bool = False, permitir_fallo: bool = False, ocultar: tuple = ()):
    """Corre gcloud y detiene el release si falla. `ocultar` son valores (contraseñas) que no deben quedar en el registro."""
    visible = " ".join("******" if a in ocultar else a for a in args)
    print("+ gcloud", visible, flush=True)
    r = subprocess.run([shutil.which("gcloud") or "gcloud", *args], input=entrada, text=True, capture_output=capturar)
    if r.returncode != 0 and not permitir_fallo:
        if capturar and r.stderr:
            print(r.stderr.strip(), flush=True)
        raise subprocess.CalledProcessError(r.returncode, ["gcloud", *args])
    return r


def asegurar_entorno_gcp(apis: list[str]) -> None:
    """Deja listo el proyecto de GCP: habilita las APIs que faltan y crea el repositorio de imágenes."""
    habilitadas = gcloud("services", "list", "--enabled", "--project", PROJECT_ID, "--format=value(config.name)", capturar=True, permitir_fallo=True)
    if habilitadas.returncode != 0:
        sys.exit(f"ERROR: no se pudo consultar el proyecto {PROJECT_ID} de GCP (¿la cuenta activa tiene permisos?):\n{habilitadas.stderr.strip()}")
    faltan = [a for a in apis if a not in habilitadas.stdout.split()]
    if faltan:
        print(f"==> Habilitando las APIs de GCP que faltan: {', '.join(faltan)}", flush=True)
        r = gcloud("services", "enable", *faltan, "--project", PROJECT_ID, capturar=True, permitir_fallo=True)
        if r.returncode != 0:
            sys.exit(f"ERROR: no se pudieron habilitar las APIs ({', '.join(faltan)}). Cloud Build y Cloud SQL exigen facturación activa:\n{r.stderr.strip()}")
    repositorio = gcloud("artifacts", "repositories", "describe", REPO, "--location", REGION, "--project", PROJECT_ID, capturar=True, permitir_fallo=True)
    if repositorio.returncode != 0:
        print(f"==> Creando el repositorio de imágenes «{REPO}»", flush=True)
        gcloud("artifacts", "repositories", "create", REPO, "--repository-format=docker", "--location", REGION, "--project", PROJECT_ID)


def cuenta_de_ejecucion(servicio: str) -> str:
    """Cuenta de servicio con la que corre el servicio (la creamos para darle solo acceso a sus secretos)."""
    nombre = (servicio + "-run")[:30].rstrip("-")
    correo = f"{nombre}@{PROJECT_ID}.iam.gserviceaccount.com"
    existe = gcloud("iam", "service-accounts", "describe", correo, "--project", PROJECT_ID, capturar=True, permitir_fallo=True)
    if existe.returncode != 0:
        gcloud("iam", "service-accounts", "create", nombre, "--display-name", f"Ejecución de {servicio}", "--project", PROJECT_ID)
        time.sleep(15)  # la cuenta tarda unos segundos en propagarse
    return correo


def secreto(nombre: str, cuenta: str, largo: int = 24) -> str:
    """Crea el secreto en Secret Manager si no existe (valor aleatorio), da acceso a la cuenta de ejecución y devuelve su valor."""
    existe = gcloud("secrets", "describe", nombre, "--project", PROJECT_ID, capturar=True, permitir_fallo=True)
    if existe.returncode != 0:
        gcloud("secrets", "create", nombre, "--replication-policy", "automatic", "--data-file=-", "--project", PROJECT_ID, entrada=secrets.token_urlsafe(largo), capturar=True)
    for _ in range(5):
        r = gcloud(
            "secrets", "add-iam-policy-binding", nombre, "--member", f"serviceAccount:{cuenta}",
            "--role", "roles/secretmanager.secretAccessor", "--project", PROJECT_ID, capturar=True, permitir_fallo=True,
        )
        if r.returncode == 0:
            break
        time.sleep(10)
    else:
        sys.exit(f"ERROR: no se pudo dar acceso al secreto {nombre} a {cuenta}:\n{r.stderr.strip()}")
    return gcloud("secrets", "versions", "access", "latest", "--secret", nombre, "--project", PROJECT_ID, capturar=True).stdout.strip()


def esperar_instancia(instancia: str, limite_s: int = 1200) -> None:
    """Espera a que la instancia de Cloud SQL esté lista (crearla tarda varios minutos)."""
    inicio = time.time()
    ultimo = ""
    while time.time() - inicio < limite_s:
        estado = gcloud("sql", "instances", "describe", instancia, "--project", PROJECT_ID, "--format=value(state)", capturar=True, permitir_fallo=True).stdout.strip()
        if estado == "RUNNABLE":
            return
        if estado != ultimo:
            print(f"==> Cloud SQL: la instancia está en estado {estado or 'desconocido'}; esperando...", flush=True)
            ultimo = estado
        if estado in ("FAILED", "SUSPENDED", "MAINTENANCE"):
            sys.exit(f"ERROR: la instancia de Cloud SQL quedó en estado {estado}.")
        time.sleep(20)
    sys.exit(f"ERROR: la instancia de Cloud SQL no estuvo lista en {limite_s // 60} minutos.")


def base_de_datos(cuenta: str) -> tuple[dict[str, str], list[str]]:
    """Cloud SQL (PostgreSQL): crea la instancia, la base y el usuario si no existen, guarda la contraseña en Secret Manager
    y devuelve (variables de entorno, secretos) para el servicio. Se puede volver a ejecutar sin duplicar nada.
    La instancia usa IP pública con TLS obligatorio y contraseña aleatoria (sin red privada): es un ambiente de pruebas."""
    instancia = BD["instancia"]
    existe = gcloud("sql", "instances", "describe", instancia, "--project", PROJECT_ID, capturar=True, permitir_fallo=True)
    if existe.returncode != 0:
        print(f"==> Cloud SQL: creando la instancia «{instancia}» (tarda entre 5 y 10 minutos)", flush=True)
        r = gcloud(
            "sql", "instances", "create", instancia, "--project", PROJECT_ID, "--database-version", BD["version"], "--tier", BD["tier"],
            "--edition", "ENTERPRISE", "--region", REGION, "--storage-size", "10GB", "--storage-type", "SSD", "--assign-ip",
            "--authorized-networks", "0.0.0.0/0", "--ssl-mode", "ENCRYPTED_ONLY", "--async", capturar=True, permitir_fallo=True,
        )
        if r.returncode != 0 and gcloud("sql", "instances", "describe", instancia, "--project", PROJECT_ID, capturar=True, permitir_fallo=True).returncode != 0:
            sys.exit(f"ERROR: no se pudo crear la instancia de Cloud SQL:\n{r.stderr.strip()}")
    esperar_instancia(instancia)
    bases = gcloud("sql", "databases", "list", "--instance", instancia, "--project", PROJECT_ID, "--format=value(name)", capturar=True).stdout.split()
    if BD["nombre"] not in bases:
        gcloud("sql", "databases", "create", BD["nombre"], "--instance", instancia, "--project", PROJECT_ID)
    clave = secreto("db-password", cuenta)
    usuarios = gcloud("sql", "users", "list", "--instance", instancia, "--project", PROJECT_ID, "--format=value(name)", capturar=True).stdout.split()
    verbo = "set-password" if BD["usuario"] in usuarios else "create"
    gcloud("sql", "users", verbo, BD["usuario"], "--instance", instancia, "--project", PROJECT_ID, "--password", clave, ocultar=(clave,))
    info = json.loads(gcloud("sql", "instances", "describe", instancia, "--project", PROJECT_ID, "--format=json", capturar=True).stdout)
    ip = next(a["ipAddress"] for a in info["ipAddresses"] if a["type"] == "PRIMARY")
    variables = {"DB_HOST": ip, "DB_PORT": "5432", "DB_NAME": BD["nombre"], "DB_USER": BD["usuario"]}
    if JDBC:
        variables["DB_URL"] = f"jdbc:postgresql://{ip}:5432/{BD['nombre']}?sslmode=require"
    return variables, ["DB_PASSWORD=db-password"]


def url_de_servicio(servicio: str) -> str:
    """URL determinista de un servicio de Cloud Run (se conoce antes de desplegarlo)."""
    numero = gcloud("projects", "describe", PROJECT_ID, "--format=value(projectNumber)", capturar=True).stdout.strip()
    return f"https://{servicio}-{numero}.{REGION}.run.app"


def construir_imagen(directorio: str, imagen: str) -> None:
    """Construye la imagen con Cloud Build. En una máquina con sesión de persona transmite el registro del build; sin ella
    (GitHub Actions, Cloud Build) la cuenta de servicio no puede leerlo, así que lanza el build sin esperar y consulta su estado."""
    if not (os.environ.get("GITHUB_ACTIONS") or os.environ.get("RELEASE_TAG")):
        ejecutar("gcloud", "builds", "submit", directorio, "--project", PROJECT_ID, "--tag", imagen)
        return
    r = gcloud("builds", "submit", directorio, "--project", PROJECT_ID, "--tag", imagen, "--async", "--format=value(id)", capturar=True)
    identificador = r.stdout.strip().splitlines()[-1].strip()
    print(f"Build {identificador} en marcha (sin transmitir su registro: esta cuenta no puede leerlo).", flush=True)
    ultimo = ""
    limite = time.time() + 1800
    while time.time() < limite:
        d = gcloud("builds", "describe", identificador, "--project", PROJECT_ID, "--format=value(status)", capturar=True, permitir_fallo=True)
        estado = d.stdout.strip()
        if estado and estado != ultimo:
            print(f"Build {identificador}: {estado}", flush=True)
            ultimo = estado
        if estado == "SUCCESS":
            return
        if estado in ("FAILURE", "INTERNAL_ERROR", "TIMEOUT", "CANCELLED", "EXPIRED"):
            sys.exit(f"ERROR: el build de la imagen terminó en {estado}. Registro: https://console.cloud.google.com/cloud-build/builds/{identificador}?project={PROJECT_ID}")
        time.sleep(8)
    sys.exit(f"ERROR: el build {identificador} no terminó en 30 minutos.")


def desplegar_cloud_run(
    nombre: str, servicio: str, directorio: str, entorno: dict[str, str] | None = None,
    secretos: list[str] | None = None, cuenta: str | None = None, publico: bool = False,
) -> None:
    imagen = f"{REGION}-docker.pkg.dev/{PROJECT_ID}/{REPO}/{servicio}:{TAG}"
    if not os.path.isfile(os.path.join(directorio, "Dockerfile")):
        sys.exit(
            f"ERROR: no existe {directorio}/Dockerfile, que Cloud Build necesita para construir {nombre}. "
            "El esqueleto solo trae Dockerfile.dev (desarrollo): el Dockerfile de producción lo crea el paquete "
            "«Dockerfiles de producción y CI». Genera y fusiona ese paquete antes de ejecutar el release."
        )
    print(f"==> {nombre}: construyendo {imagen}", flush=True)
    construir_imagen(directorio, imagen)
    print(f"==> {nombre}: desplegando en Cloud Run", flush=True)
    argumentos = ["run", "deploy", servicio, "--project", PROJECT_ID, "--region", REGION, "--image", imagen, "--quiet", "--memory", "1Gi", "--cpu-boost"]
    if cuenta:
        argumentos += ["--service-account", cuenta]
    argumentos += ["--allow-unauthenticated"] if publico else ["--no-allow-unauthenticated"]
    archivo = None
    if entorno:
        # Un archivo evita los problemas de escape del separador de gcloud (en Windows, cmd interpreta el carácter ^).
        archivo = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")
        json.dump(entorno, archivo, ensure_ascii=False)
        archivo.close()
        argumentos += ["--env-vars-file", archivo.name]
    if secretos:
        argumentos += ["--set-secrets", ",".join(f"{s}:latest" for s in secretos)]
    try:
        gcloud(*argumentos)
    finally:
        if archivo:
            os.unlink(archivo.name)
    url = gcloud("run", "services", "describe", servicio, "--project", PROJECT_ID, "--region", REGION, "--format=value(status.url)", capturar=True).stdout.strip()
    print(f"Service URL: {url}", flush=True)


def url_de_frontend() -> str:
    """URL determinista del frontend (Firebase Hosting o Cloud Run), conocida antes de desplegarlo."""
    if not FRONTEND:
        sys.exit("ERROR: una variable usa {URL_FRONTEND} pero el proyecto no despliega frontend.")
    if FRONTEND["hosting"] == "firebase_hosting":
        return f"https://{FRONTEND['servicio']}.web.app"
    return url_de_servicio(FRONTEND["servicio"])


def preparar_y_desplegar_backend(servicio: str, directorio: str) -> None:
    """Prepara lo que necesita el backend (cuenta, secretos, base de datos, variables) y lo despliega."""
    entorno = {}
    for clave, valor in VARIABLES.items():
        if "{URL_BACKEND}" in valor:
            valor = valor.replace("{URL_BACKEND}", url_de_servicio(servicio))
        if "{URL_FRONTEND}" in valor:
            valor = valor.replace("{URL_FRONTEND}", url_de_frontend())
        entorno[clave] = valor
    secretos: list[str] = []
    cuenta = None
    if BD or SECRETOS_GENERADOS:
        cuenta = cuenta_de_ejecucion(servicio)
    if BD:
        variables, sec = base_de_datos(cuenta)
        entorno.update(variables)
        secretos += sec
    for variable in SECRETOS_GENERADOS:
        identificador = variable.lower().replace("_", "-")
        secreto(identificador, cuenta, 48)
        secretos.append(f"{variable}={identificador}")
    desplegar_cloud_run("Backend", servicio, directorio, entorno, secretos, cuenta, PUBLICO)


def preparar_y_desplegar_frontend(servicio: str, directorio: str, servicio_backend: str | None) -> None:
    """Despliega el frontend en Cloud Run: público (lo abre el navegador) y con API_BASE_URL apuntando al backend."""
    entorno = {"API_BASE_URL": url_de_servicio(servicio_backend)} if servicio_backend else None
    desplegar_cloud_run("Frontend", servicio, directorio, entorno, None, None, True)


ROLES_DESPLIEGUE = [
    "roles/run.admin", "roles/iam.serviceAccountUser", "roles/iam.serviceAccountAdmin", "roles/cloudsql.admin",
    "roles/secretmanager.admin", "roles/artifactregistry.admin", "roles/cloudbuild.builds.editor",
    "roles/serviceusage.serviceUsageAdmin", "roles/storage.admin", "roles/logging.logWriter",
]


def asegurar_trigger() -> None:
    """Deja creado el trigger de Cloud Build que vuelve a ejecutar este script en cada cambio de la rama (o tag).
    Es idempotente. Dentro de Cloud Build (RELEASE_TAG definido) no hace nada. Si el repositorio de GitHub todavía no está
    conectado a Cloud Build, explica el único paso manual que falta y sigue: el despliegue de esta corrida ya se hizo."""
    if not TRIGGER or os.environ.get("RELEASE_TAG"):
        return
    print(f"==> Trigger de Cloud Build: {TRIGGER['nombre']}", flush=True)
    existe = gcloud("builds", "triggers", "list", "--project", PROJECT_ID, "--region", "global", "--filter", f"name={TRIGGER['nombre']}",
                    "--format=value(name)", capturar=True, permitir_fallo=True)
    if existe.returncode == 0 and existe.stdout.strip():
        print("El trigger ya existe; cada cambio en la rama volverá a desplegar.", flush=True)
        return
    cuenta = f"{TRIGGER['cuenta']}@{PROJECT_ID}.iam.gserviceaccount.com"
    if gcloud("iam", "service-accounts", "describe", cuenta, "--project", PROJECT_ID, capturar=True, permitir_fallo=True).returncode != 0:
        gcloud("iam", "service-accounts", "create", TRIGGER["cuenta"], "--display-name", "Despliegue por trigger (Loom)", "--project", PROJECT_ID)
    for rol in ROLES_DESPLIEGUE:
        for _ in range(5):
            r = gcloud("projects", "add-iam-policy-binding", PROJECT_ID, "--member", f"serviceAccount:{cuenta}", "--role", rol,
                       "--condition=None", "--quiet", capturar=True, permitir_fallo=True)
            if r.returncode == 0:
                break
            time.sleep(4)
    disparo = ["--branch-pattern", f"^{TRIGGER['rama']}$"] if TRIGGER.get("rama") else ["--tag-pattern", TRIGGER["tag"]]
    r = gcloud("builds", "triggers", "create", "github", "--project", PROJECT_ID, "--region", "global", "--name", TRIGGER["nombre"],
               "--repo-owner", TRIGGER["dueno"], "--repo-name", TRIGGER["repo"], *disparo, "--build-config", TRIGGER["archivo"],
               "--service-account", f"projects/{PROJECT_ID}/serviceAccounts/{cuenta}", capturar=True, permitir_fallo=True)
    if r.returncode == 0:
        print("Trigger creado: cada cambio en la rama desplegará solo.", flush=True)
        return
    print(
        "\nNO se pudo crear el trigger. Casi siempre es porque el repositorio no está conectado a Cloud Build. Es un paso único "
        "que exige autorizar la app de GitHub con tu cuenta y no se puede hacer por API:\n"
        f"  1. Abre https://console.cloud.google.com/cloud-build/triggers/connect?project={PROJECT_ID}\n"
        f"  2. Elige GitHub y autoriza el repositorio {TRIGGER['dueno']}/{TRIGGER['repo']}.\n"
        "  3. Vuelve a ejecutar este release: creará el trigger.\n"
        f"Detalle: {(r.stderr or '').strip()[:300]}",
        flush=True,
    )


def asegurar_wif() -> None:
    """Deja listo el despliegue automático con GitHub Actions y Workload Identity Federation (ADR-0081): un pool y un
    proveedor OIDC que solo aceptan a este repositorio, la cuenta de servicio desplegadora con sus roles y las variables
    del repositorio que usa el workflow. Es idempotente y no necesita ningún paso manual. Dentro de GitHub Actions no
    hace nada (ahí el script solo despliega)."""
    if not WIF or os.environ.get("GITHUB_ACTIONS") or os.environ.get("RELEASE_TAG"):
        return
    print(f"==> Despliegue automático: Workload Identity Federation para {WIF['dueno']}/{WIF['repo']}", flush=True)
    gcloud("services", "enable", "cloudresourcemanager.googleapis.com", "iamcredentials.googleapis.com", "sts.googleapis.com", "--project", PROJECT_ID, capturar=True, permitir_fallo=True)
    numero = gcloud("projects", "describe", PROJECT_ID, "--format=value(projectNumber)", capturar=True).stdout.strip()
    cuenta = f"{WIF['cuenta']}@{PROJECT_ID}.iam.gserviceaccount.com"
    if gcloud("iam", "service-accounts", "describe", cuenta, "--project", PROJECT_ID, capturar=True, permitir_fallo=True).returncode != 0:
        gcloud("iam", "service-accounts", "create", WIF["cuenta"], "--display-name", "Despliegue desde GitHub Actions (Loom)", "--project", PROJECT_ID)
    for rol in ROLES_DESPLIEGUE:
        for _ in range(5):
            r = gcloud("projects", "add-iam-policy-binding", PROJECT_ID, "--member", f"serviceAccount:{cuenta}", "--role", rol,
                       "--condition=None", "--quiet", capturar=True, permitir_fallo=True)
            if r.returncode == 0:
                break
            time.sleep(4)
    pool, proveedor = WIF["pool"], WIF["proveedor"]
    if gcloud("iam", "workload-identity-pools", "describe", pool, "--location", "global", "--project", PROJECT_ID, capturar=True, permitir_fallo=True).returncode != 0:
        gcloud("iam", "workload-identity-pools", "create", pool, "--location", "global", "--project", PROJECT_ID, "--display-name", "GitHub Actions (Loom)")
    if gcloud("iam", "workload-identity-pools", "providers", "describe", proveedor, "--workload-identity-pool", pool, "--location", "global",
              "--project", PROJECT_ID, capturar=True, permitir_fallo=True).returncode != 0:
        gcloud("iam", "workload-identity-pools", "providers", "create-oidc", proveedor, "--workload-identity-pool", pool, "--location", "global",
               "--project", PROJECT_ID, "--issuer-uri", "https://token.actions.githubusercontent.com",
               "--attribute-mapping", "google.subject=assertion.sub,attribute.repository=assertion.repository",
               "--attribute-condition", f"assertion.repository=='{WIF['dueno']}/{WIF['repo']}'")
    miembro = f"principalSet://iam.googleapis.com/projects/{numero}/locations/global/workloadIdentityPools/{pool}/attribute.repository/{WIF['dueno']}/{WIF['repo']}"
    gcloud("iam", "service-accounts", "add-iam-policy-binding", cuenta, "--project", PROJECT_ID, "--role", "roles/iam.workloadIdentityUser",
           "--member", miembro, "--quiet", capturar=True)
    proveedor_completo = f"projects/{numero}/locations/global/workloadIdentityPools/{pool}/providers/{proveedor}"
    variables = {"GCP_WORKLOAD_IDENTITY_PROVIDER": proveedor_completo, "GCP_SERVICE_ACCOUNT": cuenta}
    repo = f"{WIF['dueno']}/{WIF['repo']}"
    if shutil.which("gh"):
        fallo = False
        for nombre, valor in variables.items():
            r = subprocess.run(["gh", "variable", "set", nombre, "--body", valor, "-R", repo], capture_output=True, text=True)
            fallo = fallo or r.returncode != 0
            print(f"+ gh variable set {nombre} -R {repo}: {'ok' if r.returncode == 0 else r.stderr.strip()[:200]}", flush=True)
        if not fallo:
            print("Listo: cada cambio en la rama volverá a desplegar desde GitHub Actions.", flush=True)
            return
    print(
        "NO se pudieron guardar las variables del repositorio (falta la CLI `gh` autenticada). Créalas en GitHub, "
        "Settings > Secrets and variables > Actions > Variables:" + "\n"
        + "".join(f"  {k} = {v}" + "\n" for k, v in variables.items()),
        flush=True,
    )


def main() -> None:
    asegurar_entorno_gcp(['cloudbuild.googleapis.com',
 'run.googleapis.com',
 'artifactregistry.googleapis.com',
 'iam.googleapis.com',
 'cloudresourcemanager.googleapis.com',
 'secretmanager.googleapis.com',
 'sqladmin.googleapis.com'])
    preparar_y_desplegar_backend("inventarios-api", os.environ.get("BACKEND_DIR", "backend"))
    preparar_y_desplegar_frontend("inventarios-web", os.environ.get("FRONTEND_DIR", "frontend"), "inventarios-api")
    asegurar_wif()
    print(f"==> Release {TAG} terminado", flush=True)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
