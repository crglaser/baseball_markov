select start_base_out_state, end_base_out_state, count(*)
from retrosheet.transitions
where substring(date,1,4) = 2013
group by start_base_out_state, end_base_out_state