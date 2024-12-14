select ps.session_id as "Session",
       ps.name as "Game",
       ps.appid as "App ID",
       datetime(ps.session_time, 'unixepoch', 'localtime') as "Session Time",
       floor(ps.minutes_played / 60) || 'h' || printf('%02d', ps.minutes_played % 60) as "Session Time Played",
       ps.play_count as "Play Count",
       floor(ps.total_minutes_played / 60) || 'h' || printf('%02d', ps.total_minutes_played % 60) as "Total Time Played",
       group_concat(a.display_name, '; ') as "Achievements Unlocked"
from play_session ps
left join achievement a on ps.appid = a.appid and ps.session_id = a.session_id_unlocked
group by ps.session_id, ps.name, ps.session_time, ps.minutes_played, ps.play_count, ps.total_minutes_played
order by ps.session_time desc;

