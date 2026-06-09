
-- One row per dataset. For GDC, a "dataset" = a project.
CREATE TABLE datasets (
    dataset_id        TEXT PRIMARY KEY,   -- canonical id, e.g. 'gdc:TCGA-LUAD'
    source            TEXT NOT NULL,      -- where it came from: 'gdc'
    source_dataset_id TEXT NOT NULL,      -- the source's own id: 'TCGA-LUAD'
    title             TEXT,               -- human-readable name
    organism          TEXT,               -- 'Homo sapiens' for all GDC data
    disease           TEXT,               -- representative disease type
    tissue            TEXT,               -- representative primary site
    sample_count      INTEGER,            -- number of distinct cases (derived)
    open_access       BOOLEAN,            -- has open-access files? (derived)
    portal_url        TEXT,               -- link to the dataset (constructed)
    quality_score     REAL,               -- filled in later, in Week 4
    ingested_at       TIMESTAMP DEFAULT now()
);


-- One row per (dataset, assay type). A dataset can have several
-- assays, so they live in their own table linked back to datasets.


CREATE TABLE dataset_assays (
    dataset_id  TEXT NOT NULL REFERENCES datasets(dataset_id),
    assay_type  TEXT NOT NULL,            -- e.g. 'RNA-Seq', 'WXS'
    PRIMARY KEY (dataset_id, assay_type)
);