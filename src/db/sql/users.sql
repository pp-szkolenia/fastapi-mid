CREATE TABLE IF NOT EXISTS public.users
(
    id serial,
    username character varying(20) NOT NULL,
    password character varying(30) NOT NULL,
    is_admin boolean NOT NULL DEFAULT false,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)