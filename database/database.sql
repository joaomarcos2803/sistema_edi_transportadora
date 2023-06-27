CREATE TABLE IF NOT EXISTS public.client_address
(
    id integer NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    phone character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street character varying(60) COLLATE pg_catalog."default" NOT NULL,
    city character varying(40) COLLATE pg_catalog."default" NOT NULL,
    cep character varying(20) COLLATE pg_catalog."default" NOT NULL,
    district character varying(50) COLLATE pg_catalog."default" NOT NULL,
    "number" integer NOT NULL,
    complement character varying(60) COLLATE pg_catalog."default",
    CONSTRAINT client_address_pkey PRIMARY KEY (id),
    CONSTRAINT client_address_name_key UNIQUE (name)
)

CREATE TABLE IF NOT EXISTS public.services
(
    id integer NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    phone character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street character varying(80) COLLATE pg_catalog."default" NOT NULL,
    complement character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "number" integer NOT NULL,
    district character varying(50) COLLATE pg_catalog."default" NOT NULL,
    city character varying(80) COLLATE pg_catalog."default" NOT NULL,
    postal_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT services_pkey PRIMARY KEY (id),
    CONSTRAINT services_name_key UNIQUE (name)
)

CREATE TABLE IF NOT EXISTS public.transport_order
(
    id integer NOT NULL DEFAULT nextval('transport_order_id_seq'::regclass),
    package_code character varying(50) COLLATE pg_catalog."default" NOT NULL,
    created_at date DEFAULT now(),
    delivery_time integer NOT NULL,
    status status_type NOT NULL,
    client_address_id integer NOT NULL,
    service_id integer NOT NULL,
    CONSTRAINT transport_order_pkey PRIMARY KEY (id),
    CONSTRAINT transport_order_package_code_key UNIQUE (package_code),
    CONSTRAINT fk_client_address FOREIGN KEY (client_address_id)
        REFERENCES public.client_address (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT fk_service FOREIGN KEY (service_id)
        REFERENCES public.services (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TYPE public.status_type AS ENUM
('Awaiting Collection', 'Send', 'In Transport', 'Delivered', 'Canceled');


INSERT INTO services(id, name, phone, street, complement, number, district, city, postal_code)
VALUES 
(1, 'PAC', '1199999999', 'Rua do PAC', 'Complemento do PAC', 123, 'Bairro do PAC', 'Cidade do PAC', '12345678'),
(2, 'SEDEX', '1199999999', 'Rua do SEDEX', 'Complemento do SEDEX', 456, 'Bairro do SEDEX', 'Cidade do SEDEX', '87654321')