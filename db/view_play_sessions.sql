-- Active: 1734183392559@@127.0.0.1@3306
select ps.session_id as "Session",
       g.name as "Game",
       ps.appid,
       datetime(ps.session_time, 'unixepoch', 'localtime') as "Session Time",
       floor(ps.minutes_played / 60) || 'h' || printf('%02d', ps.minutes_played % 60) as "Session Time Played",
       ps.play_count as "Play Count",
       floor(g.total_minutes_played / 60) || 'h' || printf('%02d', g.total_minutes_played % 60) as "Total Time Played",
       group_concat(a.display_name, '; ') as "Achievements Unlocked"
from game g
join play_session ps on g.appid = ps.appid
left join achievement a on ps.appid = a.appid and ps.session_id = a.session_id_unlocked
group by ps.session_id, g.name, ps.session_time, ps.minutes_played, ps.play_count, g.total_minutes_played
order by ps.session_time desc;
