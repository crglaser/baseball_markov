create or replace view retrosheet.transitions_non_pa
as select
event_cd,
game_dt as date,
bat_lineup_id as lineup_spot,
outs_ct as start_outs,
start_bases_cd,
outs_ct + event_outs_ct as end_outs,
end_bases_cd,
event_runs_ct,
(outs_ct * 8 + start_bases_cd) as start_base_out_state,
case when outs_ct + event_outs_ct = 3 then (event_runs_ct + 24)
	else ((outs_ct + event_outs_ct) * 8 + end_bases_cd)
    end as end_base_out_state
from retrosheet.events r_event
join retrosheet.games r_games
on r_event.game_id = r_games.game_id
where r_event.event_cd in (4,5,6,8,9,10,11,12,13,17);