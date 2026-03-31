-- Drop existing tables (so pipeline is reproducible)
DROP TABLE IF EXISTS post_features;
DROP TABLE IF EXISTS account_features;

-- Create post_features
CREATE TABLE post_features AS
SELECT
    id AS post_id,
    did,

    length(text) AS char_count,

    length(text) - length(replace(text, ' ', '')) + 1 AS word_count,

    CASE WHEN text LIKE '%http%' OR text LIKE '%www%' THEN 1 ELSE 0 END AS has_url,

    CASE WHEN text LIKE '%#%' THEN 1 ELSE 0 END AS has_hashtag,

    CASE WHEN text LIKE '%@%' THEN 1 ELSE 0 END AS has_mention,

    is_reply

FROM posts;

-- Create account_features
CREATE TABLE account_features AS
SELECT
    did,

    COUNT(*) AS total_posts,

    AVG(CASE WHEN is_reply THEN 1.0 ELSE 0.0 END) AS reply_rate,

    AVG(char_count) AS avg_post_length,

    AVG(word_count) AS avg_word_count,

    AVG(has_url) AS url_rate,

    AVG(has_hashtag) AS hashtag_rate,

    AVG(has_mention) AS mention_rate

FROM post_features
GROUP BY did;