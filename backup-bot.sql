toc.dat                                                                                             0000600 0004000 0002000 00000011723 14625437022 0014450 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        PGDMP   :                    |         
   suportmate    16.3    16.3     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false         �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false         �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false         �           1262    16398 
   suportmate    DATABASE     �   CREATE DATABASE suportmate WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';
    DROP DATABASE suportmate;
                postgres    false         �            1259    16409    solucoes    TABLE       CREATE TABLE public.solucoes (
    id integer NOT NULL,
    topico_id integer NOT NULL,
    titulo text NOT NULL,
    solucao_desc text,
    created_at timestamp without time zone NOT NULL,
    modified_at timestamp without time zone,
    image_url text
);
    DROP TABLE public.solucoes;
       public         heap    postgres    false         �            1259    16408    solucoes_id_seq    SEQUENCE     �   CREATE SEQUENCE public.solucoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.solucoes_id_seq;
       public          postgres    false    218         �           0    0    solucoes_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.solucoes_id_seq OWNED BY public.solucoes.id;
          public          postgres    false    217         �            1259    16400    topicos    TABLE     �   CREATE TABLE public.topicos (
    id integer NOT NULL,
    topic text NOT NULL,
    descricao text,
    created_at timestamp without time zone
);
    DROP TABLE public.topicos;
       public         heap    postgres    false         �            1259    16399    topicos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.topicos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.topicos_id_seq;
       public          postgres    false    216         �           0    0    topicos_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.topicos_id_seq OWNED BY public.topicos.id;
          public          postgres    false    215         V           2604    16412    solucoes id    DEFAULT     j   ALTER TABLE ONLY public.solucoes ALTER COLUMN id SET DEFAULT nextval('public.solucoes_id_seq'::regclass);
 :   ALTER TABLE public.solucoes ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217    218         U           2604    16403 
   topicos id    DEFAULT     h   ALTER TABLE ONLY public.topicos ALTER COLUMN id SET DEFAULT nextval('public.topicos_id_seq'::regclass);
 9   ALTER TABLE public.topicos ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216         �          0    16409    solucoes 
   TABLE DATA           k   COPY public.solucoes (id, topico_id, titulo, solucao_desc, created_at, modified_at, image_url) FROM stdin;
    public          postgres    false    218       4846.dat �          0    16400    topicos 
   TABLE DATA           C   COPY public.topicos (id, topic, descricao, created_at) FROM stdin;
    public          postgres    false    216       4844.dat �           0    0    solucoes_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.solucoes_id_seq', 8, true);
          public          postgres    false    217         �           0    0    topicos_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.topicos_id_seq', 9, true);
          public          postgres    false    215         Z           2606    16416    solucoes solucoes_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.solucoes
    ADD CONSTRAINT solucoes_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.solucoes DROP CONSTRAINT solucoes_pkey;
       public            postgres    false    218         X           2606    16407    topicos topicos_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.topicos
    ADD CONSTRAINT topicos_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.topicos DROP CONSTRAINT topicos_pkey;
       public            postgres    false    216         [           2606    16417     solucoes solucoes_topico_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.solucoes
    ADD CONSTRAINT solucoes_topico_id_fkey FOREIGN KEY (topico_id) REFERENCES public.topicos(id);
 J   ALTER TABLE ONLY public.solucoes DROP CONSTRAINT solucoes_topico_id_fkey;
       public          postgres    false    218    216    4696                                                     4846.dat                                                                                            0000600 0004000 0002000 00000005672 14625437022 0014276 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        2	4	Rejeição E051	Verificar IE do cliente, verificar se é isento.	2024-05-15 08:49:09.68445	2024-05-15 08:49:09.68445	https://media.discordapp.net/attachments/1209544390859816993/1240269145426231316/image.png?ex=6645f227&is=6644a0a7&hm=cd1381e47105e6ca3b9cffb45652070adf281e7f73995f5467dcdbacc271b981&=&format=webp&quality=lossless&width=983&height=662;https://media.discordapp.net/attachments/1209544390859816993/1240269288124710984/0732771f136b794a962492cc1fac136245f4b288.png?ex=6645f249&is=6644a0c9&hm=53baf0baa08d2dbe8ee8af60e337e46aa80f5cfb85210e78281df01e0a234b93&=&format=webp&quality=lossless&width=883&height=662
3	6	Erro: coluna gcotb006 produto.t006 caminho não existe administrar produtos	Rodar script no banco de dados: ````-- Column: t006_caminho  -- ALTER TABLE gcotb006_produto DROP COLUMN t006_caminho;  ALTER TABLE gcotb006_produto ADD COLUMN t006_caminho character varying(255);```	2024-05-16 11:20:47.009962	2024-05-16 11:20:47.009962	https://media.discordapp.net/attachments/1209544390859816993/1240668645013586020/6f74112a61edc6371547be77f05a0b638cec78d4.jpeg?ex=66476637&is=664614b7&hm=3395cf2fb12bbe88d73a20759ba95921d2557ea5e28bfed37b1a6e5754308d05&=&format=webp&width=1177&height=662
4	7	Erro não Especificado	Tente reiniciar o node.	2024-05-17 08:54:05.559997	2024-05-17 08:54:05.559997	https://media.discordapp.net/attachments/897846061987668049/1240989957166731405/image.png?ex=66489176&is=66473ff6&hm=29485b3b995deefb0811a75ce9e10b6ec36c582a03f7a227f5764983704a4de6&=&format=webp&quality=lossless&width=1440&height=658
5	8	Senhas Banco de Dados	.Sis365!@#2210ç sis365!@# .sis365!@# .Sis365!@#2210. gcom!@#	2024-05-27 11:32:04.046865	2024-05-27 11:32:04.046865	.
6	9	Cadastro de Ticket - Milvus	Segue video com o passo a passo para a criação de ticket na plataforma: https://www.loom.com/share/b9ea7f2649ae49f88e01047b5689d69f?sid=ff996c0f-6413-4829-9c9b-d20a7d6d70ff	2024-05-28 08:44:14.079603	2024-05-28 08:44:14.079603	.
7	5	Inserir Informações Adicionais NFe (Procon)	Siga para manutenção de Empresa, 4° aba, opção para texto para NFE.	2024-05-28 12:18:29.396428	2024-05-28 12:18:29.396428	https://media.discordapp.net/attachments/897846061987668049/1245026534125731860/image.png?ex=665740d1&is=6655ef51&hm=73432bd9a283ad3f51ea432b618f30288342015bb5764160ed5f98536c2e5a72&=&format=webp&quality=lossless&width=913&height=662
8	1	Inserir Informações Adicionais NFC (Procon)	Siga para tela de configurar PDV, canto inferior	2024-05-28 12:40:27.080539	2024-05-28 12:40:27.080539	https://media.discordapp.net/attachments/897846061987668049/1098609416003125388/image.png?ex=6657353f&is=6655e3bf&hm=702888c727669356a13fa07c437d278fdefb511908338bae5512f120b971730f&=&format=webp&quality=lossless&width=1056&height=498;https://media.discordapp.net/attachments/1209544390859816993/1245038761834971166/image.png?ex=66574c34&is=6655fab4&hm=6e8fe2feafdbc177cfbb54a642af7169ed895ae99894ccd47bbc3733972ad594&=&format=webp&quality=lossless&width=1101&height=662
\.


                                                                      4844.dat                                                                                            0000600 0004000 0002000 00000000516 14625437022 0014264 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        3	Impressora	\N	\N
1	Rejeições NFC	\N	\N
4	Rejeições NFS	\N	2024-05-15 08:46:04.562964
5	Rejeições NFe	\N	2024-05-16 08:36:00.660902
6	Erro Coluna SQL	\N	2024-05-16 11:18:03.887547
7	Erro Inicialização do Sistema	\N	2024-05-17 08:46:04.814308
8	Senhas	\N	2024-05-27 11:31:20.651043
9	Milvus	\N	2024-05-27 19:35:05.305906
\.


                                                                                                                                                                                  restore.sql                                                                                         0000600 0004000 0002000 00000011060 14625437022 0015367 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        --
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

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

DROP DATABASE suportmate;
--
-- Name: suportmate; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE suportmate WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';


ALTER DATABASE suportmate OWNER TO postgres;

\connect suportmate

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
-- Name: solucoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.solucoes (
    id integer NOT NULL,
    topico_id integer NOT NULL,
    titulo text NOT NULL,
    solucao_desc text,
    created_at timestamp without time zone NOT NULL,
    modified_at timestamp without time zone,
    image_url text
);


ALTER TABLE public.solucoes OWNER TO postgres;

--
-- Name: solucoes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.solucoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.solucoes_id_seq OWNER TO postgres;

--
-- Name: solucoes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.solucoes_id_seq OWNED BY public.solucoes.id;


--
-- Name: topicos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.topicos (
    id integer NOT NULL,
    topic text NOT NULL,
    descricao text,
    created_at timestamp without time zone
);


ALTER TABLE public.topicos OWNER TO postgres;

--
-- Name: topicos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.topicos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.topicos_id_seq OWNER TO postgres;

--
-- Name: topicos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.topicos_id_seq OWNED BY public.topicos.id;


--
-- Name: solucoes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solucoes ALTER COLUMN id SET DEFAULT nextval('public.solucoes_id_seq'::regclass);


--
-- Name: topicos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.topicos ALTER COLUMN id SET DEFAULT nextval('public.topicos_id_seq'::regclass);


--
-- Data for Name: solucoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.solucoes (id, topico_id, titulo, solucao_desc, created_at, modified_at, image_url) FROM stdin;
\.
COPY public.solucoes (id, topico_id, titulo, solucao_desc, created_at, modified_at, image_url) FROM '$$PATH$$/4846.dat';

--
-- Data for Name: topicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.topicos (id, topic, descricao, created_at) FROM stdin;
\.
COPY public.topicos (id, topic, descricao, created_at) FROM '$$PATH$$/4844.dat';

--
-- Name: solucoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.solucoes_id_seq', 8, true);


--
-- Name: topicos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.topicos_id_seq', 9, true);


--
-- Name: solucoes solucoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solucoes
    ADD CONSTRAINT solucoes_pkey PRIMARY KEY (id);


--
-- Name: topicos topicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.topicos
    ADD CONSTRAINT topicos_pkey PRIMARY KEY (id);


--
-- Name: solucoes solucoes_topico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solucoes
    ADD CONSTRAINT solucoes_topico_id_fkey FOREIGN KEY (topico_id) REFERENCES public.topicos(id);


--
-- PostgreSQL database dump complete
--

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                