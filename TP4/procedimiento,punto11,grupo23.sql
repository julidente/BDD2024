DELIMITER //

CREATE PROCEDURE GenerarResumenDiario()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE linea_produccion VARCHAR(50);
    DECLARE fecha_produccion DATE;
    DECLARE total_producido INT;

    DECLARE cur_produccion CURSOR FOR 
        SELECT LineaProduccion, FechaProduccion, SUM(CantidadProducida) 
        FROM Produccion 
        GROUP BY LineaProduccion, FechaProduccion;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error durante la generación del resumen diario' AS Mensaje;
    END;

    START TRANSACTION;

    TRUNCATE TABLE ResumenProduccion; 

    OPEN cur_produccion;

    read_loop: LOOP
        FETCH cur_produccion INTO linea_produccion, fecha_produccion, total_producido;
        IF done THEN 
            LEAVE read_loop;
        END IF;

        INSERT INTO ResumenProduccion (LineaProduccion, FechaProduccion, TotalProducido) 
        VALUES (linea_produccion, fecha_produccion, total_producido);
    END LOOP;

    CLOSE cur_produccion;

    COMMIT;
END //

DELIMITER ;