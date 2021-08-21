include "table.mzn";
include "table_int.mzn";
include "member.mzn";

enum Classes;
enum Schedules;
enum Rooms;
enum Weeks;
enum Days;

array[Schedules] of int: ScheduleStarts;
array[Schedules] of int: ScheduleLengths;
array[Schedules] of set of Weeks: ScheduleWeeks;
array[Schedules] of set of Days: ScheduleDays;
array[Classes] of set of Schedules: ClassSchedules;
array[Classes] of set of Rooms: ClassRooms;
array[Classes,Rooms] of int: ClassRoomPenalties;
array[Classes,Schedules] of int: ClassSchedulePenalties;

array[Schedules] of set of Schedules: ScheduleOverlaps;
array[Schedules] of set of Schedules: Precedences;

array[Schedules] of set of Schedules: SameStarts;
array[Schedules] of set of Schedules: SameDays;
array[Schedules] of set of Schedules: SameTime;
array[Schedules] of set of Schedules: SameWeeks;

%array[int,int] of Schedules: SameStarts;
%array[int,int] of Schedules: SameDays;
%array[int,int] of Schedules: SameTime;
%array[int,int] of Schedules: SameWeeks;

% Distributions
array[int] of set of Classes: OverlapHard;
array[int] of set of Classes: OverlapSoft;
array[int] of int: OverlapPenalties;

array[int] of set of Classes: NotOverlapHard;
array[int] of set of Classes: NotOverlapSoft;
array[int] of int: NotOverlapPenalties;

array[int] of set of Classes: PrecedenceHard;
array[int] of set of Classes: PrecedenceSoft;
array[int] of int: PrecedencePenalties;

array[int] of set of Classes: SameAttendeesHard;
array[int] of set of Classes: SameAttendeesSoft;
array[int] of int: SameAttendeesPenalties;

array[int] of set of Classes: SameStartHard;
array[int] of set of Classes: SameStartSoft;
array[int] of int: SameStartPenalties;

array[int] of set of Classes: SameTimeHard;
array[int] of set of Classes: SameTimeSoft;
array[int] of int: SameTimePenalties;

array[int] of set of Classes: DifferentTimeHard;
array[int] of set of Classes: DifferentTimeSoft;
array[int] of int: DifferentTimePenalties;

array[int] of set of Classes: SameDaysHard;
array[int] of set of Classes: SameDaysSoft;
array[int] of int: SameDaysPenalties;

array[int] of set of Classes: DifferentDaysHard;
array[int] of set of Classes: DifferentDaysSoft;
array[int] of int: DifferentDaysPenalties;

array[int] of set of Classes: SameWeeksHard;
array[int] of set of Classes: SameWeeksSoft;
array[int] of int: SameWeeksPenalties;

array[int] of set of Classes: DifferentWeeksHard;
array[int] of set of Classes: DifferentWeeksSoft;
array[int] of int: DifferentWeeksPenalties;

array[int] of set of Classes: SameRoomHard;
array[int] of set of Classes: SameRoomSoft;
array[int] of int: SameRoomPenalties;

array[int] of set of Classes: DifferentRoomHard;
array[int] of set of Classes: DifferentRoomSoft;
array[int] of int: DifferentRoomPenalties;

array[int] of set of Classes: WorkDayHard;
array[int] of set of Classes: WorkDaySoft;
array[int] of int: WorkDayPenalties;
array[int] of int: WorkDayHardParameters;
array[int] of int: WorkDaySoftParameters;

array[int] of set of Classes: MinGapHard;
array[int] of set of Classes: MinGapSoft;
array[int] of int: MinGapPenalties;
array[int] of int: MinGapHardParameters;
array[int] of int: MinGapSoftParameters;

array[int] of set of Classes: MaxDaysHard;
array[int] of set of Classes: MaxDaysSoft;
array[int] of int: MaxDaysPenalties;
array[int] of int: MaxDaysHardParameters;
array[int] of int: MaxDaysSoftParameters;

array[int] of set of Classes: MaxDayLoadHard;
array[int] of set of Classes: MaxDayLoadSoft;
array[int] of int: MaxDayLoadPenalties;
array[int] of int: MaxDayLoadHardParameters;
array[int] of int: MaxDayLoadSoftParameters;

