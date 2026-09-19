# ADR-0056: Un README por servicio, además del de la raíz

## Estado

Aceptada. Amplía [ADR-0050](0050-entorno-de-desarrollo-dockerizado-y-readme-en-el-esqueleto.md) (README de despliegue en desarrollo en la raíz).

## Contexto

El README de la raíz explica cómo levantar todo el aplicativo con Docker, pero cada servicio (backend, frontend, cada microservicio) también necesita su propia
guía: cómo levantarlo solo, variables, pruebas, estructura y, en el backend, la URL de Swagger.

## Decisión

1. **Arquitectura (skill 04):** la estructura de carpetas incluye un `README.md` en la raíz y uno por servicio o aplicación.
2. **Descomposición (skill 05):** el README de la raíz enlaza a los de cada servicio; el **primer paquete de backend y el primero de frontend del esqueleto** crean el
   README propio de su servicio (qué hace, cómo levantarlo solo, variables de entorno, pruebas, estructura y URL de Swagger). En multirepo, el README de cada
   repositorio hace ese papel. Los paquetes que cambian cómo se instala, configura, levanta o prueba su servicio actualizan su README y el de la raíz.
3. **Generación de código (skill 06):** la regla del agente exige mantener al día ambos niveles de README. Además hay una compuerta: el primer paquete de backend
   y el de frontend del esqueleto no pueden terminar sin escribir un README dentro de la carpeta de su servicio (monorepo) o el de la raíz del repositorio
   (multirepo); se rechaza hasta 2 veces, como la de pruebas y la de archivos obligatorios.
4. **Revisión (skill 07):** si el paquete cambia cómo se instala, configura, levanta o prueba un servicio y su README no lo refleja, se reporta una observación
   menor.

## Consecuencias

- Los paquetes del esqueleto ya generados o fusionados antes de este ADR no cumplen la compuerta; para incluirla hay que volver a descomponer y regenerar esos
  paquetes, o pedir la corrección en un paquete posterior. La regla de mantener los README sí se aplica a todo el código nuevo.
- La compuerta identifica el README del servicio como uno situado un nivel debajo de la raíz; no valida su contenido (eso lo hace la revisión).

## Pendiente

- Validar que el README de cada servicio incluya las secciones esperadas (levantar, variables, pruebas, Swagger).
