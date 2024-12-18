﻿**1. Determinamos las dependencias funcionales:**

**DFs identificadas a partir de las restricciones:**

1. **Sucursal y datos relacionados**:
   1. codigoSucursal → domicilioSucursal, telefonoSucursal
1. **Fosas y datos relacionados**:
   1. codigoSucursal, codigoFosa → largoFosa, anchoFosa
1. **Autos y datos relacionados**:
   1. patenteAuto → marcaAuto, modeloAuto, dniCliente
1. **Clientes y datos relacionados**:
   1. dniCliente → nombreCliente, celularCliente
1. **Mecánicos y datos relacionados**:
   1. dniMecanico → nombreMecanico, emailMecanico
1. **Relación entre sucursal, fosas, autos y mecánicos**:
   1. codigoSucursal, codigoFosa, patenteAuto → dniMecanico
-----
**2. Identificamos las claves candidatas:**

**Clave candidata del esquema original:**

El esquema original tiene como clave candidata:

- **codigoSucursal, codigoFosa, patenteAuto**, ya que identifica de manera única cada entrada en el esquema dado.

**3. Elegimos justificadamente la clave primaria**

Elegimos como clave primaria **codigoSucursal, codigoFosa, patenteAuto**, ya que:

Es la combinación mínima que identifica de forma única una tupla y respeta las dependencias funcionales y la naturaleza de los datos.

**4. Normalización hasta la Tercera Forma Normal (3FN)**

Para llevar el esquema a la Tercera Forma Normal (3FN), necesitamos eliminar dependencias transitivas y asegurarnos de que cada atributo no clave dependa únicamente de la clave primaria completa. Esto implica dividir la tabla en varias tablas relacionadas para reducir la redundancia y asegurar la integridad de los datos.

PASO 1: El esquema ya está en 1FN porque:

- Todos los atributos son atómicos.
- No hay listas ni conjuntos de valores.

**Paso 2: Segunda Forma Normal (2FN)**

Para llegar a 2FN:

- Eliminamos las dependencias funcionales parciales (atributos dependientes solo de una parte de la clave primaria).

Dividimos el esquema en las siguientes tablas:

1. **Sucursal**
   1. Atributos: codigoSucursal, domicilioSucursal, telefonoSucursal

1. **Fosa**
   1. Atributos: codigoSucursal, codigoFosa, largoFosa, anchoFosa

1. **Auto**
   1. Atributos: patenteAuto, marcaAuto, modeloAuto, dniCliente

1. **Cliente**
   1. Atributos: dniCliente, nombreCliente, celularCliente

1. **Mecánico**
   1. Atributos: dniMecanico, nombreMecanico, emailMecanico

1. **Servicio** (Relación entre sucursal, fosas, autos y mecánicos)
   1. Atributos: codigoSucursal, codigoFosa, patenteAuto, dniMecanico

**Paso 3: Tercera Forma Normal (3FN)**

Para llegar a 3FN:

- Eliminamos las dependencias funcionales transitivas.

Las tablas resultantes no requieren más modificaciones, ya que:

1. Cada atributo no clave depende de forma directa y únicamente de la clave primaria.
1. No hay dependencias transitivas.

**Tablas en 3FN**

**1. Tabla: Sucursal**

**Contiene la información de cada sucursal:**

- **Atributos:**
  - **codigoSucursal (clave primaria): Código único de la sucursal.**
  - **domicilioSucursal: Dirección de la sucursal.**
  - **telefonoSucursal: Teléfono de la sucursal.**

**2. Tabla: Fosa**

**Contiene la información de las fosas asociadas a cada sucursal:**

- **Atributos:**
  - **codigoSucursal (clave foranea): Relación con la tabla Sucursal.**
  - **codigoFosa (clave primaria, dentro de la sucursal): Código único de la fosa dentro de la sucursal.**
  - **largoFosa: Largo de la fosa.**
  - **anchoFosa: Ancho de la fosa.**

**3. Tabla: Auto**

**Registra los autos y su relación con el cliente propietario:**

- **Atributos:**
  - **patenteAuto (clave primaria): Identificador único del auto.**
  - **marcaAuto: Marca del auto.**
  - **modeloAuto: Modelo del auto.**
  - **dniCliente (clave foranea): Relación con la tabla Cliente.**

**4. Tabla: Cliente**

**Guarda la información de los clientes:**

- **Atributos:**
  - **dniCliente (clave primaria): Identificador único del cliente.**
  - **nombreCliente: Nombre del cliente.**
  - **celularCliente: Teléfono celular del cliente.**

**5. Tabla: Mecánico**

**Almacena información sobre los mecánicos:**

- **Atributos:**
  - **dniMecanico (clave primaria): Identificador único del mecánico.**
  - **nombreMecanico: Nombre del mecánico.**
  - **emailMecanico: Correo electrónico del mecánico.**

**6. Tabla: Servicio**

**Relaciona sucursales, fosas, autos y mecánicos:**

- **Atributos:**
  - **codigoSucursal (clave foranea): Relación con la tabla Sucursal.**
  - **codigoFosa (clave foranea): Relación con la tabla Fosa.**
  - **patenteAuto (clave foranea): Relación con la tabla Auto.**
  - **dniMecanico (clave foranea): Relación con la tabla Mecánico.**