array[int] of set of Classes: MaxBreaksHard;
array[int] of set of Classes: MaxBreaksSoft;
array[int] of int: MaxBreaksPenalties;
array[int,int] of int: MaxBreaksHardParameters;
array[int,int] of int: MaxBreaksSoftParameters;

array[int] of set of Classes: MaxBlockHard;
array[int] of set of Classes: MaxBlockSoft;
array[int] of int: MaxBlockPenalties;
array[int,int] of int: MaxBlockHardParameters;
array[int,int] of int: MaxBlockSoftParameters;

array[Schedules] of set of Rooms: RoomUnavailable;
array[Rooms,Rooms] of int: RoomDistances;

int: maxSameStartViolations;
int: maxSameTimeViolations;
int: maxDifferentTimeViolations;
int: maxSameDaysViolations;
int: maxDifferentDaysViolations;
int: maxSameWeeksViolations;
int: maxDifferentWeeksViolations;
int: maxSameRoomViolations;
int: maxDifferentRoomViolations;
int: maxOverlapViolations;
int: maxNotOverlapViolations;
int: maxSameAttendeesViolations;
int: maxPrecedenceViolations;
int: maxWorkDayViolations;
int: maxMinGapViolations;
int: maxMaxDaysViolations;
int: maxMaxDayLoadViolations;
int: maxMaxBreaksViolations;
int: maxMaxBlockViolations;

array[Classes] of var Schedules: ScheduledTime; 
array[Classes] of var Rooms: ScheduledRoom; 

array[1..length(SameRoomSoft)] of var 0..maxSameRoomViolations: SameRoomViolations; 
array[1..length(DifferentRoomSoft)] of var 0..maxDifferentRoomViolations: DifferentRoomViolations; 
array[1..length(SameAttendeesSoft)] of var 0..maxSameAttendeesViolations: SameAttendeesViolations; 
array[1..length(NotOverlapSoft)] of var 0..maxNotOverlapViolations: NotOverlapViolations; 
array[1..length(OverlapSoft)] of var 0..maxOverlapViolations: OverlapViolations; 
array[1..length(SameTimeSoft)] of var 0..maxSameTimeViolations: SameTimeViolations; 
array[1..length(DifferentTimeSoft)] of var 0..maxDifferentTimeViolations: DifferentTimeViolations; 
array[1..length(SameWeeksSoft)] of var 0..maxSameWeeksViolations: SameWeeksViolations; 
array[1..length(DifferentWeeksSoft)] of var 0..maxDifferentWeeksViolations: DifferentWeeksViolations; 
array[1..length(SameDaysSoft)] of var 0..maxSameDaysViolations: SameDaysViolations; 
array[1..length(DifferentDaysSoft)] of var 0..maxDifferentDaysViolations: DifferentDaysViolations; 
array[1..length(SameStartSoft)] of var 0..maxSameStartViolations: SameStartViolations; 
array[1..length(PrecedenceSoft)] of var 0..maxPrecedenceViolations: PrecedenceViolations; 

predicate same_start(Classes: c1, Classes: c2) =
    %ScheduledTime[c2] in SameStarts[ScheduledTime[c1]]
    %table([ScheduledTime[c1], ScheduledTime[c2]], SameStarts)
    ScheduleStarts[ScheduledTime[c1]] == ScheduleStarts[ScheduledTime[c2]]
;

predicate same_time(Classes: c1, Classes: c2) =
    %ScheduledTime[c2] in SameTime[ScheduledTime[c1]]
    ScheduleStarts[ScheduledTime[c1]] == ScheduleStarts[ScheduledTime[c2]]
    %table([ScheduledTime[c1], ScheduledTime[c2]], SameTime)
;

predicate same_room(Classes: c1, Classes: c2) =
    ScheduledRoom[c1] == ScheduledRoom[c2]
;

predicate overlap(Classes: c1, Classes: c2) =
    member(ScheduleOverlaps[ScheduledTime[c1]], ScheduledTime[c2])
    %let { var Schedules: s1 = ScheduledTime[c1]; var Schedules: s2 = ScheduledTime[c2]} in

    %(ScheduleStarts[s2] < ScheduleStarts[s1] + ScheduleLengths[s1]) /\
    %(ScheduleStarts[s1] < ScheduleStarts[s2] + ScheduleLengths[s2]) /\
    %not(same_days(c1,c2)) /\ not(same_weeks(c1,c2))
