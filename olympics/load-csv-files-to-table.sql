\copy athlete from 'athlete.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy public.event from 'event.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy game from 'game.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy athlete_NOC_event_game_metal from 'athlete_NOC_event_game_metal.csv' DELIMITER ',' CSV NULL AS 'NULL'
