
Justificación del Diseño:

Dependencias Funcionales:
Usuarios
IDUsuario → Nombre, Email, FechaRegistro, CuotaMensual

Cada usuario tiene un ID único y se asocia con su nombre, correo electrónico (único), fecha de registro y cuota mensual. Un usuario puede tener múltiples préstamos, pagos y multas.

Libros
IDLibro → Título, Autor, AñoPublicacion, Disponibles

Cada libro tiene un ID único y se asocia con su título, autor, año de publicación y cantidad disponible. Un libro puede estar asociado a múltiples préstamos.

Préstamos
IDPrestamo → IDUsuario, IDLibro, FechaPrestamo, FechaDevolucionEsperada, FechaDevolucion

Cada préstamo se identifica por su ID único y relaciona a un usuario con un libro en una fecha específica, incluyendo las fechas de devolución esperada y real.

Pagos
IDPago → IDUsuario, Mes, Año, FechaPago, Monto

Cada pago se identifica por su ID único y está asociado a un usuario en un mes y año específicos, registrando la fecha de pago y el monto.

Multas
IDMulta → IDPrestamo, Monto, FechaMulta

Cada multa se identifica por su ID único y está asociada a un préstamo específico, indicando el monto de la multa y la fecha en que se generó.

Claves Candidatas
Usuarios: (IDUsuario)
Libros: (IDLibro)
Préstamos: (IDPrestamo)
Pagos: (IDPago)
Multas: (IDMulta)


Diseño en Tercera Forma Normal (3FN):

Tabla Usuarios:
IDUsuario (Clave primaria)
Nombre
Email (único)
FechaRegistro
CuotaMensual

Tabla Libros:
IDLibro (Clave primaria)
Título
Autor
AñoPublicacion
Disponibles

Tabla Préstamos:
IDPrestamo (Clave primaria)
IDUsuario (Clave foránea que referencia a Usuarios)
IDLibro (Clave foránea que referencia a Libros)
FechaPrestamo
FechaDevolucionEsperada
FechaDevolucion

Tabla Pagos:
IDPago (Clave primaria)
IDUsuario (Clave foránea que referencia a Usuarios)
Mes
Año
FechaPago
Monto

Tabla Multas:
IDMulta (Clave primaria)
IDPrestamo (Clave foránea que referencia a Préstamos)
Monto
FechaMulta

Justificación del Diseño:
El diseño de la base de datos ha sido realizado siguiendo las normas de normalización hasta la Tercera Forma Normal (3FN), con el objetivo de eliminar redundancias, asegurar la integridad de los datos y optimizar el rendimiento de las consultas.

1. Normalización y Integridad de Datos
Eliminación de Redundancias: Al descomponer los datos en tablas relacionadas, evitamos la duplicación de información, lo que reduce el espacio de almacenamiento y previene inconsistencias.

Integridad Referencial: Las claves foráneas establecidas entre las tablas aseguran que las relaciones entre los datos sean válidas. Por ejemplo, un préstamo no puede existir sin un usuario y un libro válidos.

2. Tabla Usuarios
Email Único: La restricción de unicidad en el campo Email garantiza que cada usuario tenga un correo electrónico único, facilitando la comunicación y evitando duplicados.

CuotaMensual: Almacena la cuota mensual que paga el usuario, permitiendo una fácil actualización y consulta de este dato para fines administrativos y financieros.

3. Tabla Libros
Control de Inventario: El campo Disponibles permite llevar un seguimiento preciso de los ejemplares disponibles de cada libro, esencial para gestionar los préstamos y evitar sobreasignaciones.

Información Detallada: Al almacenar el título, autor y año de publicación, se facilita la búsqueda y clasificación de los libros en la biblioteca.

4. Tabla Préstamos
Registro de Operaciones: Esta tabla centraliza la información de cada préstamo realizado, incluyendo las fechas clave para el control de devoluciones y cálculo de posibles multas.

Gestión de Devoluciones: Los campos FechaDevolucionEsperada y FechaDevolucion permiten identificar retrasos y generar las acciones correspondientes.

5. Tabla Pagos
Historial Financiero: Al registrar cada pago realizado por los usuarios, se mantiene un historial detallado que puede ser utilizado para generar reportes financieros y evaluar la morosidad.

Validaciones Temporales: Los campos Mes y Año, junto con FechaPago, aseguran que los pagos correspondan al período correcto y permiten realizar análisis temporales.

6. Tabla Multas
Seguimiento de Penalizaciones: Al almacenar las multas generadas por retrasos, se facilita el seguimiento de las obligaciones pendientes de los usuarios y la aplicación de políticas de la biblioteca.

Asociación Directa con Préstamos: La clave foránea IDPrestamo vincula cada multa con su préstamo correspondiente, proporcionando contexto y facilitando consultas detalladas.

7. Cumplimiento de la Tercera Forma Normal
Dependencias Funcionales Correctas: Cada atributo no clave es funcionalmente dependiente únicamente de la clave primaria de su tabla, eliminando dependencias parciales y transitivas.

Flexibilidad y Escalabilidad: El diseño permite agregar nuevas funcionalidades sin afectar la estructura existente, ya que las tablas están correctamente normalizadas y relacionadas.