;

predicate same_attendees(Classes: c1, Classes: c2) =
    %not(same_weeks(c1,c2)) \/ not(same_days(c1,c2)) \/
    %    ((ScheduleStarts[ScheduledTime[c1]] + ScheduleLengths[ScheduledTime[c1]] + RoomDistances[ScheduledRoom[c1],ScheduledRoom[c2]]) <= ScheduleStarts[ScheduledTime[c2]]) \/
    %    ((ScheduleStarts[ScheduledTime[c2]] + ScheduleLengths[ScheduledTime[c2]] + RoomDistances[ScheduledRoom[c2],ScheduledRoom[c1]]) <= ScheduleStarts[ScheduledTime[c1]])

    let {var Schedules: s1 = ScheduledTime[c1]; var Schedules: s2 = ScheduledTime[c2]} in
    (ScheduleStarts[s1] + ScheduleLengths[s1] + RoomDistances[ScheduledRoom[c1],ScheduledRoom[c2]] <= ScheduleStarts[s2]) \/
    (ScheduleStarts[s2] + ScheduleLengths[s2] + RoomDistances[ScheduledRoom[c2],ScheduledRoom[c1]] <= ScheduleStarts[s1]) \/
    (card(ScheduleDays[s1] intersect ScheduleDays[s2]) == 0) \/
    (card(ScheduleWeeks[s1] intersect ScheduleWeeks[s2]) == 0)
;

predicate precede(Classes: c1, Classes: c2) =
    member(Precedences[ScheduledTime[c2]], ScheduledTime[c1])
;

predicate same_weeks(Classes: c1, Classes: c2) =
    member(SameWeeks[ScheduledTime[c1]], ScheduledTime[c2])
    %table([ScheduledTime[c1], ScheduledTime[c2]], SameWeeks)
;

predicate same_days(Classes: c1, Classes: c2) =
    member(SameDays[ScheduledTime[c1]], ScheduledTime[c2])
    %table([ScheduledTime[c1], ScheduledTime[c2]], SameDays)
;

predicate workday(Classes: c1, Classes: c2, int: s) =
    not(same_days(c1,c2)) \/
    not(same_weeks(c1,c2)) \/
    (max(ScheduleStarts[ScheduledTime[c1]] + ScheduleLengths[ScheduledTime[c1]], ScheduleStarts[ScheduledTime[c2]] + ScheduleLengths[ScheduledTime[c2]])
    - min(ScheduleStarts[ScheduledTime[c1]], ScheduleStarts[ScheduledTime[c2]]) <= s)
;

predicate mingap(Classes: c1, Classes: c2, int: g) =
    let {var Schedules: s1 = ScheduledTime[c1]; var Schedules: s2 = ScheduledTime[c2]} in
    not(same_days(c1,c2)) \/ not(same_weeks(c1,c2))
    \/ (ScheduleStarts[s1] + ScheduleLengths[s1] + g <= ScheduleStarts[s2])
    \/ (ScheduleStarts[s2] + ScheduleLengths[s2] + g <= ScheduleStarts[s1])
;

%predicate maxdays(Classes: c, int: d) =
%    let {var Schedules: s = ScheduledTime[c]} in
%    card(ScheduleDays[s]) <= d 
%;

predicate maxdayload(set of Classes: clas, int: s) =
    forall(w in Weeks, d in Days)(
        sum(
            [
                ScheduleLengths[ScheduledTime[c]] | c in clas where
                    card(ScheduleDays[ScheduledTime[c]] intersect {d}) != 0 /\
                    card(ScheduleWeeks[ScheduledTime[c]] intersect {w}) != 0
            ]
        ) <= s
    )
;

predicate maxbreaks(set of Classes: clas, int: r, int: s) =
    forall(w in Weeks, d in Days)(
        sum(c1,c2 in clas where c1<c2 /\
                card(ScheduleDays[ScheduledTime[c1]] intersect {d}) != 0 /\
                card(ScheduleWeeks[ScheduledTime[c1]] intersect {w}) != 0 /\
                card(ScheduleDays[ScheduledTime[c2]] intersect {d}) != 0 /\
                card(ScheduleWeeks[ScheduledTime[c2]] intersect {w}) != 0 /\
                abs(ScheduleStarts[ScheduledTime[c1]] + ScheduleLengths[ScheduledTime[c1]] - ScheduleStarts[ScheduledTime[c2]]) < s
        )(1) <= r + 1
    )
