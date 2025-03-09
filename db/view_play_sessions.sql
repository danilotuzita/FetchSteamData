-- Active: 1734183392559@@127.0.0.1@3306
with play_session_with_play_time_until as (
    select ps.*,
           sum(ps.minutes_played) over (partition by ps.appid order by ps.session_id) as minutes_played_until_session
    from play_session ps
)
select ps.session_id as "Session",
       g.name as "Game",
       ps.appid,
       printf('%s ~ %s', datetime(ps.session_time - (minutes_played * 60), 'unixepoch', 'localtime'), datetime(ps.session_time, 'unixepoch', 'localtime')) as "Session Time",
       printf('%dh%02d', floor(ps.minutes_played / 60), ps.minutes_played % 60) as "Session Time Played",
       ps.play_count as "Play Count",
       printf('%dh%02d', floor(ps.minutes_played_until_session / 60), ps.minutes_played_until_session % 60) as "Time played until session (including)",
       floor(g.total_minutes_played / 60) || 'h' || printf('%02d', g.total_minutes_played % 60) as "Total Time Played",
       group_concat(a.display_name, '; ') as "Achievements Unlocked",
       group_concat(distinct n.content) as "Session Notes"
from game g
join play_session_with_play_time_until ps on g.appid = ps.appid
left join achievement a on ps.appid = a.appid and ps.session_id = a.session_id_unlocked
left join note n on ps.appid = n.appid and ps.session_id = n.session_id
group by ps.session_id, g.name, ps.session_time, ps.minutes_played, ps.play_count, g.total_minutes_played
order by ps.session_time desc;
