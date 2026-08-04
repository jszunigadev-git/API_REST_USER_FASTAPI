--
-- PostgreSQL database dump
--

\restrict fU6lmn7bGidaANZo8H0mUbOSf3HTMWO0bcFShhCwvwPViBZc1Vg0PdQVTkxlObA

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: btree_gist; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS btree_gist WITH SCHEMA public;


--
-- Name: EXTENSION btree_gist; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION btree_gist IS 'support for indexing common datatypes in GiST';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: clase; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clase (
    id integer NOT NULL,
    fecha_hora timestamp without time zone NOT NULL,
    capacidad integer NOT NULL,
    duracion_minutos integer NOT NULL,
    tipo_clase_id integer,
    entrenador_id integer,
    sucursal_id integer,
    CONSTRAINT capacidad_positiva CHECK ((capacidad >= 0)),
    CONSTRAINT duracion_positiva CHECK ((duracion_minutos > 0))
);


ALTER TABLE public.clase OWNER TO postgres;

--
-- Name: clase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clase_id_seq OWNER TO postgres;

--
-- Name: clase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clase_id_seq OWNED BY public.clase.id;


--
-- Name: entrenador; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.entrenador (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    telefono character varying(50) NOT NULL
);


ALTER TABLE public.entrenador OWNER TO postgres;

--
-- Name: entrenador_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.entrenador_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.entrenador_id_seq OWNER TO postgres;

--
-- Name: entrenador_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.entrenador_id_seq OWNED BY public.entrenador.id;


--
-- Name: membresia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.membresia (
    nombre character varying(100) CONSTRAINT producto_nombre_not_null NOT NULL,
    precio integer CONSTRAINT producto_precio_not_null NOT NULL,
    duracion_meses integer NOT NULL,
    id integer NOT NULL,
    CONSTRAINT chk_duracion_meses CHECK ((duracion_meses = ANY (ARRAY[1, 3, 6, 12])))
);


ALTER TABLE public.membresia OWNER TO postgres;

--
-- Name: membresia_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.membresia_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.membresia_id_seq OWNER TO postgres;

--
-- Name: membresia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.membresia_id_seq OWNED BY public.membresia.id;


--
-- Name: plan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan (
    id integer NOT NULL,
    usuario_id integer,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    estado character varying(20) DEFAULT 'activo'::character varying,
    membresia_id integer,
    CONSTRAINT estado_plan_valido CHECK (((estado)::text = ANY ((ARRAY['activo'::character varying, 'vencido'::character varying, 'cancelado'::character varying])::text[]))),
    CONSTRAINT fechas_validas CHECK ((fecha_fin > fecha_inicio))
);


ALTER TABLE public.plan OWNER TO postgres;

--
-- Name: plan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.plan_id_seq OWNER TO postgres;

--
-- Name: plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.plan_id_seq OWNED BY public.plan.id;


--
-- Name: reserva; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reserva (
    usuario_id integer NOT NULL,
    clase_id integer NOT NULL,
    fecha_reserva timestamp without time zone DEFAULT now(),
    estado character varying(20) DEFAULT 'confirmada'::character varying,
    id integer NOT NULL,
    CONSTRAINT chk_estado_valido CHECK (((estado)::text = ANY ((ARRAY['confirmada'::character varying, 'cancelada'::character varying, 'asistió'::character varying])::text[])))
);


ALTER TABLE public.reserva OWNER TO postgres;

--
-- Name: reserva_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reserva_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reserva_id_seq OWNER TO postgres;

--
-- Name: reserva_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reserva_id_seq OWNED BY public.reserva.id;


--
-- Name: sucursal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sucursal (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL
);


ALTER TABLE public.sucursal OWNER TO postgres;

--
-- Name: sucursal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sucursal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sucursal_id_seq OWNER TO postgres;

--
-- Name: sucursal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sucursal_id_seq OWNED BY public.sucursal.id;


--
-- Name: tipo_clase; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipo_clase (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL
);


ALTER TABLE public.tipo_clase OWNER TO postgres;

