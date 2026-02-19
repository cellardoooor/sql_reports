CREATE TABLE incidents (
    id INT IDENTITY(1,1) PRIMARY KEY,
    created_at DATETIME2 DEFAULT GETDATE(),
    fio NVARCHAR(255) NOT NULL,
    event_datetime DATETIME2 NOT NULL DEFAULT GETDATE(),
    tag NVARCHAR(50) NOT NULL CHECK (tag IN ('Мониторинг', 'Латенси', 'Информация', 'Массовое', 'ОТМ', 'Veeam')),
    validity_hours INT NOT NULL,
    event_description NVARCHAR(MAX),
    engineer_actions NVARCHAR(MAX)
);

CREATE INDEX idx_event_datetime ON incidents(event_datetime);
CREATE INDEX idx_tag ON incidents(tag);
