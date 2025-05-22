USE agent_metadata;
GO

-- View to easily browse all table lineages
CREATE VIEW vw_TableLineageSummary AS
SELECT
    tl.Id AS LineageId,
    tl.SourceTable,
    tl.TargetTable,
    tl.LineageType,
    ISNULL(lr.RequiresReview, 0) AS RequiresReview,
    lr.ReviewedBy,
    lr.ReviewedAt,
    tl.Notes,
    tl.CreatedAt
FROM TableLineage tl
LEFT JOIN LineageReviewStatus lr ON tl.Id = lr.LineageId;
GO

-- View to inspect detailed column mappings for each lineage
CREATE VIEW vw_ColumnMappingDetail AS
SELECT
    tl.SourceTable,
    tl.TargetTable,
    cm.SourceColumn,
    cm.TargetColumn,
    cm.Transformation,
    cm.ConfidenceScore,
    cm.CreatedAt
FROM ColumnMapping cm
JOIN TableLineage tl ON cm.LineageId = tl.Id;
GO

-- View for auditing all natural language queries to the agent
CREATE VIEW vw_AgentQueryLog AS
SELECT
    Id,
    Username,
    QueryText,
    LEFT(ResponseText, 500) AS ResponseSnippet, -- truncate for overview
    Timestamp
FROM AgentQueryLog;
GO

CREATE VIEW vw_SourceSystems AS
SELECT
    Id, Name, Type, IsActive, Notes
FROM SourceSystems;
GO

Example
INSERT INTO SourceSystems (Name, Type, ConnectionString, Notes)
VALUES (
    'CRM_Oracle_Prod',
    'oracle',
    'oracle+cx_oracle://user:pass@host:1521/?service_name=svc',
    'Production CRM Oracle server'
);