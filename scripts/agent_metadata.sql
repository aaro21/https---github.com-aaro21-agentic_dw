CREATE TABLE SourceSystems (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255) UNIQUE NOT NULL,         -- e.g., 'CRM_SQL_Prod'
    Type NVARCHAR(50) NOT NULL,                 -- 'sqlserver' or 'oracle'
    AuthMode NVARCHAR(50) NOT NULL DEFAULT 'alias', -- 'alias', 'trusted'
    ConnectionAlias NVARCHAR(255) NOT NULL,     -- maps to env variable or external secret
    Notes NVARCHAR(MAX),
    IsActive BIT DEFAULT 1
);