;

constraint forall(c in Classes)(
    member(ClassSchedules[c], ScheduledTime[c])
);

constraint forall(c in Classes)(
    member(ClassRooms[c], ScheduledRoom[c])
);

constraint forall(c1,c2 in Classes where c1<c2 /\ ScheduledRoom[c1] == ScheduledRoom[c2] /\ ScheduledRoom[c1] != None)(
    not(overlap(c1,c2))
);

constraint forall(c in Classes where ScheduledRoom[c] != None)(
    not(member(RoomUnavailable[ScheduledTime[c]], ScheduledRoom[c]))
);

% Dist Overlap
constraint forall(overlap in OverlapHard, c1,c2 in overlap where c1<c2)(
    overlap(c1,c2)
);

% Dist Overlap Violations
constraint forall(s in 1..length(OverlapSoft))(
    OverlapViolations[s] >= sum(c1,c2 in OverlapSoft[s] where c1<c2 /\ not(overlap(c1,c2)))(1)
);

% Dist NotOverlap 
constraint forall(notOverlap in NotOverlapHard, c1,c2 in notOverlap where c1<c2)(
    not(overlap(c1,c2))
);

% Dist NotOverlap Violations
constraint forall(s in 1..length(NotOverlapSoft))(
    NotOverlapViolations[s] >= sum(c1,c2 in NotOverlapSoft[s] where c1<c2 /\ overlap(c1,c2))(1)
);

% Dist SameAttendees 
constraint forall(sameAttend in SameAttendeesHard, c1,c2 in sameAttend where c1<c2)(
   same_attendees(c1,c2)
);

% Dist SameAttendees Violations
constraint forall(s in 1..length(SameAttendeesPenalties), c1,c2 in SameAttendeesSoft[s] where c1<c2)(
   SameAttendeesViolations[s] >= sum(c1,c2 in SameAttendeesSoft[s] where c1<c2 /\ not(same_attendees(c1, c2)))(1)
);

% Dist SameRoom 
constraint forall(sameRoom in SameRoomHard, c1,c2 in sameRoom where c1<c2)(
    same_room(c1,c2)
);

% Dist SameRoom Violations
constraint forall(s in 1..length(SameRoomSoft))(
    SameRoomViolations[s] >= sum(c1,c2 in SameRoomSoft[s] where c1<c2 /\ not(same_room(c1,c2)))(1)
);

% Dist DifferentRoom 
constraint forall(diffRoom in DifferentRoomHard, c1,c2 in diffRoom where c1<c2)(
    not(same_room(c1,c2))
);

% Dist DifferentRoom Violations
constraint forall(s in 1..length(DifferentRoomSoft))(
    DifferentRoomViolations[s] >= sum(c1,c2 in DifferentRoomSoft[s] where c1<c2 /\ same_room(c1,c2))(1)
);

% Dist SameStart
constraint forall(sameStart in SameStartHard, c1,c2 in sameStart where c1<c2)(
    same_start(c1,c2)
);

% Dist SameStart Violations
constraint forall(s in 1..length(SameStartSoft))(
    SameStartViolations[s] >= sum(c1,c2 in SameStartSoft[s] where c1<c2 /\ not(same_start(c1,c2)))(1)
);

% Dist SameTime 
constraint forall(sameTime in SameTimeHard, c1,c2 in sameTime where c1<c2)(
    same_time(c1,c2)
);

% Dist SameTime Violations
constraint forall(s in 1..length(SameTimeSoft))(
    SameTimeViolations[s] >= sum(c1,c2 in SameTimeSoft[s] where c1<c2 /\ not(same_time(c1,c2)))(1)
);

% Dist DifferentTime 
constraint forall(diffTime in DifferentTimeHard, c1,c2 in diffTime where c1<c2)(
    not(same_time(c1,c2))
);

% Dist DifferentTime Violations
constraint forall(s in 1..length(DifferentTimeSoft))(
    DifferentTimeViolations[s] >= sum(c1,c2 in DifferentTimeSoft[s] where c1<c2 /\ same_time(c1,c2))(1)
);

