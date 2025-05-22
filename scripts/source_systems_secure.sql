USE agent_metadata;
GO

-- Secure source systems table with alias-based connection lookup
CREATE TABLE SourceSystems (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255) UNIQUE NOT NULL,         -- e.g., 'CRM_SQL_Prod'
    Type NVARCHAR(50) NOT NULL,                 -- 'sqlserver', 'oracle', etc.
    AuthMode NVARCHAR(50) NOT NULL DEFAULT 'alias', -- 'alias', 'trusted'
    ConnectionAlias NVARCHAR(255) NOT NULL,     -- env var or secret alias
    Notes NVARCHAR(MAX),
    IsActive BIT DEFAULT 1
);
GO

-- View to safely list source systems (no passwords or actual conn strings exposed)
CREATE VIEW vw_SourceSystems AS
SELECT
    Id, Name, Type, AuthMode, ConnectionAlias, IsActive, Notes
FROM SourceSystems;
GO