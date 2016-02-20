select lineup_spot, start_base_out_state, end_base_out_state, count(*)
from retrosheet.transitions_non_pa
where start_base_out_state != end_base_out_state
group by lineup_spot, start_base_out_state, end_base_out_state
union
select lineup_spot, start_base_out_state, start_base_out_state, count(*)
from retrosheet.transitions
where start_base_out_state != end_base_out_state
group by lineup_spot, start_base_out_state;