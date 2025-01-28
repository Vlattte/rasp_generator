SELECT 
    r7.id,
    r7.disc_id,
    r7.pair,
    r7.weekday,
    r7.weeksarray
    FROM sc_rasp7 r7
INNER JOIN sc_rasp7_groups r7_gr ON r7.id = r7_gr.rasp7_id 
    WHERE r7.semcode = 242500 and r7_gr.group_id = 0;