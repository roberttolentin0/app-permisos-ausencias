PGDMP      ,                |            db_permisos    16.1    16.1 #               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    49479    db_permisos    DATABASE     }   CREATE DATABASE db_permisos WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Peru.1252';
    DROP DATABASE db_permisos;
                postgres    false            �            1255    49480 1   fun_get_last_permission_by_dni(character varying)    FUNCTION     �  CREATE FUNCTION public.fun_get_last_permission_by_dni(dni_input character varying) RETURNS TABLE(id integer, dni character varying, permission_date date, start_time time without time zone, return_time time without time zone, reason character varying, status character varying, observation text, validator_id integer, created_at date, updated_at date, end_time time without time zone)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY 
    SELECT p.id, p.dni::VARCHAR, p.permission_date, p.start_time, p.return_time, p.reason, p.status, p.observation, p.validator_id, p.created_at, p.updated_at, p.end_time
    FROM public.permissions p
    WHERE p.dni = dni_input 
    ORDER BY p.id DESC
    LIMIT 1;
END;
$$;
 R   DROP FUNCTION public.fun_get_last_permission_by_dni(dni_input character varying);
       public          postgres    false            �            1255    49481 -   get_last_permission_by_dni(character varying) 	   PROCEDURE     �  CREATE PROCEDURE public.get_last_permission_by_dni(IN dni_input character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    id_output INT;
    dni_output VARCHAR;
    permission_date_output DATE;
    start_time_output TIME;
    return_time_output TIME;
    reason_output TEXT;
    status_output VARCHAR;
    observation_output TEXT;
    validator_id_output INT;
    created_at_output TIMESTAMP;
    updated_at_output TIMESTAMP;
    end_time_output TIME;
BEGIN
    SELECT id, dni, permission_date, start_time, return_time, reason, status, observation, validator_id, created_at, updated_at, end_time
    INTO STRICT 
        id_output, dni_output, permission_date_output, start_time_output, return_time_output, reason_output, status_output, observation_output, validator_id_output, created_at_output, updated_at_output, end_time_output
    FROM public.permissions 
    WHERE dni = dni_input 
    ORDER BY id DESC
    LIMIT 1;
END;
$$;
 R   DROP PROCEDURE public.get_last_permission_by_dni(IN dni_input character varying);
       public          postgres    false            �            1259    49482    permission_details    TABLE     �   CREATE TABLE public.permission_details (
    id integer NOT NULL,
    permission_id integer NOT NULL,
    reason character varying(60),
    return_time time without time zone,
    created_at date
);
 &   DROP TABLE public.permission_details;
       public         heap    postgres    false            �            1259    49485    additional_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.additional_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.additional_permissions_id_seq;
       public          postgres    false    215                       0    0    additional_permissions_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.additional_permissions_id_seq OWNED BY public.permission_details.id;
          public          postgres    false    216            �            1259    49486 	   employees    TABLE     f   CREATE TABLE public.employees (
    dni character(8) NOT NULL,
    full_name character varying(60)
);
    DROP TABLE public.employees;
       public         heap    postgres    false            �            1259    49489    permissions    TABLE     �  CREATE TABLE public.permissions (
    id integer NOT NULL,
    dni character(8) NOT NULL,
    permission_date date,
    start_time time without time zone,
    return_time time without time zone,
    reason character varying(120),
    status character varying(10),
    observation text,
    validator_id integer,
    created_at date,
    updated_at date,
    end_time time without time zone
);
    DROP TABLE public.permissions;
       public         heap    postgres    false            �            1259    49494    permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.permissions_id_seq;
       public          postgres    false    218                       0    0    permissions_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;
          public          postgres    false    219            �            1259    49495 
   validators    TABLE     s   CREATE TABLE public.validators (
    id integer NOT NULL,
    type character(15),
    dni character(8) NOT NULL
);
    DROP TABLE public.validators;
       public         heap    postgres    false                       0    0    TABLE validators    COMMENT     e   COMMENT ON TABLE public.validators IS 'valida si puede tener el permiso si o no, danne o antonella';
          public          postgres    false    220            �            1259    49498    validators_id_seq    SEQUENCE     �   CREATE SEQUENCE public.validators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.validators_id_seq;
       public          postgres    false    220                       0    0    validators_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.validators_id_seq OWNED BY public.validators.id;
          public          postgres    false    221            �            1259    49524    view_permissions    VIEW     s  CREATE VIEW public.view_permissions AS
 SELECT id,
    ( SELECT concat(e.dni, ' ', e.full_name) AS concat
           FROM public.employees e
          WHERE (e.dni = p.dni)) AS name,
    permission_date,
    start_time,
    return_time,
    reason,
    status,
    observation,
    validator_id,
    created_at,
    updated_at,
    end_time
   FROM public.permissions p;
 #   DROP VIEW public.view_permissions;
       public          postgres    false    217    218    218    218    218    218    218    218    218    218    218    218    218    217            �            1259    49499    view_permissions_with_details    VIEW     f  CREATE VIEW public.view_permissions_with_details AS
 SELECT p.id AS permission_id,
    p.permission_date,
    p.start_time,
    p.return_time,
    p.reason,
    p.status,
    p.end_time,
    ap.reason AS detail_reason,
    ap.return_time AS detail_return_time
   FROM public.permissions p,
    public.permission_details ap
  WHERE (p.id = ap.permission_id);
 0   DROP VIEW public.view_permissions_with_details;
       public          postgres    false    215    215    218    218    218    218    218    218    218    215            h           2604    49503    permission_details id    DEFAULT     �   ALTER TABLE ONLY public.permission_details ALTER COLUMN id SET DEFAULT nextval('public.additional_permissions_id_seq'::regclass);
 D   ALTER TABLE public.permission_details ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215            i           2604    49504    permissions id    DEFAULT     p   ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);
 =   ALTER TABLE public.permissions ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218            j           2604    49505    validators id    DEFAULT     n   ALTER TABLE ONLY public.validators ALTER COLUMN id SET DEFAULT nextval('public.validators_id_seq'::regclass);
 <   ALTER TABLE public.validators ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    220                      0    49486 	   employees 
   TABLE DATA           3   COPY public.employees (dni, full_name) FROM stdin;
    public          postgres    false    217   �0                 0    49482    permission_details 
   TABLE DATA           `   COPY public.permission_details (id, permission_id, reason, return_time, created_at) FROM stdin;
    public          postgres    false    215   u1       	          0    49489    permissions 
   TABLE DATA           �   COPY public.permissions (id, dni, permission_date, start_time, return_time, reason, status, observation, validator_id, created_at, updated_at, end_time) FROM stdin;
    public          postgres    false    218   �1                 0    49495 
   validators 
   TABLE DATA           3   COPY public.validators (id, type, dni) FROM stdin;
    public          postgres    false    220   .2                  0    0    additional_permissions_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.additional_permissions_id_seq', 1, true);
          public          postgres    false    216                       0    0    permissions_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.permissions_id_seq', 1, true);
          public          postgres    false    219                       0    0    validators_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.validators_id_seq', 2, true);
          public          postgres    false    221            l           2606    49507 .   permission_details additional_permissions_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.permission_details
    ADD CONSTRAINT additional_permissions_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.permission_details DROP CONSTRAINT additional_permissions_pkey;
       public            postgres    false    215            n           2606    49509    employees dni 
   CONSTRAINT     L   ALTER TABLE ONLY public.employees
    ADD CONSTRAINT dni PRIMARY KEY (dni);
 7   ALTER TABLE ONLY public.employees DROP CONSTRAINT dni;
       public            postgres    false    217            p           2606    49511    permissions id 
   CONSTRAINT     L   ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT id PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.permissions DROP CONSTRAINT id;
       public            postgres    false    218            r           2606    49513    validators validators_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.validators
    ADD CONSTRAINT validators_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.validators DROP CONSTRAINT validators_pkey;
       public            postgres    false    220            s           2606    49514 <   permission_details additional_permissions_permission_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.permission_details
    ADD CONSTRAINT additional_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id) NOT VALID;
 f   ALTER TABLE ONLY public.permission_details DROP CONSTRAINT additional_permissions_permission_id_fkey;
       public          postgres    false    218    4720    215            t           2606    49519 )   permissions permissions_validator_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_validator_id_fkey FOREIGN KEY (validator_id) REFERENCES public.validators(id) NOT VALID;
 S   ALTER TABLE ONLY public.permissions DROP CONSTRAINT permissions_validator_id_fkey;
       public          postgres    false    220    218    4722               t   x��1�0 ��~�_�Z5��h��]�0��w��#��JK�غ��2��-"�~���G3�9�[�������.��:X9W�]��(.)nש�MZ��M��]�z5ǗX��� ���         >   x�3�4�(��M-JT((*MMJTHIU(N��LI�44�21�20�4202�50�52����� �X�      	   [   x�3�471�06�0�4202�50�52�44�2��20 1LLA�����ԢD����ԤD��T��Ĝ̔DNGg׀GNNCd��1~\1z\\\ ��         &   x�3�LL���S�NC#cS3s.#���=... i0     