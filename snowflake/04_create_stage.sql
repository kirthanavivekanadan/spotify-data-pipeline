CREATE OR REPLACE STAGE spotify_stage
URL = 's3://spotify-data-pipeline-kirthi/'
FILE_FORMAT = (TYPE = 'JSON');

CREATE OR REPLACE FILE FORMAT json_format
TYPE = 'JSON'
COMPRESSION = 'AUTO';


COPY INTO spotify_tracks
FROM @spotify_stage
FILE_FORMAT = (FORMAT_NAME = json_format)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';