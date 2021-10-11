CREATE TABLE public.national_olympics_commities (
    NOC_name text,
    NOC_abbreviation text
);



CREATE TABLE public.athlete (
    id integer,
    last_name text,
    first_name text
);

CREATE TABLE public.medal (
    id integer,
    year integer,
    city text,
    sport text,
    event text,
    medal text
);

CREATE TABLE public.metal_athlete_team (
    metal_ID integer,
    athlete_ID integer,
    NOC_abbreviation text
);
