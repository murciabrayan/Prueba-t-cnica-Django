# Prueba técnica Django – Alertas y paradas de máquina

Brayan Fernando Murcia Cordoba
8 de octubre de 2026

## Control de tiempo

Empecé la prueba a las 11:32 a. m. (hora Colombia), cuando creé el proyecto y el entorno virtual.

El primer commit, "Proyecto base Django", lo hice a las 11:38 a. m.
Enlace: https://github.com/murciabrayan/Prueba-t-cnica-Django/commit/2593b09f5daa4291a54dda50a461412a66724667

Después fui haciendo commits a medida que avanzaba:

- 11:41 a. m. – README con control de tiempo
- 11:48 a. m. – Modelos, migraciones, admin y usuarios demo
- 11:56 a. m. – Login, página principal, vistas con permisos y plantillas
- 12:32 p. m. – Diseño con Tailwind y vista responsive

El commit final es el de este README. Su hash lo envío en el correo de entrega.

## Qué hace la aplicación

Es una aplicación para registrar alertas y paradas de una máquina. Tiene inicio y cierre de sesión y una sola página principal que muestra lo que cada usuario puede hacer según su rol:

- El operario crea alertas y solo ve las que él reportó.
- El supervisor ve y edita todas las alertas y registra paradas.
- El jefe ve las alertas y las paradas, y puede cancelar una parada indicando el motivo.

Los roles los manejé con los grupos de Django. Cada vista revisa en el backend si el usuario tiene el rol necesario. Si alguien intenta hacer algo que no le corresponde, por ejemplo enviando la petición a mano, recibe un error 403 y no se cambia nada. Todas las páginas piden haber iniciado sesión y todos los formularios tienen protección CSRF.

Cuando se cancela una parada no se borra: se guarda quién la canceló, cuándo y por qué. Si alguien intenta cancelarla otra vez, se conserva la primera cancelación.

La duración de cada parada se calcula en minutos a partir de la fecha y hora de inicio y fin. Por eso una parada de 23:50 a 00:20 del día siguiente da 30 minutos.

## Tecnologías

- Python 3.13 y Django 5.2
- SQLite (viene incluido con Python, no hay que instalar nada)
- Tailwind CSS cargado desde su CDN para los estilos (necesita internet para verse con estilos)

## Cómo ejecutarla

