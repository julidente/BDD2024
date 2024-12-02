-- Creación de la tabla Usuarios
CREATE TABLE Usuarios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    FechaRegistro DATE NOT NULL,
    CuotaMensual DECIMAL(10, 2) NOT NULL CHECK (CuotaMensual > 0)
);

-- Creación de la tabla Libros
CREATE TABLE Libros (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Titulo VARCHAR(200) NOT NULL,
    Autor VARCHAR(100) NOT NULL,
    AñoPublicacion INT CHECK (AñoPublicacion >= 1000 AND AñoPublicacion <= YEAR(CURDATE())),
    Disponibles INT NOT NULL CHECK (Disponibles >= 0)
);

-- Creación de la tabla Prestamos
CREATE TABLE Prestamos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    IDUsuario INT NOT NULL,
    IDLibro INT NOT NULL,
    FechaPrestamo DATE NOT NULL,
    FechaDevolucionEsperada DATE NOT NULL,
    FechaDevolucion DATE,
    FOREIGN KEY (IDUsuario) REFERENCES Usuarios(ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (IDLibro) REFERENCES Libros(ID) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Creación de la tabla Pagos
CREATE TABLE Pagos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    IDUsuario INT NOT NULL,
    Mes INT NOT NULL CHECK (Mes BETWEEN 1 AND 12),
    Año INT NOT NULL CHECK (Año >= 2000),
    FechaPago DATE NOT NULL,
    Monto DECIMAL(10, 2) NOT NULL CHECK (Monto > 0),
    FOREIGN KEY (IDUsuario) REFERENCES Usuarios(ID) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Creación de la tabla Multas
CREATE TABLE Multas (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    IDPrestamo INT NOT NULL,
    Monto DECIMAL(10, 2) NOT NULL CHECK (Monto > 0),
    FechaMulta DATE NOT NULL,
    FOREIGN KEY (IDPrestamo) REFERENCES Prestamos(ID) ON DELETE RESTRICT ON UPDATE CASCADE
);