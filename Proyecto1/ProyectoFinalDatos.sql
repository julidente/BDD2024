-- Datos iniciales para la tabla Usuarios
INSERT INTO Usuarios (Nombre, Email, FechaRegistro, CuotaMensual) VALUES
('Juan Pérez', 'juan.perez@example.com', '2023-01-15', 500.00),
('María López', 'maria.lopez@example.com', '2023-02-10', 500.00),
('Carlos Gómez', 'carlos.gomez@example.com', '2022-11-05', 450.00),
('Ana Martínez', 'ana.martinez@example.com', '2022-12-01', 500.00),
('Pedro Fernández', 'pedro.fernandez@example.com', '2023-04-18', 480.00),
('Sofía Díaz', 'sofia.diaz@example.com', '2023-05-10', 500.00),
('Luis Vargas', 'luis.vargas@example.com', '2023-06-01', 470.00),
('Elena Navarro', 'elena.navarro@example.com', '2023-03-23', 490.00),
('Diego Sánchez', 'diego.sanchez@example.com', '2023-07-15', 500.00),
('Laura Torres', 'laura.torres@example.com', '2023-08-20', 480.00);

-- Datos iniciales para la tabla Libros
INSERT INTO Libros (Titulo, Autor, AñoPublicacion, Disponibles) VALUES
('Cien Años de Soledad', 'Gabriel García Márquez', 1967, 5),
('Don Quijote de la Mancha', 'Miguel de Cervantes', 1605, 3),
('1984', 'George Orwell', 1949, 4),
('El Principito', 'Antoine de Saint-Exupéry', 1943, 6),
('Crimen y Castigo', 'Fiódor Dostoyevski', 1866, 2),
('Orgullo y Prejuicio', 'Jane Austen', 1813, 4),
('El Gran Gatsby', 'F. Scott Fitzgerald', 1925, 3),
('Los Juegos del Hambre', 'Suzanne Collins', 2008, 7),
('Harry Potter y la Piedra Filosofal', 'J.K. Rowling', 1997, 8),
('El Señor de los Anillos', 'J.R.R. Tolkien', 1954, 3);

-- Datos iniciales para la tabla Prestamos
INSERT INTO Prestamos (IDUsuario, IDLibro, FechaPrestamo, FechaDevolucionEsperada) VALUES
(1, 1, '2023-10-01', '2023-10-15'),
(2, 2, '2023-09-15', '2023-09-29'),
(3, 3, '2023-09-20', '2023-10-04'),
(4, 4, '2023-10-10', '2023-10-24'),
(5, 5, '2023-10-15', '2023-10-29'),
(6, 6, '2023-08-05', '2023-08-19'),
(7, 7, '2023-07-22', '2023-08-05'),
(8, 8, '2023-09-01', '2023-09-15'),
(9, 9, '2023-08-18', '2023-09-01'),
(10, 10, '2023-07-30', '2023-08-13');

-- Datos iniciales para la tabla Pagos
INSERT INTO Pagos (IDUsuario, Mes, Año, FechaPago, Monto) VALUES
(1, 10, 2023, '2023-10-01', 500.00),
(2, 9, 2023, '2023-09-05', 500.00),
(3, 9, 2023, '2023-09-10', 450.00),
(4, 9, 2023, '2023-09-15', 500.00),
(5, 8, 2023, '2023-08-20', 480.00),
(6, 8, 2023, '2023-08-10', 500.00),
(7, 7, 2023, '2023-07-05', 470.00),
(8, 9, 2023, '2023-09-25', 490.00),
(9, 8, 2023, '2023-08-15', 500.00),
(10, 7, 2023, '2023-07-20', 480.00);

-- Datos iniciales para la tabla Multas 
INSERT INTO Multas (IDPrestamo, Monto, FechaMulta) VALUES
(3, 45.00, '2023-10-10'),  -- El usuario 3 devolvió con retraso
(5, 30.00, '2023-11-01'),  -- El usuario 5 devolvió con retraso
(7, 28.20, '2023-08-10');  -- El usuario 7 devolvió con retraso

-- Actualizar la tabla Prestamos para incluir FechaDevolucion y reflejar las multas 
UPDATE Prestamos SET FechaDevolucion = '2023-10-18' WHERE ID = 3;  -- Devolución con retraso
UPDATE Prestamos SET FechaDevolucion = '2023-11-05' WHERE ID = 5;  -- Devolución con retraso
UPDATE Prestamos SET FechaDevolucion = '2023-08-10' WHERE ID = 7;  -- Devolución con retraso

-- Crear índices para optimizar consultas

-- Índice en la columna Titulo de la tabla Libros para búsquedas rápidas por título
CREATE INDEX idx_libros_titulo ON Libros(Titulo);

-- Índice combinado en las columnas Mes y Año de la tabla Pagos para consultas por período
CREATE INDEX idx_pagos_mes_anio ON Pagos(Mes, Año);

-- Índice en la columna IDUsuario de la tabla Prestamos para consultas de préstamos por usuario
CREATE INDEX idx_prestamos_idusuario ON Prestamos(IDUsuario);

-- Índice en la columna IDLibro de la tabla Prestamos para consultas de préstamos por libro
CREATE INDEX idx_prestamos_idlibro ON Prestamos(IDLibro);

-- Índice en la columna Autor de la tabla Libros (
CREATE INDEX idx_libros_autor ON Libros(Autor);