En Windows, desde la carpeta del proyecto:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py crear_demo
python manage.py runserver
```

Luego se abre http://127.0.0.1:8000/ en el navegador.

El comando `crear_demo` crea los grupos (Operario, Supervisor y Jefe) y los usuarios de demostración. Lo hice como comando porque la base de datos no se sube al repositorio y así cualquiera puede tener los usuarios con una sola línea.

## Usuarios de demostración

Todos tienen la contraseña Demo12345.

- operario1: operario
- operario2: operario (lo agregué para comprobar que cada operario solo ve sus propias alertas)
- supervisor: supervisor
- jefe: jefe

## Pruebas realizadas

Las hice de forma manual en el navegador y enviando peticiones desde la consola del navegador.

1. Datos vacíos y fechas incorrectas: intenté guardar alertas y paradas con la descripción o el motivo vacíos (o solo con espacios), cancelar una parada sin motivo, y registrar paradas donde el fin era igual o anterior al inicio. Todas se rechazaron con un mensaje y no se guardó nada.
2. Parada de 23:50 a 00:20 del día siguiente: muestra 30 minutos.
3. Editar una alerta como operario y como jefe con una petición manual: la respuesta fue 403 y la alerta no cambió.
4. Cancelar dos veces la misma parada: la segunda vez aparece el aviso de que ya estaba cancelada. Se mantienen el primer usuario, la fecha y el motivo, y el registro no se borró ni se duplicó.
5. Creé 10 alertas (5 de cada operario) y 5 paradas. La página carga bien, conserva todos los registros, cada operario ve solo sus 5 alertas, y el supervisor y el jefe ven las 10.

También comprobé que sin iniciar sesión la página manda al login y que un formulario enviado sin el token CSRF se rechaza.

## Fallas que encontré y cómo las resolví

- El comando para generar requirements.txt no funcionaba porque estaba en CMD y no en PowerShell. Lo resolví usando `pip freeze > requirements.txt`.
- Al principio pensé crear los usuarios desde el admin de Django, pero la base de datos no se sube al repositorio y quien revise no los tendría. Por eso hice el comando `crear_demo`.
- Al pasar a Tailwind, los formularios que genera Django quedaban sin bordes porque Tailwind quita los estilos por defecto. Escribí los campos a mano en el HTML con los mismos nombres, y la validación sigue en el backend.

En las pruebas finales no encontré fallas.

## Pendientes

- Mostrar los errores al lado de cada campo y conservar lo que el usuario escribió cuando el formulario falla.
- Pruebas automatizadas.
- Filtros por máquina o fecha y paginación cuando haya muchos registros.
- Usar PostgreSQL y no depender del CDN de Tailwind en producción.

## Integración con un monolito Django

Agregaría la app `maquinas` a INSTALLED_APPS del monolito, incluiría sus rutas en el urls.py principal y correría sus migraciones.
Como los modelos usan el User de Django, funcionaría con los mismos usuarios y el mismo inicio de sesión del monolito.
Solo faltaría crear los grupos Operario, Supervisor y Jefe y asignarlos a los usuarios reales desde el admin.

## Resolución de problemas

**Caso 1.** Primero que todo intentaría calmar al supervisor, propondría otro método de registro, ya sea en papel escrito a mano o en planillas, y así después poder vincular toda esa información en la aplicación una vez se solucionen los problemas. Después revisaría los logs de la aplicación para entender el contexto de lo que pasó y la causa del problema. Como es posible que aun registrando las paradas manualmente sea importante tener el sistema de vuelta, daría reportes cada cierto tiempo en base a lo que voy encontrando y al posible escenario. Si después de cierto tiempo no logro identificar la causa, pediría ayuda a un desarrollador con más experiencia que me pueda guiar y ayudar en ese caso.

**Caso 2.** Recientemente tomé algunas clases sobre QA y en ese ámbito se me quedaron dos términos, los cuales son prioridad y severidad, y basándome en esto situaría en primer lugar el problema del inicio de sesión y luego el reporte. Pienso que aunque el reporte tenga prioridad, su severidad es casi nula, sin embargo, para no adelantarnos a los hechos y poder clasificar mejor ambas situaciones, habría que primero averiguar a cuántos usuarios está afectando el inicio de sesión, si es solo para una cuenta y si muestra algún detalle o mensaje que nos pueda ayudar. El jefe también debería proporcionar información como si el reporte es para verlo con un cliente, cuál es la hora límite para entregar el reporte, si existe ya un formato previo, etc. Así que basándome en eso daría prioridad para arreglar primero un problema u otro. Aunque si existe un equipo de trabajo cuyas responsabilidades están alineadas, pediría que me ayudaran en alguno de los dos casos, algún analista que pueda generar el reporte o algún compañero desarrollador que pueda mirar si soluciona la falla del inicio de sesión. Para la pregunta de cómo explicar los tiempos de espera, creo que es crucial comunicar ambas situaciones y pedir un poco de paciencia. En el caso del jefe se podría comunicar y decirle que aunque su reporte es urgente y estamos mirando la manera de solucionarlo o delegarlo a alguien, tenemos primero un incidente crítico donde los usuarios no pueden iniciar sesión. Y al usuario comunicarle la situación para evitar zozobra o malestar, que estamos resolviendo el problema de forma prioritaria y estamos investigando la causa del problema.

**Caso 3.** En estos casos hay que mantener la cabeza calmada, pediría disculpas a mi equipo de trabajo y pues asumiría la culpa. Después rechazaría esa propuesta, no es una buena práctica ni mucho menos una buena alternativa enviar cosas a producción sin revisarlas, hacer eso solo puede empeorar la situación. Así que volvería al commit pasado donde la versión es estable y no tiene errores, crearía una rama para arreglar el error basándome en los logs que nos dio el sistema y por último pediría una revisión de código por parte del líder, quizá en vivo o mediante un pull request.

## Uso de IA

Sí usé IA. Trabajé con Claude como asistente durante la prueba. Me guió paso a paso: propuso la estructura del proyecto, los permisos, las plantillas, los estilos y el comando de usuarios demo, y me explicó cada parte. Yo escribí el código en mi equipo, ejecuté los comandos, hice las pruebas manuales y los commits, y elegí el diseño de referencia. Las respuestas a los casos de resolución de problemas son mías.