% Dist Precedence
constraint forall(diffTime in DifferentTimeHard, c1,c2 in diffTime where c1<c2)(
    precede(c1,c2)
);

% Dist Precedence Violations
constraint forall(s in 1..length(PrecedenceSoft))(
    PrecedenceViolations[s] >= sum(c1,c2 in PrecedenceSoft[s] where c1<c2 /\ not(precede(c1,c2)))(1)
);

% Dist SameDays
constraint forall(sameDays in SameDaysHard, c1,c2 in sameDays where c1<c2)(
    same_days(c1,c2)
);

% Dist SameDays Violations
constraint forall(s in 1..length(SameDaysSoft))(
    SameDaysViolations[s] >= sum(c1,c2 in SameDaysSoft[s] where c1<c2 /\ not(same_days(c1,c2)))(1)
);

% Dist DifferentDays
constraint forall(diffDays in DifferentDaysHard, c1,c2 in diffDays where c1<c2)(
    not(same_days(c1,c2))
);

% Dist DifferentDays Violations
constraint forall(s in 1..length(DifferentDaysSoft))(
    DifferentDaysViolations[s] >= sum(c1,c2 in DifferentDaysSoft[s] where c1<c2 /\ same_days(c1,c2))(1)
);


% Dist SameWeeks
constraint forall(sameWeeks in SameWeeksHard, c1,c2 in sameWeeks where c1<c2)(
    same_weeks(c1,c2)
);

% Dist SameWeeks Violations
constraint forall(s in 1..length(SameWeeksSoft))(
    SameWeeksViolations[s] >= sum(c1,c2 in SameWeeksSoft[s] where c1<c2 /\ not(same_weeks(c1,c2)))(1)
);

% Dist DifferentWeeks
constraint forall(diffWeeks in DifferentWeeksHard, c1,c2 in diffWeeks where c1<c2)(
    not(same_weeks(c1,c2))
);

% Dist DifferentWeeks Violations
constraint forall(s in 1..length(DifferentWeeksSoft))(
    DifferentWeeksViolations[s] >= sum(c1,c2 in DifferentWeeksSoft[s] where c1<c2 /\ same_weeks(c1,c2))(1)
);

% Dist WorkDay
constraint forall(i in 1..length(WorkDayHard), c1,c2 in WorkDayHard[i] where c1<c2)(
    workday(c1,c2,WorkDayHardParameters[i])
);

% TODO Dist WorkDay Violations

% Dist MinGap
constraint forall(i in 1..length(MinGapHard), c1,c2 in MinGapHard[i] where c1<c2)(
    mingap(c1,c2,MinGapHardParameters[i])
);

% TODO Dist MinGap Violations

% Dist MaxDays
%constraint forall(i in 1..length(MaxDaysHard), c in MaxDaysHard[i])(
%    maxdays(c,MaxDaysHardParameters[i])
%);

% TODO Dist MaxDays Violations

% Dist MaxDayLoad
%constraint forall(i in 1..length(MaxDayLoadHard))(
%    maxdayload(MaxDayLoadHard[i],MaxDayLoadHardParameters[i])
%);

% TODO Dist MaxDayLoad Violations

% TODO Dist MaxBreaks
%constraint forall(i in 1..length(MaxBreaksHard))(
%    maxbreaks(MaxBreaksHard[i],MaxBreaksHardParameters[i][1],MaxBreaksHardParameters[i][2])
%);

% TODO Dist MaxBreaks Violations

% TODO Dist MaxBlock


% TODO Dist MaxBlock Violations


