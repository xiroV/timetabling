include "alldifferent.mzn";
include "disjunctive.mzn";
include "count_fn.mzn";
include "count_geq.mzn";
include "nvalue_fn.mzn";
include "cumulative.mzn";
include "member.mzn";
include "global_cardinality_fn.mzn";

% The IMADA Timetabling Problem
enum Courses;
enum Teachers;
enum Rooms;
enum Students;
enum Events;
array[Events] of int: Duration;
array[Events] of int: InWeek;

int: hourStart = 8; % Starting hour of each day
int: hourEnd = 20; % Ending hour for each day
int: numDays = 5; % Number of days per week
int: goodDayEnd = 16;

set of int: Weeks;
int: firstWeek = min(Weeks);
int: lastWeek = max(Weeks);
int: numWeeks = lastWeek-firstWeek; % Number of weeks
int: numPrecedences = max(index_set_1of2(Precedences));
int: numPairings = max(index_set_1of2(Pairings));

int: slotsPerDay = (hourEnd-hourStart);
int: slotsPerWeek = slotsPerDay*numDays;
int: numRooms = length(Rooms);

set of int: Days = 1..numDays;
set of int: Hours = hourStart..hourEnd-1;
set of int: Slots = 1..(numWeeks+1)*numDays*(slotsPerDay)*numRooms;
int: numTimeslots = ((numWeeks+1)*numDays*(slotsPerDay));
set of int: Timeslots = 0..numTimeslots-1;

array[Teachers] of set of Timeslots: TeacherBusy;
array[Teachers] of set of Events: TeacherEvents;
array[Rooms] of set of Timeslots: RoomOccupied;

array[Events] of Courses: PartOf;
array[int,1..2] of Events: Precedences;
array[int,1..2] of Events: Pairings;
array[Students] of set of Events: Attending;
array[Events] of var 1..1: RoomsRequired;

array[Events] of var Slots: Scheduled;
array[Events] of var Timeslots: Timeslot;
array[Events] of var 0..slotsPerWeek: TimeslotInWeek;
array[Events] of var 0..4: badSlots;
array[Events] of var Rooms: eventRoom;
array[Events] of var Weeks: eventWeek;
array[Events] of var Days: eventDay;
array[Events] of var Hours: eventHour;

% maxAttending should be the number of courses which the student is signed up for,
% slotsPerDay is a looser upper bound.
int: maxAttending = slotsPerDay;

% Auxiliary Variables
array[Teachers, firstWeek..lastWeek, Days] of var 1..10: eventxDayxTeacher; % for S3
array[Teachers] of var 1..numTimeslots: maxEventsxDayxTeacher; % for S3
array[Students, firstWeek..lastWeek, Days] of var 3..maxAttending: eventxDayxStudent;
array[Students] of var 3..numTimeslots: maxEventsxDayxStudent;
array[Students] of var 0..maxAttending: studentOverlaps;
array[Students] of var 0..maxAttending: maxStudentOverlaps;
array[1..numPairings] of var 0..slotsPerWeek-1: timeDiscrepancies;
array[1..numPairings] of var 0..numRooms-1: roomDiscrepancies;


% Restrict Scheduled
constraint forall(e in Events)(
    ((eventWeek[e]-firstWeek)*slotsPerWeek +
    (eventDay[e]-1)*slotsPerDay +
    (eventHour[e]-hourStart))
    *numRooms + eventRoom[e] = Scheduled[e]
);

% Channel Timeslot
constraint forall(e in Events)(
    Scheduled[e] = (Timeslot[e])*numRooms+eventRoom[e]
);

% Channel TimeslotInWeek
constraint forall(e in Events)(
    TimeslotInWeek[e] = Timeslot[e] - ((eventWeek[e]-firstWeek)*slotsPerWeek)
);

%% Schedule each event into right week
%% TODO Could be using the table constraint?
constraint forall(e in Events, w in Weeks where InWeek[e]==w)(
    eventWeek[e] = w
);

% Events cannot be scheduled into rooms which is marked as occupied at a given timeslot
constraint forall(r in Rooms, e in Events where eventRoom[e]==r, d in 0..Duration[e]-1)(
    not(member(RoomOccupied[r], Timeslot[e]+d))
);


% Max 1 event per day per course
constraint forall(w in Weeks, c in Courses)(
    alldifferent(e in Events where InWeek[e]==w /\ PartOf[e]==c)(
        eventDay[e]
    )
);

% Max 1 event per room at a time (H2, H3)
constraint cumulative(
    [Timeslot[e]+numTimeslots*(eventRoom[e]-1) | e in Events],
    Duration,
    RoomsRequired,
    1
);

% Teacher can not teach when busy
constraint forall(t in Teachers, e in TeacherEvents[t], d in 0..Duration[e]-1)(
    not(member(TeacherBusy[t], Timeslot[e]+d))
);

% Events must have time to finish within the current day (H4, H5)
constraint forall(e in Events)(
    eventHour[e]+Duration[e] <= hourEnd
);

% Teacher can only teach on event at a time (H6)
constraint forall(t in Teachers)(
    if length(e in TeacherEvents[t])(1)>0 then
        disjunctive(
            [Timeslot[e]+numTimeslots*(eventRoom[e]-1) | e in TeacherEvents[t]],
            [Duration[e] | e in TeacherEvents[t]] 
        )
    endif
);


