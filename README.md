# ECE4564_FinalProject
WEB UI

ADD

curl -u user:pass "http://[server_ip]:[5000]/add?competition_name=[competition name]&lifter_name=[lifter name]&lift_name=[lift name]&attempt_number=[attempt number]&weight=[weight]&judgememt_one=[judgement one]&judgememt_two=[judgement two]&judgememt_three=[judgement three]&result=[result]"

UPDATE
Use view to obtain document id

curl -u user:pass "http://[server_ip]:[5000]/update?competition_name=[competition name]&lifter_name=[lifter name]&id=[document id]key=[key]&value=[value]"

DELETE

curl -u user:pass "http://[server_ip]:[5000]/delete?competition_name=[competition name]&lifter_name=[lifter name]&search_key=[search key]&search_value=[search value]"

VIEW

All lifts in competition: curl "http://[server ip]:[5000]/view?competition_name=[competition name]"
All lifters in competition that match critera: curl "http://[server ip]:[5000]/view?competition_name=[competition name]&search_key=[search key]&search_value=[search value]"
All lifts for a certain lifter: curl "http://[server ip]:[5000]/view?competition_name=[competition name]&lifter_name=[lifter name]"
All lifts for a certain lifter that match criteria: curl "http://[server ip]:[5000]/view?competition_name=[competition name]&lifter=[lifter name]&search_key=[search key]&search_value=[search value]"

VALID SEARCH KEYS:

lifter [firstname]_[lastname]
lift (Squat/Bench/Deadlift)
attempt_number (1-3)
weight ([number]lbs)
result (Pass/Fail)
