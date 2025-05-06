---- setting the tast every 12 hours -------
CREATE OR REPLACE TASK spotify_load_task
  WAREHOUSE = SPOTIFY_WH
  SCHEDULE = '12 HOURS'
AS
  CALL load_spotify_data();
----- ACTIVATING THE TASK -------
ALTER TASK spotify_load_task RESUME;
