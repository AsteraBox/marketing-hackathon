--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin (
    username text,
    password text
);

-- Inserting a user record
INSERT INTO public.admin (username, password) VALUES ('admin', 'adminpass');


ALTER TABLE public.admin OWNER TO postgres;

--
-- Name: info_text; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.info_text (
    id integer NOT NULL,
    json_input json,
    text text,
    result boolean
);


ALTER TABLE public.info_text OWNER TO postgres;

--
-- Name: info_text_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.info_text_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.info_text_id_seq OWNER TO postgres;

--
-- Name: info_text_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.info_text_id_seq OWNED BY public.info_text.id;


--
-- Name: info_text id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.info_text ALTER COLUMN id SET DEFAULT nextval('public.info_text_id_seq'::regclass);


--
-- PostgreSQL database dump complete
--

