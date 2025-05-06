CREATE OR REPLACE PROCEDURE load_spotify_data()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
  INSERT INTO spotify_tracks (
    track_id,
    track_name,
    artist_name,
    album_name,
    release_date
  )
  SELECT 
    value:track_id::STRING,
    value:track_name::STRING,
    value:artist_name::STRING,
    value:album_name::STRING,
    TO_DATE(value:release_date::STRING)
  FROM @spotify_stage (FILE_FORMAT => 'json_format'),
       LATERAL FLATTEN(input => PARSE_JSON($1));

  RETURN 'Load completed.';
END;
$$;