--
-- Name: tipo_clase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipo_clase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipo_clase_id_seq OWNER TO postgres;

--
-- Name: tipo_clase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipo_clase_id_seq OWNED BY public.tipo_clase.id;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    telefono character varying(50)
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_seq OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;


--
-- Name: clase id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clase ALTER COLUMN id SET DEFAULT nextval('public.clase_id_seq'::regclass);


--
-- Name: entrenador id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.entrenador ALTER COLUMN id SET DEFAULT nextval('public.entrenador_id_seq'::regclass);


--
-- Name: membresia id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membresia ALTER COLUMN id SET DEFAULT nextval('public.membresia_id_seq'::regclass);


--
-- Name: plan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan ALTER COLUMN id SET DEFAULT nextval('public.plan_id_seq'::regclass);


--
-- Name: reserva id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva ALTER COLUMN id SET DEFAULT nextval('public.reserva_id_seq'::regclass);


--
-- Name: sucursal id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sucursal ALTER COLUMN id SET DEFAULT nextval('public.sucursal_id_seq'::regclass);


--
-- Name: tipo_clase id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_clase ALTER COLUMN id SET DEFAULT nextval('public.tipo_clase_id_seq'::regclass);


--
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- Name: clase clase_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clase
    ADD CONSTRAINT clase_pkey PRIMARY KEY (id);


--
-- Name: entrenador entrenador_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.entrenador
    ADD CONSTRAINT entrenador_pkey PRIMARY KEY (id);


--
-- Name: membresia membresia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membresia
    ADD CONSTRAINT membresia_pkey PRIMARY KEY (id);


--
-- Name: plan no_solape_plan_usuario; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan
    ADD CONSTRAINT no_solape_plan_usuario EXCLUDE USING gist (usuario_id WITH =, daterange(fecha_inicio, fecha_fin, '[)'::text) WITH &&) WHERE (((estado)::text = 'activo'::text));


--
-- Name: reserva pk_reserva; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT pk_reserva PRIMARY KEY (id);


--
-- Name: plan plan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan
    ADD CONSTRAINT plan_pkey PRIMARY KEY (id);


--
-- Name: sucursal sucursal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sucursal
    ADD CONSTRAINT sucursal_pkey PRIMARY KEY (id);


--
-- Name: tipo_clase tipo_clase_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_clase
    ADD CONSTRAINT tipo_clase_pkey PRIMARY KEY (id);


--
-- Name: entrenador uq_entrenador_mail; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.entrenador
    ADD CONSTRAINT uq_entrenador_mail UNIQUE (email);


--
-- Name: usuario uq_usuarios_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT uq_usuarios_email UNIQUE (email);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- Name: uq_usuario_clase_activa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uq_usuario_clase_activa ON public.reserva USING btree (usuario_id, clase_id) WHERE ((estado)::text <> 'cancelada'::text);


--
-- Name: clase clase_entrenador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clase
    ADD CONSTRAINT clase_entrenador_id_fkey FOREIGN KEY (entrenador_id) REFERENCES public.entrenador(id);


--
-- Name: clase clase_sucursal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clase
    ADD CONSTRAINT clase_sucursal_id_fkey FOREIGN KEY (sucursal_id) REFERENCES public.sucursal(id);


--
-- Name: clase clase_tipo_clase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clase
    ADD CONSTRAINT clase_tipo_clase_id_fkey FOREIGN KEY (tipo_clase_id) REFERENCES public.tipo_clase(id);


--
-- Name: plan plan_membresia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan
    ADD CONSTRAINT plan_membresia_id_fkey FOREIGN KEY (membresia_id) REFERENCES public.membresia(id);


--
-- Name: plan plan_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan
    ADD CONSTRAINT plan_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: reserva reserva_clase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_clase_id_fkey FOREIGN KEY (clase_id) REFERENCES public.clase(id);


--
-- Name: reserva reserva_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- PostgreSQL database dump complete
--

\unrestrict fU6lmn7bGidaANZo8H0mUbOSf3HTMWO0bcFShhCwvwPViBZc1Vg0PdQVTkxlObA

