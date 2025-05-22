-- Database: agent_metadata (or your preferred name)
CREATE DATABASE agent_metadata;
GO
USE agent_metadata;
GO

-- Table for logging user queries to the agent
CREATE TABLE AgentQueryLog (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(255),
    QueryText NVARCHAR(MAX),
    ResponseText NVARCHAR(MAX),
    Timestamp DATETIME DEFAULT GETDATE()
);
GO

-- Table to store table-level lineage
CREATE TABLE TableLineage (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    SourceTable NVARCHAR(255),
    TargetTable NVARCHAR(255),
    LineageType NVARCHAR(50), -- 'bronze-to-silver', 'silver-to-gold'
    Notes NVARCHAR(MAX),
    CreatedAt DATETIME DEFAULT GETDATE()
);
GO

-- Table to store detailed column-level mappings
CREATE TABLE ColumnMapping (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    LineageId INT FOREIGN KEY REFERENCES TableLineage(Id),
    SourceColumn NVARCHAR(255),
    TargetColumn NVARCHAR(255),
    Transformation NVARCHAR(MAX), -- raw SQL or expression
    ConfidenceScore FLOAT, -- optional heuristic
    CreatedAt DATETIME DEFAULT GETDATE()
);
GO

-- Table for manual overrides or marking complex joins
CREATE TABLE LineageReviewStatus (
    LineageId INT PRIMARY KEY,
    RequiresReview BIT DEFAULT 0,
    ReviewedBy NVARCHAR(255),
    ReviewedAt DATETIME NULL,
    Notes NVARCHAR(MAX)
);
GO