DELIMITER $$

CREATE PROCEDURE RegistrarPrestamo(
    IN p_IDUsuario INT,
    IN p_IDLibro INT,
    IN p_FechaPrestamo DATE,
    IN p_FechaDevolucionEsperada DATE
)
BEGIN
    -- Variables locales
    DECLARE v_Disponibles INT;
    DECLARE v_ErrorMensaje VARCHAR(255);

    -- Manejador de errores
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- En caso de error, se revierte la transacción y se muestra un mensaje
        ROLLBACK;
        SELECT 'Error al registrar el préstamo.';
    END;

    START TRANSACTION;

    -- Verificar si el libro tiene ejemplares disponibles
    SELECT Disponibles INTO v_Disponibles
    FROM Libros
    WHERE ID = p_IDLibro
    FOR UPDATE;

    IF v_Disponibles IS NULL THEN
        -- Si el libro no existe
        ROLLBACK;
        SELECT 'El libro no existe.';
    ELSEIF v_Disponibles <= 0 THEN
        -- Si no hay ejemplares disponibles
        ROLLBACK;
        SELECT 'No hay ejemplares disponibles de este libro.';
    ELSE
        -- Disminuir la cantidad de ejemplares disponibles
        UPDATE Libros
        SET Disponibles = Disponibles - 1
        WHERE ID = p_IDLibro;

        -- Registrar el préstamo
        INSERT INTO Prestamos (IDUsuario, IDLibro, FechaPrestamo, FechaDevolucionEsperada)
        VALUES (p_IDUsuario, p_IDLibro, p_FechaPrestamo, p_FechaDevolucionEsperada);

        COMMIT;
        SELECT 'Préstamo registrado correctamente.';
    END IF;
END$$

DELIMITER ;

-- Procedimiento para Registrar Devolución

DELIMITER $$

CREATE PROCEDURE RegistrarDevolucion(
    IN p_IDPrestamo INT,
    IN p_FechaDevolucion DATE
)
BEGIN
    -- Variables locales
    DECLARE v_IDLibro INT;
    DECLARE v_IDUsuario INT;
    DECLARE v_FechaDevolucionEsperada DATE;
    DECLARE v_CuotaMensual DECIMAL(10,2);
    DECLARE v_DiasRetraso INT;
    DECLARE v_Multa DECIMAL(10,2);
    DECLARE v_ErrorMensaje VARCHAR(255);

    -- Manejador de errores
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- En caso de error, se revierte la transacción y se muestra un mensaje
        ROLLBACK;
        SELECT 'Error al registrar la devolución.';
    END;

    START TRANSACTION;

    -- Obteniene información del préstamo
    SELECT IDLibro, IDUsuario, FechaDevolucionEsperada INTO v_IDLibro, v_IDUsuario, v_FechaDevolucionEsperada
    FROM Prestamos
    WHERE ID = p_IDPrestamo AND FechaDevolucion IS NULL
    FOR UPDATE;

    IF v_IDLibro IS NULL THEN
        -- Si el préstamo no existe o ya fue devuelto
        ROLLBACK;
        SELECT 'El préstamo no existe o ya ha sido devuelto.';
    ELSE
        -- Actualizo la fecha de devolución del préstamo
        UPDATE Prestamos
        SET FechaDevolucion = p_FechaDevolucion
        WHERE ID = p_IDPrestamo;

        -- Aumenta la cantidad de ejemplares disponibles del libro
        UPDATE Libros
        SET Disponibles = Disponibles + 1
        WHERE ID = v_IDLibro;

        -- Calcular días de retraso
        SET v_DiasRetraso = DATEDIFF(p_FechaDevolucion, v_FechaDevolucionEsperada);

        IF v_DiasRetraso > 0 THEN
            -- Obtener la cuota mensual del usuario
            SELECT CuotaMensual INTO v_CuotaMensual
            FROM Usuarios
            WHERE ID = v_IDUsuario;

            -- Calcular la multa utilizando la función CalcularMulta
            SET v_Multa = CalcularMulta(v_CuotaMensual, v_DiasRetraso);

            COMMIT;
            SELECT CONCAT('El usuario tiene un retraso de ', v_DiasRetraso, ' días. Multa: $', FORMAT(v_Multa, 2));
        ELSE
            COMMIT;
            SELECT 'Devolución realizada sin retrasos.';
        END IF;
    END IF;
END$$

DELIMITER ;

-- Función para Calcular Multa

DELIMITER $$

CREATE FUNCTION CalcularMulta(
    p_CuotaMensual DECIMAL(10,2),
    p_DiasRetraso INT
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    -- Calcula la multa como el 3% de la cuota mensual por día de retraso
    RETURN ROUND(p_DiasRetraso * (p_CuotaMensual * 0.03), 2);
END$$

DELIMITER ;

-- ========================================
-- Procedimiento para Modificar Cuota Mensual
-- ========================================
DELIMITER $$

CREATE PROCEDURE ModificarCuotaMensual(
    IN p_IDUsuario INT,
    IN p_NuevaCuota DECIMAL(10,2)
)
BEGIN
    DECLARE v_FilasAfectadas INT;

    UPDATE Usuarios
    SET CuotaMensual = p_NuevaCuota
    WHERE ID = p_IDUsuario;

    SET v_FilasAfectadas = ROW_COUNT();

    IF v_FilasAfectadas > 0 THEN
        SELECT CONCAT('La cuota mensual del usuario con ID ', p_IDUsuario, ' ha sido actualizada a $', FORMAT(p_NuevaCuota, 2));
    ELSE
        SELECT 'No se encontró el usuario o no se pudo actualizar la cuota mensual.';
    END IF;
END$$

DELIMITER ;


-- Procedimiento para Reporte de Promedio de Meses Impagos

DELIMITER $$

CREATE PROCEDURE ReportePromedioMesesImpagos()
BEGIN
    -- Variable para almacenar el promedio
    DECLARE v_PromedioMesesImpagos DECIMAL(10,2);

    -- Crea tabla temporal para almacenar los meses impagos de cada usuario
    CREATE TEMPORARY TABLE TempMesesImpagos AS
    SELECT 
        u.ID,
        u.Nombre,
        u.Email,
        TIMESTAMPDIFF(MONTH,
            IFNULL(
                (SELECT MAX(STR_TO_DATE(CONCAT(p.Año, '-', p.Mes, '-01'), '%Y-%m-%d'))
                 FROM Pagos p WHERE p.IDUsuario = u.ID),
                u.FechaRegistro
            ),
            CURDATE()
        ) AS MesesImpagos
    FROM Usuarios u;

    -- Calcular el promedio
    SELECT AVG(MesesImpagos) INTO v_PromedioMesesImpagos FROM TempMesesImpagos;

    -- Mostrar el promedio
    SELECT CONCAT('Promedio de meses impagos por los socios: ', FORMAT(v_PromedioMesesImpagos, 2), ' meses.') AS Promedio;

    -- Mostrar detalles de los usuarios con cuotas impagas
    SELECT ID, Nombre, Email, MesesImpagos
    FROM TempMesesImpagos
    WHERE MesesImpagos > 0;

    -- Eliminar la tabla temporal
    DROP TEMPORARY TABLE TempMesesImpagos;
END$$

DELIMITER ;