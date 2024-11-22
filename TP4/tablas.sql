
CREATE TABLE Produccion (
    ProduccionId INT PRIMARY KEY IDENTITY(1,1),  
    LineaProduccion VARCHAR(50) NOT NULL,        
    FechaProduccion DATE NOT NULL,               
    CantidadProducida INT NOT NULL               
);


CREATE TABLE ResumenProduccion (
    ResumenId INT PRIMARY KEY IDENTITY(1,1),     
    LineaProduccion VARCHAR(50) NOT NULL,        
    FechaProduccion DATE NOT NULL,               
    TotalProducido INT NOT NULL 
);                 