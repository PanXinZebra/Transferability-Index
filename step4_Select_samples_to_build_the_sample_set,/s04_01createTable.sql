-- Table: public.myobjects

-- DROP TABLE IF EXISTS public.myobjects;

CREATE TABLE IF NOT EXISTS public.myobjects
(
    id bigint NOT NULL,
    v1 character varying COLLATE pg_catalog."default",
    d1 integer,
    d2 integer,
    processed integer,
    d2021 integer,
    d2020 integer,
    d2019 integer,
    d2018 integer,
    ic integer,
    CONSTRAINT objects_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.myobjects
    OWNER to postgres;