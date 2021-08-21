% The IMADA Timetabling Problem
enum Events;
enum Courses;
enum Teachers;
enum Rooms;
enum Students;
enum SectionTypes;
array[Events] of int: Duration;
array[Events, Weeks] of bool: InWeek;
array[Events] of int: TaughtBy;
int: ReferenceWeek;

int: numRooms = length(Rooms);
int: hourStart = 8; % Starting hour of each day
int: hourEnd = 16; % Ending hour for each day
int: numDays = 5; % Number of days per week
int: numWeeks = 4; % Number of weeks
%int: numPrecedences;

%set of int: Weeks = 1..numWeeks;
set of int: Weeks;
set of int: Days = 1..numDays;
set of int: Hours = hourStart..hourEnd;
int: slotsPerDay = (hourEnd-hourStart);
array[Events] of SectionTypes: Sections;

int: numTimeslots = ((numWeeks+1)*numDays*(slotsPerDay));
set of int: Timeslots = 0..numTimeslots-1;

array[Events] of Courses: PartOf;
array[int,int] of Events: Precedences;
array[Students, Events] of bool: Attending;
array[Students] of set of Events: Attending2;
int: numPrecedences = max(index_set_1of2(Precedences));
array[int,1..2] of Events: Pairings;
array[Teachers] of set of Events: TeacherEvents;
array[Teachers] of set of Timeslots: TeacherBusy;
array[Events, Rooms, Weeks, Days, Hours] of var bool: Scheduled;
array[Rooms] of set of Timeslots: RoomOccupied;

% Auxillary Variables
array[Teachers, Weeks, Days] of var 0..hourEnd-hourStart: eventxDayxTeacher; % for S3
array[Students, Weeks, Days] of var 0..hourEnd-hourStart: eventxDayxStudent;
array[Students, Weeks, Days, Hours] of var 0..10: eventxTimeslotxStudent;
array[Events, Weeks] of var 0..(hourEnd-hourStart)*numDays: timeDiscrepancies;
array[Events, Weeks] of var 0..numRooms: roomDiscrepancies;

% All events scheduled (H1)
constraint forall(e in Events, w in Weeks where InWeek[e, w])(
    sum(r in Rooms, d in Days, h in Hours)(Scheduled[e, r, w, d, h]) = 1
);

% Events cannot be scheduled in a room if it is occupied (H2,H3)
constraint forall(r in Rooms, w in Weeks, d in Days, h in Hours)(
    sum(e in Events, s in h..h+Duration[e]-1)(Scheduled[e,r,w,d,min(hourEnd, s)]) <= 1
);

% Events should have time to finish within the current day (H4,H5)
constraint forall(e in Events, r in Rooms, w in Weeks, d in Days, h in Hours)(
    Scheduled[e,r,w,d,h] * (h + Duration[e]) <= hourEnd
);

% Teacher can only teach on event at a time (H6)
constraint forall(w in Weeks, d in Days, h in Hours, t in Teachers)(
    sum(e in Events, r in Rooms, s in 0..Duration[e]-1 where TaughtBy[e]==t)(Scheduled[e,r,w,d,min(hourEnd, h+s)]) <= 1
);

% Max One event per day per course (H7)
constraint forall(w in Weeks, d in Days, c in Courses)(
    sum(e in Events, r in Rooms, h in Hours where fix(PartOf[e])==c)(Scheduled[e, r, w, d, h]) <= 1
);

% Enforce precedences (H8)
constraint forall(p in 1..numPrecedences)(
    sum(w in Weeks, d in Days, h in Hours, e in Events where Precedences[p, 1]==e)(((hourEnd-hourStart)*numDays*w+(hourEnd-hourStart)*d + h) * sum(r in Rooms)(Scheduled[e,r,w,d,h])) <=
    sum(w in Weeks, d in Days, h in Hours, e in Events where Precedences[p, 2]==e)(((hourEnd-hourStart)*numDays*w+(hourEnd-hourStart)*d + h) * sum(r in Rooms)(Scheduled[e,r,w,d,h]))
);

% Timeslot stability (S1)
% TODO Test this -> Tested once
%constraint forall(c in Courses, e in Events where PartOf[e]==c, w in Weeks where InWeek[e, w])(
%    abs(sum(r in Rooms, d in Days, h in Hours)(Scheduled[e,r,w,d,h]*d*(hourEnd-hourStart)+h)-sum(r in Rooms, d in Days, h in Hours)(Scheduled[e,r,referenceWeek,d,h]*d*(hourEnd-hourStart)+h))
%    <= timeDiscrepancies[e,w]
%);

% Room stability (S2)
% TODO Test this
%constraint forall(c in Courses, e in Events where PartOf[e]==c, w in Weeks where InWeek[e, w])(
%    abs(sum(r in Rooms, d in Days, h in Hours)(Scheduled[e,r,w,d,h]*r)-sum(r in Rooms, d in Days, h in Hours)(Scheduled[e,r,referenceWeek,d,h]*r))
%    <= roomDiscrepancies[e,w]
%);

% TODO Check S3 and S4: Gecode stuck in looking for a optimal solution if it does not exist
% (e.g. minimizing num events per day per teacher for n days and number of events > n).

% Minimize number of events per day per teacher (S3)
%constraint forall(t in Teachers, w in Weeks, d in Days)(
%    sum(e in Events, r in Rooms, h in Hours where TaughtBy[e]==t)(Scheduled[e,r,w,d,h])-1 <= eventxDayxTeacher[t,w,d]
%);

% Minimize number of events per student per day (S4) (if more than 3)
%constraint forall(s in Students, w in Weeks, d in Days)(
%    sum(e in Events, r in Rooms, h in Hours where Attending[s, e]==true)(Scheduled[e,r,w,d,h])-3 <= eventxDayxStudent[s,w,d]
%);

% Minimize student overlaps/conflicts (S6)
%constraint forall(s in Students, w in Weeks, d in Days, h in Hours)(
%    sum(e in Events, h2 in h..h+Duration[e]-1, r in Rooms where Attending[s, e]==true)(Scheduled[e,r,w,d,min(hourEnd, h+h2)]) <= eventxTimeslotxStudent[s,w,d,h]
%);

% Define objective
%solve minimize sum(e in Events, w in Weeks, d in Days, h in Hours)(
%                    sum(r in Rooms)(Scheduled[e,r,w,d,h]) - sum(r in Rooms)(Scheduled[e,r,referenceWeek,d,h])
%             )
%             + sum(t in Teachers, w in Weeks, d in Days)(eventxDayxTeacher[t,w,d])
%             + sum(s in Students, w in Weeks, d in Days)(eventxDayxStudent[s,w,d])
%             + sum(s in Students, w in Weeks, d in Days, h in Hours)(eventxTimeslotxStudent[s,w,d,h])
%             + sum(w in Weeks, e in Events)(timeDiscrepancies[e,w])
%;

% Pretty print output
output [ concat([
    "w=" ++ show(w) ++ " d=" ++ show(d) ++ " h=" ++ show(h) ++ " e=" ++ show(e) ++ " r=" ++ show(r) ++ " t=" ++ show(Teachers[TaughtBy[e]]) ++ ",\n"
    | w in Weeks, d in Days, h in Hours, e in Events, r in Rooms where fix(Scheduled[e, r, w, d, h])==1])
];