% Enforce precedences (H8)
constraint forall(w in Weeks, p in 1..numPrecedences where w==InWeek[Precedences[p,1]] /\ w==InWeek[Precedences[p,2]])(
     Scheduled[Precedences[p,1]] < Scheduled[Precedences[p,2]]
);


% Timeslot stability (S1)
constraint forall(p in 1..numPairings)(
    abs(TimeslotInWeek[Pairings[p,1]] - TimeslotInWeek[Pairings[p,2]]) <= timeDiscrepancies[p]
);


% Room stability (S2)
constraint forall(p in 1..numPairings)(
    abs(eventRoom[Pairings[p,1]] - eventRoom[Pairings[p,2]]) <= roomDiscrepancies[p]
);

% constraint trace("Processing eventxDayxTeacher\n",true);
constraint forall(t in Teachers)(
    max(global_cardinality(
        [(eventWeek[e]-firstWeek)*numDays + eventDay[e] | e in TeacherEvents[t]],
        [(w-firstWeek)*numDays + d | w in Weeks, d in Days]
    )) <= maxEventsxDayxTeacher[t]
);

% Minimize number of events per student per day (S4) (if more than 3)
% maxEventsxDayxStudent[s] should be the number of events s is attending the day where s is attending
% the highest number of events
% constraint trace("Processing eventxDayxStudent\n",true);
constraint forall(s in Students)(
    max(global_cardinality(
        [(eventWeek[e]-firstWeek)*numDays + eventDay[e] | e in Attending[s]],
        [(w-firstWeek)*numDays + d | w in Weeks, d in Days]
    )) <= maxEventsxDayxStudent[s]
);


% Minimize bad slots
% constraint trace("Processing badSlots\n",true);
constraint forall(e in Events)(
    if eventHour[e]+Duration[e] > goodDayEnd then
        eventHour[e]+Duration[e]-goodDayEnd <= badSlots[e]
    endif
);

% Minimize student overlaps/conflicts (S6)
% constraint trace("Processing overlaps\n",true);
constraint forall(s in Students)(
    count_geq(global_cardinality(
        [Timeslot[e]+d | e in Attending[s], d in 0..Duration[e]-1],
        Timeslots
    ), 2, maxStudentOverlaps[s])
);

%constraint trace("\nDone\n",true);

% Increases utilization of the rooms (e.g. choose another room instead of waiting for room to be empty)
% Actually instructs the solver to place events as early in time as possible
solve :: int_search(Scheduled, smallest, indomain_min, complete)
     minimize sum(maxEventsxDayxTeacher) +
             sum(timeDiscrepancies) +
             sum(roomDiscrepancies) +
             sum(maxStudentOverlaps) +
             sum(maxEventsxDayxStudent) +
             sum(badSlots);

% Satisfiability version for testing
%solve :: int_search(Scheduled, smallest, indomain_min, complete) satisfy;


% Pretty print output
output [ concat([
    "s=" ++ show(s) ++
    " ts=" ++ show(Timeslot[e]) ++
    " ts_w=" ++ show(TimeslotInWeek[e]) ++
    " w=" ++ show(eventWeek[e]) ++
    " d=" ++ show(eventDay[e]) ++
    " h=" ++ show(eventHour[e]) ++
    " r=" ++ show(eventRoom[e]) ++
    " e=" ++ show(e) ++ "\n"
    | s in Slots, e in Events where fix(Scheduled[e])==s])
];

output [ concat([
    "A " ++ show(e) ++
    " " ++ show(eventDay[e]) ++
    " " ++ show(eventHour[e]) ++
    " " ++ show(eventHour[e] + Duration[e]) ++
    " " ++ show(eventWeek[e]) ++
    " " ++ show(eventRoom[e]) ++ "\n"
    | s in Slots, e in Events where fix(Scheduled[e])==s])
];


output [ "\nViolations:.\n" ];
output [ "timeStability: " ++ show(fix(sum(timeDiscrepancies))) ++ "\n"];
output [ "roomStability: " ++ show(fix(sum(roomDiscrepancies))) ++ "\n"];
output [ "maxEventsxDayxTeacher: " ++ show(fix(sum(maxEventsxDayxTeacher))) ++ "\n"];
output [ "maxEventsxDayxStudent: " ++ show(fix(sum(maxEventsxDayxStudent))) ++ "\n"];
output [ "maxStudentOverlaps: " ++ show(fix(sum(maxStudentOverlaps))) ++ "\n"];
output [ "badSlots: " ++ show(fix(sum(badSlots))) ++ "\n"];

output [ "timeStability: " ++ show(fix(timeDiscrepancies)) ++ "\n"];
output [ "roomStability: " ++ show(fix((roomDiscrepancies))) ++ "\n"];
output [ "maxEventsxDayxTeacher: " ++ show(((maxEventsxDayxTeacher))) ++ "\n"];
output [ "maxEventsxDayxStudent: " ++ show(((maxEventsxDayxStudent))) ++ "\n"];
output [ "maxStudentOverlaps: " ++ show(fix(maxStudentOverlaps)) ++ "\n"];
output [ "badSlots: " ++ show(fix(badSlots)) ++ "\n"];

