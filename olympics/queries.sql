/* 
List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation. 
*/
SELECT noc_regions.NOC_name, noc_regions.NOC_abbreviation FROM noc_regions 
ORDER BY noc_regions.NOC_abbreviation;

/*
List the names of all the athletes from Kenya. If your database design allows it, sort the athletes by last name.
*/
SELECT DISTINCT athlete.whole_name
              , athlete.last_name
FROM athlete_NOC_event_game_metal
   , athlete, noc_regions
WHERE athlete.id = athlete_NOC_event_game_metal.athlete_ID
AND noc_regions.NOC_abbreviation = athlete_NOC_event_game_metal.NOC_abbreviation
AND noc_regions.NOC_name = 'Kenya'
ORDER BY athlete.last_name;

/*
List all the medals won by Greg Louganis, sorted by year. Include whatever fields in this output that you think appropriate.
*/
SELECT game.year
     , game.season
     , game.city
     , public.event.sport
     , public.event.athletic_event
     , athlete_NOC_event_game_metal.metal
     , noc_regions.NOC_name
FROM game, public.event, noc_regions, athlete_NOC_event_game_metal, athlete
WHERE athlete.id = athlete_NOC_event_game_metal.athlete_ID
AND public.event.id = athlete_NOC_event_game_metal.event_ID
AND game.id = athlete_NOC_event_game_metal.game_ID
AND noc_regions.NOC_abbreviation = athlete_NOC_event_game_metal.NOC_abbreviation
AND athlete.whole_name LIKE '%Greg%'
AND athlete.whole_name LIKE '%Louganis%'
ORDER BY game.year;

/*
List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.
*/
SELECT noc_regions.NOC_abbreviation, COUNT(CASE WHEN athlete_NOC_event_game_metal.metal = 'Gold' THEN 1 END) 
FROM noc_regions, athlete_NOC_event_game_metal 
WHERE noc_regions.NOC_abbreviation = athlete_NOC_event_game_metal.NOC_abbreviation 
GROUP BY noc_regions.NOC_abbreviation ORDER BY COUNT(CASE WHEN athlete_NOC_event_game_metal.metal = 'Gold' THEN 1 END)  DESC;