solve :: int_search(ScheduledTime, smallest, indomain_min, complete)
    minimize sum(c in Classes)(ClassRoomPenalties[c,ScheduledRoom[c]])
       + sum(c in Classes)(ClassSchedulePenalties[c,ScheduledTime[c]])
       + sum(s in 1..length(SameStartSoft))(SameStartViolations[s]*SameStartPenalties[s])
       + sum(s in 1..length(SameTimeSoft))(SameTimeViolations[s]*SameTimePenalties[s])
       + sum(s in 1..length(DifferentTimeSoft))(DifferentTimeViolations[s]*DifferentTimePenalties[s])
       + sum(s in 1..length(SameDaysSoft))(SameDaysViolations[s]*SameDaysPenalties[s])
       + sum(s in 1..length(DifferentDaysSoft))(DifferentDaysViolations[s]*DifferentDaysPenalties[s])
       + sum(s in 1..length(SameWeeksSoft))(SameWeeksViolations[s]*SameWeeksPenalties[s])
       + sum(s in 1..length(DifferentWeeksSoft))(DifferentWeeksViolations[s]*DifferentWeeksPenalties[s])
       + sum(s in 1..length(SameRoomSoft))(SameRoomViolations[s]*SameRoomPenalties[s])
       + sum(s in 1..length(DifferentRoomSoft))(DifferentRoomViolations[s]*DifferentRoomPenalties[s])
       + sum(s in 1..length(OverlapSoft))(OverlapViolations[s]*OverlapPenalties[s])
       + sum(s in 1..length(NotOverlapSoft))(NotOverlapViolations[s]*NotOverlapPenalties[s])
       + sum(s in 1..length(SameAttendeesSoft))(SameAttendeesViolations[s]*SameAttendeesPenalties[s])
       + sum(s in 1..length(PrecedenceSoft))(PrecedenceViolations[s]*PrecedencePenalties[s])
;

%solve :: int_search(ScheduledTime, smallest, indomain_min, complete) satisfy;

% Pretty print output
output [ concat([
        "A," ++ show(c) ++
        "," ++ show(t) ++
        "," ++ show(ScheduledRoom[c]) ++
        "," ++ show(ClassRoomPenalties[c,ScheduledRoom[c]]) ++ "\n"
    | c in Classes, t in Schedules where t==fix(ScheduledTime[c])])
];

output [
    "\nSameStartViolations: " ++ show(SameStartViolations) ++
    "\nSameTimeViolations: " ++ show(SameTimeViolations) ++
    "\nDifferentTimeViolations: " ++ show(DifferentTimeViolations) ++
    "\nSameDaysViolations: " ++ show(SameDaysViolations) ++
    "\nDifferentDaysViolations: " ++ show(DifferentDaysViolations) ++
    "\nSameWeeksViolations: " ++ show(SameWeeksViolations) ++
    "\nDifferentWeeksViolations: " ++ show(DifferentWeeksViolations) ++
    "\nSameRoomViolations: " ++ show(SameRoomViolations) ++
    "\nDifferentRoomViolations: " ++ show(DifferentRoomViolations) ++
    "\nOverlapViolations: " ++ show(OverlapViolations) ++
    "\nNotOverlapViolations: " ++ show(NotOverlapViolations) ++
    "\nSameAttendeesViolations: " ++ show(SameAttendeesViolations) ++
    "\nPrecedenceViolations: " ++ show(PrecedenceViolations)
];

output [
    "\n\nSchedulePenalties: " ++ show(sum(c in Classes)(ClassSchedulePenalties[c,ScheduledTime[c]])) ++
    "\nRoomPenalties: " ++ show(sum(c in Classes)(ClassRoomPenalties[c,ScheduledRoom[c]])) ++
    "\nSameStartPenalty: " ++ show(sum(s in 1..length(SameStartSoft))(SameStartViolations[s]*SameStartPenalties[s])) ++
    "\nSameTimePenalty: " ++ show(sum(s in 1..length(SameTimeSoft))(SameTimeViolations[s]*SameTimePenalties[s])) ++
    "\nDifferentTimePenalty: " ++ show(sum(s in 1..length(DifferentTimeSoft))(DifferentTimeViolations[s]*DifferentTimePenalties[s])) ++
    "\nSameRoomPenalty: " ++ show(sum(s in 1..length(SameRoomSoft))(SameRoomViolations[s]*SameRoomPenalties[s])) ++
    "\nOverlapPenalty: " ++ show(sum(s in 1..length(OverlapSoft))(OverlapViolations[s]*OverlapPenalties[s])) ++
    "\nNotOverlapPenalty: " ++ show(sum(s in 1..length(NotOverlapSoft))(NotOverlapViolations[s]*NotOverlapPenalties[s])) ++
    "\nSameAttendeesPenalty: " ++ show(sum(s in 1..length(SameAttendeesSoft))(SameAttendeesViolations[s]*SameAttendeesPenalties[s])) ++
    "\nPrecedencePenalty: " ++ show(sum(s in 1..length(PrecedenceSoft))(PrecedenceViolations[s]*PrecedencePenalties[s]))
];
