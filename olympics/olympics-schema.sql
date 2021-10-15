CREATE TABLE public.noc_regions (
    NOC_name text,
    NOC_abbreviation text,
    NOC_notes text
);



CREATE TABLE public.athlete (
    id integer,
    last_name text,
    whole_name text,
    sex text
);

CREATE TABLE public.game (
    id integer,
    year integer,
    season text,
    city text
);

CREATE TABLE public.event (
    id integer,
    sport text,
    athletic_event text
);

CREATE TABLE public.athlete_NOC_event_game_metal (
    athlete_ID integer,
    NOC_abbreviation text,
    event_ID integer,
    game_ID integer,
    metal text
);
