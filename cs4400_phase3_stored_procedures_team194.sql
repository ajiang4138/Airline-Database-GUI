-- CS4400: Introduction to Database Systems: Monday, March 3, 2025
-- Simple Airline Management System Course Project Mechanics [TEMPLATE] (v0)
-- Views, Functions & Stored Procedures

/* This is a standard preamble for most of our scripts.  The intent is to establish
a consistent environment for the database behavior. */
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

set @thisDatabase = 'flight_tracking';
use flight_tracking;
-- -----------------------------------------------------------------------------
-- stored procedures and views
-- -----------------------------------------------------------------------------
/* Standard Procedure: If one or more of the necessary conditions for a procedure to
be executed is false, then simply have the procedure halt execution without changing
the database state. Do NOT display any error messages, etc. */

-- [_] supporting functions, views and stored procedures
-- -----------------------------------------------------------------------------
/* Helpful library capabilities to simplify the implementation of the required
views and procedures. */
-- -----------------------------------------------------------------------------
drop function if exists leg_time;
delimiter //
create function leg_time (ip_distance integer, ip_speed integer)
	returns time reads sql data
begin
	declare total_time decimal(10,2);
    declare hours, minutes integer default 0;
    set total_time = ip_distance / ip_speed;
    set hours = truncate(total_time, 0);
    set minutes = truncate((total_time - hours) * 60, 0);
    return maketime(hours, minutes, 0);
end //
delimiter ;

-- [1] add_airplane()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new airplane.  A new airplane must be sponsored
by an existing airline, and must have a unique tail number for that airline.
username.  An airplane must also have a non-zero seat capacity and speed. An airplane
might also have other factors depending on it's type, like the model and the engine.  
Finally, an airplane must have a new and database-wide unique location
since it will be used to carry passengers. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_airplane;
delimiter //
create procedure add_airplane (in ip_airlineID varchar(50), in ip_tail_num varchar(50),
	in ip_seat_capacity integer, in ip_speed integer, in ip_locationID varchar(50),
    in ip_plane_type varchar(100), in ip_maintenanced boolean, in ip_model varchar(50),
    in ip_neo boolean)
sp_main: begin
	
    -- edge cases
    if ip_seat_capacity <= 0 or ip_speed <= 0 then
		leave sp_main;
	end if;
    
    if not exists (select 1 from airline where airlineID = ip_airlineID) then
		leave sp_main;
	end if;
    
    if ip_airlineID is NULL or ip_tail_num is NULL or ip_seat_capacity is NULL or ip_speed is NULL or ip_locationID is NULL then
		leave sp_main;
	end if;
    
    -- Ensure that the plane type is valid: Boeing, Airbus, or neither
    if ip_plane_type not in ('Boeing', 'Airbus') and ip_plane_type is not NULL then
		leave sp_main;
	end if;
    
    -- Ensure that the type-specific attributes are accurate for the type
    if ip_plane_type = 'Boeing' and ip_neo is not NULL then
		leave sp_main;
	end if;
    
    if ip_plane_type = 'Airbus' and (ip_maintenanced is not NULL or ip_model is not NULL) then
		leave sp_main;
	end if;
    
    if ip_plane_type is NULL and (ip_maintenanced is not NULL or ip_model is not NULL or ip_neo is not NULL) then
		leave sp_main;
	end if;
    
    -- Ensure that the airplane and location values are new and unique
    if exists (select 1 from airplane where tail_num = ip_tail_num and airlineID = ip_airlineID) then
		leave sp_main;
	end if;
    
    if exists (select 1 from location where locationID = ip_locationID) then
		leave sp_main;
	end if;
    
    -- Add airplane and location into respective tables
    insert into location (locationID) values
		(ip_locationID);
	
    insert into airplane (airlineID, tail_num, seat_capacity, speed, locationID, plane_type, maintenanced, model, neo) values
		(ip_airlineID, ip_tail_num, ip_seat_capacity, ip_speed, ip_locationID,
         ip_plane_type, ip_maintenanced, ip_model, ip_neo);

end //
delimiter ;

-- [2] add_airport()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new airport.  A new airport must have a unique
identifier along with a new and database-wide unique location if it will be used
to support airplane takeoffs and landings.  An airport may have a longer, more
descriptive name.  An airport must also have a city, state, and country designation. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_airport;
delimiter //
create procedure add_airport (in ip_airportID char(3), in ip_airport_name varchar(200),
    in ip_city varchar(100), in ip_state varchar(100), in ip_country char(3), in ip_locationID varchar(50))
sp_main: begin

	-- edge cases
    if ip_airportID is NULL or ip_city is NULL or ip_state is NULL or ip_country is NULL or ip_locationID is NULL then
		leave sp_main;
	end if;

	-- Ensure that the airport and location values are new and unique
    if exists (select 1 from airport where airportID = ip_airportID) then
		leave sp_main;
	end if;
    
    if exists (select 1 from location where locationID = ip_locationID) then
		leave sp_main;
	end if;
    
    -- Add airport and location into respective tables
    insert into location (locationID) values
		(ip_locationID);
	
    insert into airport (airportID, airport_name, city, state, country, locationID) values
		(ip_airportID, ip_airport_name, ip_city, ip_state, ip_country, ip_locationID);

end //
delimiter ;

-- [3] add_person()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new person.  A new person must reference a unique
identifier along with a database-wide unique location used to determine where the
person is currently located: either at an airport, or on an airplane, at any given
time.  A person must have a first name, and might also have a last name.

A person can hold a pilot role or a passenger role (exclusively).  As a pilot,
a person must have a tax identifier to receive pay, and an experience level.  As a
passenger, a person will have some amount of frequent flyer miles, along with a
certain amount of funds needed to purchase tickets for flights. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_person;
delimiter //
create procedure add_person (in ip_personID varchar(50), in ip_first_name varchar(100),
    in ip_last_name varchar(100), in ip_locationID varchar(50), in ip_taxID varchar(50),
    in ip_experience integer, in ip_miles integer, in ip_funds integer)
sp_main: begin

	-- edge cases
    if ip_personID is NULL or ip_first_name is NULL or ip_locationID is NULL then
		leave sp_main;
	end if;
    
    if ip_experience < 0 then
		leave sp_main;
	end if;
    
    if ip_miles < 0 or ip_funds < 0 then
		leave sp_main;
	end if;

	-- Ensure that the location is valid
    if not exists (select 1 from location where locationID = ip_locationID) then
		leave sp_main;
	end if;
    
    -- Ensure that the persion ID is unique
    if exists (select 1 from person where personID = ip_personID) then
		leave sp_main;
	end if;
    
    -- Ensure that the person is a pilot or passenger
    if (ip_taxID is not NULL or ip_experience is not NULL) and (ip_miles is not NULL or ip_funds is not NULL) then
		leave sp_main;
	end if;
    
    if (ip_taxID is NOT NULL and ip_experience is NULL) then
		leave sp_main;
	end if;
    
    if (ip_taxID is NULL and ip_experience is not NULL) then
		leave sp_main;
	end if;
    
    if (ip_miles is not NULL and ip_funds is NULL) then
		leave sp_main;
	end if;
    
    if (ip_miles is NULL and ip_funds is not NULL) then
		leave sp_main;
	end if;
    
    -- Add them to the person table as well as the table of their respective role
	insert into person (personID, first_name, last_name, locationID) values
		(ip_personID, ip_first_name, ip_last_name, ip_locationID);
        
	if (ip_taxID is not NULL and ip_experience is not NULL) then
		insert into pilot (personID, taxID, experience, commanding_flight) values
			(ip_personID, ip_taxID, ip_experience, NULL);
	end if;
    
    if (ip_miles is not NULL and ip_funds is not NULL) then
		insert into passenger (personID, miles, funds) values
			(ip_personID, ip_miles, ip_funds);
	end if;
    
end //
delimiter ;

-- [4] grant_or_revoke_pilot_license()
-- -----------------------------------------------------------------------------
/* This stored procedure inverts the status of a pilot license.  If the license
doesn't exist, it must be created; and, if it aready exists, then it must be removed. */
-- -----------------------------------------------------------------------------
drop procedure if exists grant_or_revoke_pilot_license;
delimiter //
create procedure grant_or_revoke_pilot_license (in ip_personID varchar(50), in ip_license varchar(100))
sp_main: begin
	
    -- edge cases
    if ip_personID is NULL or ip_license is NULL then
		leave sp_main;
	end if;

	-- Ensure that the person is a valid pilot
    if not exists (select * from pilot where personID = ip_personID) then leave sp_main;
		end if;
    -- If license exists, delete it, otherwise add the license
	if exists (select * from pilot_licenses where (personID = ip_personID and license = ip_license)) then
    delete from pilot_licenses where (personID = ip_personID and license = ip_license);
    
    else insert into pilot_licenses(personID, license) values
    (ip_personID, ip_license);
		end if;

end //
delimiter ;

-- [5] offer_flight()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new flight.  The flight can be defined before
an airplane has been assigned for support, but it must have a valid route.  And
the airplane, if designated, must not be in use by another flight.  The flight
can be started at any valid location along the route except for the final stop,
and it will begin on the ground.  You must also include when the flight will
takeoff along with its cost. */
-- -----------------------------------------------------------------------------
drop procedure if exists offer_flight;
delimiter //
create procedure offer_flight (in ip_flightID varchar(50), in ip_routeID varchar(50),
    in ip_support_airline varchar(50), in ip_support_tail varchar(50), in ip_progress integer,
    in ip_next_time time, in ip_cost integer)
sp_main: begin
	
    -- edge cases
    if exists (select 1 from flight where support_tail = ip_support_tail) then
		leave sp_main;
	end if;
    
    if exists (select 1 from flight where flightID = ip_flightID) then
		leave sp_main;
	end if;
    
    if ip_flightID is NULL or ip_routeID is NULL or ip_support_airline is NULL or ip_next_time is NULL or ip_cost is NULL then
		leave sp_main;
	end if;

	-- Ensure that the airplane exists
    if not exists (select 1 from airplane where tail_num = ip_support_tail and airlineID = ip_support_airline) then
		leave sp_main;
	end if;

    -- Ensure that the route exists
    if not exists (select 1 from route where routeID = ip_routeID) then
		leave sp_main;
	end if;
    
    -- Ensure that the progress is less than the length of the route
    if ip_progress < 0 or (select count(*) from route_path where routeID = ip_routeID) <= ip_progress then
		leave sp_main;
	end if;
    
    -- Create the flight with the airplane starting in on the ground
    insert into flight (flightID, routeID, support_airline, support_tail, progress, airplane_status, next_time, cost) values
		(ip_flightID, ip_routeID, ip_support_airline, ip_support_tail, ip_progress, 'on_ground', ip_next_time, ip_cost);

end //
delimiter ;

-- [6] flight_landing()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for a flight landing at the next airport
along it's route.  The time for the flight should be moved one hour into the future
to allow for the flight to be checked, refueled, restocked, etc. for the next leg
of travel.  Also, the pilots of the flight should receive increased experience, and
the passengers should have their frequent flyer miles updated. */
-- -----------------------------------------------------------------------------
drop procedure if exists flight_landing;
delimiter //
create procedure flight_landing (in ip_flightID varchar(50))
sp_main: begin
declare flight_miles integer default 0;
declare landing_progress integer;
    
	-- Ensure that the flight exists
    if not exists (select 1 from flight where flightID = ip_flightID) then
		leave sp_main;
	end if;
    
    -- Ensure that the flight is in the air
    if (select airplane_status from flight where flightID = ip_flightID) != 'in_flight' then
		leave sp_main;
	end if;
    
    -- Increment the pilot's experience by 1
    update pilot 
		set experience = experience + 1 
		where commanding_flight = ip_flightID;
        
    -- Increment the frequent flyer miles of all passengers on the plane
    select progress into landing_progress from flight where flightID = ip_flightID;
    
    select l.distance into flight_miles from flight f
    join route_path r on f.routeID = r.routeID
    join leg l on r.legID = l.legID
    where f.flightID = ip_flightID and r.sequence = landing_progress;
        
	update passenger
		set miles = miles + flight_miles
        where personID in (select personID from (select a.personID from person p inner join passenger a on p.personID = a.personID
        where p.locationID = (select locationID from airplane
        where tail_num = (select support_tail from flight
        where flightID = ip_flightID))) as subquery);
        
    -- Update the status of the flight and increment the next time to 1 hour later
		-- Hint: use addtime()
	update flight
		set airplane_status = 'on_ground',
			next_time = addtime(next_time, '1:00:00')
		where flightID = ip_flightID;


end //
delimiter ;

-- [7] flight_takeoff()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for a flight taking off from its current
airport towards the next airport along it's route.  The time for the next leg of
the flight must be calculated based on the distance and the speed of the airplane.
And we must also ensure that Airbus and general planes have at least one pilot
assigned, while Boeing must have a minimum of two pilots. If the flight cannot take
off because of a pilot shortage, then the flight must be delayed for 30 minutes. */
-- -----------------------------------------------------------------------------
drop procedure if exists flight_takeoff;
delimiter //
create procedure flight_takeoff (in ip_flightID varchar(50))
sp_main: begin
    declare takeoff_progress integer;
    declare plane_type varchar(50);
    declare pilot_amount integer;
    declare leg_distance integer;
    declare plane_speed integer;
    declare travel_time time;
    
    select progress+1 into takeoff_progress from flight where flightID = ip_flightID;
    
    select a.plane_type into plane_type from airplane as a join flight as f on a.tail_num = f.support_tail
    where f.flightID = ip_flightID;
    
    select count(*) into pilot_amount from pilot
	where commanding_flight = ip_flightID;

	-- Ensure that the flight exists
    if not exists (select 1 from flight where flightID = ip_flightID) then
		leave sp_main;
	end if;
    
    -- Ensure that the flight is on the ground
    if (select airplane_status from flight where flightID = ip_flightID) != 'on_ground' then
		leave sp_main;
	end if;

    -- Ensure that the flight has another leg to fly
    if (select max(sequence) from route_path 
		where routeID = (select routeID from flight 
		where flightID = ip_flightID)) = (select progress from flight where flightID = ip_flightID) then
		leave sp_main;
	end if;
    
    -- Ensure that there are enough pilots (1 for Airbus and general, 2 for Boeing)
    -- If there are not enough, move next time to 30 minutes later
    if plane_type = 'Airbus' or plane_type = 'general' then
		if pilot_amount < 1 then
			update flight
				set next_time = addtime(next_time, '0:30:00')
			where flightID = ip_flightID;
            leave sp_main;
		end if;
	end if;
    
    if plane_type = 'Boeing' then
		if pilot_amount < 2 then
			update flight
				set next_time = addtime(next_time, '0:30:00')
			where flightID = ip_flightID;
            leave sp_main;
		end if;
	end if;
        
	-- Increment the progress and set the status to in flight
    update flight
		set progress = progress + 1,
			airplane_status = 'in_flight'
	where flightID = ip_flightID;
    
    -- Calculate the flight time using the speed of airplane and distance of leg
    select l.distance into leg_distance from flight f
    join route_path r on f.routeID = r.routeID
    join leg l on r.legID = l.legID
    where f.flightID = ip_flightID and r.sequence = takeoff_progress;
    
    select speed into plane_speed from airplane
	where tail_num = (select support_tail from flight
    where flightID = ip_flightID);
    
    set travel_time = sec_to_time((leg_distance/plane_speed) * 3600);
		
    -- Update the next time using the flight time
    update flight
		set next_time = addtime(next_time, travel_time)
	where flightID = ip_flightID;

end //
delimiter ;

-- [8] passengers_board()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for passengers getting on a flight at
its current airport.  The passengers must be at the same airport as the flight,
and the flight must be heading towards that passenger's desired destination.
Also, each passenger must have enough funds to cover the flight.  Finally, there
must be enough seats to accommodate all boarding passengers. */
-- -----------------------------------------------------------------------------
drop procedure if exists passengers_board;
delimiter //
create procedure passengers_board (in ip_flightID varchar(50))
sp_main: begin
declare on_plane integer;
    declare board_plane integer;
    declare plane_tail varchar(50);
    declare current_location varchar(50);
    declare current_airport char(3);

	-- Ensure the flight exists
    if not exists (select 1 from flight where flightID = ip_flightID) then
		leave sp_main;
	end if;
    
    -- Ensure that the flight is on the ground
    if (select airplane_status from flight where flightID = ip_flightID) != 'on_ground' then
		leave sp_main;
	end if;
    
    -- Ensure that the flight has further legs to be flown
    if (select progress from flight where flightID = ip_flightID) = (select max(sequence) from route_path 
		where routeID = (select routeID from flight 
		where flightID = ip_flightID)) then
        leave sp_main;
	end if;
    
    -- Determine the number of passengers attempting to board the flight
    select support_tail into plane_tail from flight where flightID = ip_flightID;
    
    select count(*) into on_plane from passenger a join person p on a.personID = p.personID 
    where p.locationID = (select locationID from airplane where tail_num = plane_tail);
    
    -- Use the following to check:
		-- The airport the airplane is currently located at
        -- The passengers are located at that airport
        -- The passenger's immediate next destination matches that of the flight
        -- The passenger has enough funds to afford the flight
	select a.locationID, l.arrival into current_location, current_airport from flight f 
    join route_path r on f.routeID = r.routeID and r.sequence = (select progress + 1 from flight where flightID = ip_flightID) 
    join leg l on r.legID = l.legID 
    join airport a on l.departure = a.airportID 
	where f.flightID = ip_flightID;
    
    select count(distinct p.personID) into board_plane from person p 
    join passenger_vacations v on p.personID = v.personID 
    join passenger a on p.personID = a.personID
	where p.locationID = current_location and v.sequence = 1 and v.airportID = current_airport and a.funds >= (select cost from flight where flightID = ip_flightID);
        
	-- Check if there enough seats for all the passengers
		-- If not, do not add board any passengers
        -- If there are, board them and deduct their funds
	if board_plane + on_plane > (select seat_capacity from airplane where tail_num = plane_tail) then
		leave sp_main;
	end if;
    
    update passenger a join (
		select p.personID as pid from person p 
        join passenger a on p.personID = a.personID 
        join passenger_vacations v on p.personID = v.personID 
        where p.locationID = current_location and v.sequence = 1 and v.airportID = current_airport and a.funds >= (select cost from flight where flightID = ip_flightID)) as subq on a.personID = subq.pid
	set a.funds = a.funds - (select cost from flight where flightID = ip_flightID);
    
    update person p join (
       select p.personID as pid from person p 
       join passenger_vacations v on p.personID = v.personID 
       join passenger a on p.personID = a.personID
       where p.locationID = current_location and v.sequence = 1 and v.airportID = current_airport) as subq on p.personID = subq.pid
    set p.locationID = (select locationID from airplane where tail_num = plane_tail);
    
    update airline 
		set revenue = revenue + (board_plane * (select cost from flight where flightID = ip_flightID)) 
	where airlineID = (select support_airline from flight where flightID = ip_flightID);

end //
delimiter ;

-- [9] passengers_disembark()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for passengers getting off of a flight
at its current airport.  The passengers must be on that flight, and the flight must
be located at the destination airport as referenced by the ticket. */
-- -----------------------------------------------------------------------------
drop procedure if exists passengers_disembark;
delimiter //
create procedure passengers_disembark (in ip_flightID varchar(50))
sp_main: begin
	declare airplane_locationID varchar(50);
    declare current_legID varchar(50);
    declare current_airportID char(3);
    declare airport_locationID varchar(50);
    
	-- Ensure the flight exists
    if not exists (select 1 from flight where flightID = ip_flightID) then
		leave sp_main;
	end if;
    
    -- Ensure that the flight is on the ground
    if (select airplane_status from flight where flightID = ip_flightID) != 'on_ground' then
		leave sp_main;
	end if;
    
    select a.locationID into airplane_locationID from flight f 
    join airplane a on f.support_tail = a.tail_num
    where flightID = ip_flightID;
    
    select l.legID into current_legID from flight f
    join route_path r on f.routeID = r.routeID and f.progress = r.sequence
    join leg l on r.legID = l.legID
    where flightID = ip_flightID;
    
    select arrival into current_airportID from leg where legID = current_legID;
    select locationID into airport_locationID from airport where airportID = current_airportID;
    
    -- Determine the list of passengers who are disembarking
	-- select personID from person where locationID = current_location;
    
	-- Use the following to check:
		-- Passengers must be on the plane supporting the flight
        -- Passenger has reached their immediate next destionation airport
        
	-- Move the appropriate passengers to the airport
    -- Update the vacation plans of the passengers
    
    update person p 
    join passenger pa on p.personID = pa.personID
    join (
		select v.personID, min(v.sequence) as next_sequence from passenger_vacations v
        where v.airportID = current_airportID 
        group by v.personID
    ) as next_sequences on p.personID = next_sequences.personID
		set p.locationID = airport_locationID
    where p.locationID = airplane_locationID;
    
    delete v from passenger_vacations v
	join (
		select p.personID, min(v2.sequence) as next_sequence 
		from person p join passenger_vacations v2 on p.personID = v2.personID
		where p.locationID = airport_locationID
		group by p.personID
	) as exiting on v.personID = exiting.personID and v.sequence = exiting.next_sequence and v.airportID = current_airportID;
    
end //
delimiter ;

-- [10] assign_pilot()
-- -----------------------------------------------------------------------------
/* This stored procedure assigns a pilot as part of the flight crew for a given
flight.  The pilot being assigned must have a license for that type of airplane,
and must be at the same location as the flight.  Also, a pilot can only support
one flight (i.e. one airplane) at a time.  The pilot must be assigned to the flight
and have their location updated for the appropriate airplane. */
-- -----------------------------------------------------------------------------
drop procedure if exists assign_pilot;
delimiter //
create procedure assign_pilot (in ip_flightID varchar(50), ip_personID varchar(50))
sp_main: begin
declare model varchar(100);
    declare plane_loc varchar(50);

	-- Ensure the flight exists
    if not exists (select 1 from flight where flightID = ip_flightID) then
		leave sp_main;
	end if;
    
    -- Ensure that the flight is on the ground
    if (select airplane_status from flight where flightID = ip_flightID) != 'on_ground' then
		leave sp_main;
	end if;
    
    -- Ensure that the flight has further legs to be flown
    if (select max(sequence) from route_path 
		where routeID = (select routeID from flight 
		where flightID = ip_flightID)) = (select progress from flight where flightID = ip_flightID) then
		leave sp_main;
	end if;
    
    -- Ensure that the pilot exists and is not already assigned
    if not exists (select 1 from pilot where personID = ip_personID) then
		leave sp_main;
	end if;
    
    if (select commanding_flight from pilot where personID = ip_personID) is not null then
		leave sp_main;
	end if;
    
	-- Ensure that the pilot has the appropriate license
    select plane_type into model from airplane
    where tail_num = (select support_tail from flight
	where flightID = ip_flightID);
    
    if not exists (select 1 from pilot_licenses where personID = ip_personID and license = model) then
		leave sp_main;
	end if;
    
    -- Ensure the pilot is located at the airport of the plane that is supporting the flight
    select locationID into plane_loc from airport 
    where airportID = (select departure from leg
    where legID = (select legID from route_path
    where routeID = (select routeID from flight where flightID = ip_flightID) 
    and sequence = (select progress + 1 from flight where flightID = ip_flightID)));
    
    if (select locationID from person where personID = ip_personID) != plane_loc then
        leave sp_main;
	end if;
    
    -- Assign the pilot to the flight and update their location to be on the plane
    update pilot
		set commanding_flight = ip_flightID
	where personID = ip_personID;
    
    update person
		set locationID = (select locationID from airplane 
			where tail_num = (select support_tail from flight where flightID = ip_flightID))
	where personID = ip_personID;

end //
delimiter ;

-- [11] recycle_crew()
-- -----------------------------------------------------------------------------
/* This stored procedure releases the assignments for a given flight crew.  The
flight must have ended, and all passengers must have disembarked. */
-- -----------------------------------------------------------------------------
drop procedure if exists recycle_crew;
delimiter //
create procedure recycle_crew (in ip_flightID varchar(50))
sp_main: begin
declare arrival_airport char(3);

	-- Ensure that the flight is on the ground
    if (select airplane_status from flight where flightID = ip_flightID) != 'on_ground' then
		leave sp_main;
	end if;
    
    -- Ensure that the flight does not have any more legs
    if (select progress from flight where flightID = ip_flightID) != (select max(sequence) from route_path 
		where routeID = (select routeID from flight 
		where flightID = ip_flightID)) then
		leave sp_main;
	end if;
    
    -- Ensure that the flight is empty of passengers
    if (select count(*) from person p inner join passenger a on p.personID = a.personID 
		where locationID = (select locationID from airplane 
		where tail_num = (select support_tail from flight where flightID = ip_flightID))) != 0 then
        leave sp_main;
	end if;
    
    -- Update assignments of all pilots
    -- Move all pilots to the airport the plane of the flight is located at
    
    select arrival into arrival_airport from leg
    where legID = (select legID from route_path
    where routeID = (select routeID from flight
    where flightID = ip_flightID));
    
    update person
		set locationID = (select locationID from airport where airportID = arrival_airport)
		where personID in (select personID from (select i.personID from person p inner join pilot i on p.personID = i.personID
        where i.commanding_flight = ip_flightID)as subquery);
        
	update pilot
		set commanding_flight = null
	where commanding_flight = ip_flightID;

end //
delimiter ;

-- [12] retire_flight()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a flight that has ended from the system.  The
flight must be on the ground, and either be at the start its route, or at the
end of its route.  And the flight must be empty - no pilots or passengers. */
-- -----------------------------------------------------------------------------
drop procedure if exists retire_flight;
delimiter //
create procedure retire_flight (in ip_flightID varchar(50))
sp_main: begin

	-- Ensure that the flight is on the ground
    if (select airplane_status from flight where flightID = ip_flightID) != 'on_ground' then
		leave sp_main;
	end if;
    
    -- Ensure that the flight does not have any more legs
    if (select progress from flight where flightID = ip_flightID) not in (0, (select max(sequence) from route_path 
		where routeID = (select routeID from flight where flightID = ip_flightID))) then
		leave sp_main;
	end if;
    
    -- Ensure that there are no more people on the plane supporting the flight
    if (select count(*) from person p
		where locationID = (select locationID from airplane 
		where tail_num = (select support_tail from flight where flightID = ip_flightID))) != 0 then
        leave sp_main;
	end if;
    
    -- Remove the flight from the system
    delete from flight where flightID = ip_flightID;

end //
delimiter ;

-- [13] simulation_cycle()
-- -----------------------------------------------------------------------------
/* This stored procedure executes the next step in the simulation cycle.  The flight
with the smallest next time in chronological order must be identified and selected.
If multiple flights have the same time, then flights that are landing should be
preferred over flights that are taking off.  Similarly, flights with the lowest
identifier in alphabetical order should also be preferred.

If an airplane is in flight and waiting to land, then the flight should be allowed
to land, passengers allowed to disembark, and the time advanced by one hour until
the next takeoff to allow for preparations.

If an airplane is on the ground and waiting to takeoff, then the passengers should
be allowed to board, and the time should be advanced to represent when the airplane
will land at its next location based on the leg distance and airplane speed.

If an airplane is on the ground and has reached the end of its route, then the
flight crew should be recycled to allow rest, and the flight itself should be
retired from the system. */
-- -----------------------------------------------------------------------------
drop procedure if exists simulation_cycle;
delimiter //
create procedure simulation_cycle ()
sp_main: begin
	declare next_flight varchar(50);

	-- Identify the next flight to be processed
    select flightID into next_flight from flight
	where next_time = (select min(next_time) from flight)
    order by case when airplane_status = 'in_flight' then 1 else 100 end,
    flightID limit 1;
    
    -- If the flight is in the air:
		-- Land the flight and disembark passengers
	if (select airplane_status from flight where flightID = next_flight) = 'in_flight' then
		call flight_landing(next_flight);
		call passengers_disembark(next_flight);
            
	-- If the flight is on the ground:
		-- Board passengers and have the plane takeoff
	
    elseif (select airplane_status from flight where flightID = next_flight) = 'on_ground' then
		-- If it has reached the end:
			-- Recycle crew and retire flight
		if (select progress from flight where flightID = next_flight) >= 
			(select max(sequence) from route_path 
            where routeID = (select routeID from flight where flightID = next_flight)) then
				call recycle_crew(next_flight);
                call retire_flight(next_flight);
		else
			call passengers_board(next_flight);
            call flight_takeoff(next_flight);
		end if;
	end if;

end //
delimiter ;

-- [14] flights_in_the_air()
-- -----------------------------------------------------------------------------
/* This view describes where flights that are currently airborne are located. 
We need to display what airports these flights are departing from, what airports 
they are arriving at, the number of flights that are flying between the 
departure and arrival airport, the list of those flights (ordered by their 
flight IDs), the earliest and latest arrival times for the destinations and the 
list of planes (by their respective flight IDs) flying these flights. */
-- -----------------------------------------------------------------------------
create or replace view flights_in_the_air (departing_from, arriving_at, num_flights,
	flight_list, earliest_arrival, latest_arrival, airplane_list) as
select
l.departure as departing_from,
l.arrival as arriving_at, 
count(distinct f.flightID) as num_flights, 
group_concat(distinct f.flightID order by f.flightID asc) as flight_list,
min(f.next_time) as earliest_arrival,
max(f.next_time) as latest_arrival,
group_concat(distinct a.locationID order by a.locationID desc) as airplane_list
from leg as l
join route_path as rp on l.legID = rp.legID
join flight as f on rp.routeID = f.routeID
join airplane as a on f.support_tail = a.tail_num
where f.airplane_status = 'in_flight' and f.progress = rp.sequence
group by l.departure, l.arrival;

-- [15] flights_on_the_ground()
-- ------------------------------------------------------------------------------
/* This view describes where flights that are currently on the ground are 
located. We need to display what airports these flights are departing from, how 
many flights are departing from each airport, the list of flights departing from 
each airport (ordered by their flight IDs), the earliest and latest arrival time 
amongst all of these flights at each airport, and the list of planes (by their 
respective flight IDs) that are departing from each airport.*/
-- ------------------------------------------------------------------------------
create or replace view flights_on_the_ground (departing_from, num_flights,
	flight_list, earliest_arrival, latest_arrival, airplane_list) as 
select
l.departure as departing_from,
count(distinct f.flightID) as num_flights, 
group_concat(distinct f.flightID order by f.flightID asc) as flight_list,
min(f.next_time) as earliest_arrival,
max(f.next_time) as latest_arrival,
group_concat(distinct a.locationID order by a.locationID desc) as airplane_list
from leg as l
join route_path as rp on l.legID = rp.legID
join flight as f on rp.routeID = f.routeID
join airplane as a on f.support_tail = a.tail_num
where f.airplane_status = 'on_ground' and f.progress = 0 and rp.sequence = 1
group by l.departure

union

select
l.arrival as departing_from,
count(distinct f.flightID) as num_flights, 
group_concat(distinct f.flightID order by f.flightID asc) as flight_list,
min(f.next_time) as earliest_arrival,
max(f.next_time) as latest_arrival,
group_concat(distinct a.locationID order by a.locationID desc) as airplane_list
from leg as l
join route_path as rp on l.legID = rp.legID
join flight as f on rp.routeID = f.routeID
join airplane as a on f.support_tail = a.tail_num
where f.airplane_status = 'on_ground' and f.progress = rp.sequence
group by l.arrival;


-- [16] people_in_the_air()
-- -----------------------------------------------------------------------------
/* This view describes where people who are currently airborne are located. We 
need to display what airports these people are departing from, what airports 
they are arriving at, the list of planes (by the location id) flying these 
people, the list of flights these people are on (by flight ID), the earliest 
and latest arrival times of these people, the number of these people that are 
pilots, the number of these people that are passengers, the total number of 
people on the airplane, and the list of these people by their person id. */
-- -----------------------------------------------------------------------------
create or replace view people_in_the_air (departing_from, arriving_at, num_airplanes,
	airplane_list, flight_list, earliest_arrival, latest_arrival, num_pilots,
	num_passengers, joint_pilots_passengers, person_list) as
select
l.departure as departing_from,
l.arrival as arriving_at, 
count(distinct a.locationID) as num_airplanes,
group_concat(distinct a.locationID order by a.locationID asc) as airplane_list,
group_concat(distinct f.flightID order by f.flightID asc) as flight_list,
min(f.next_time) as earliest_arrival,
max(f.next_time) as latest_arrival,
count(distinct pi.taxID) as num_pilots,
count(pa.miles) as num_passengers,
count(pe.personID) as joint_pilots_passengers,
group_concat(distinct pe.personID order by pe.personID asc) as person_list
from leg as l
join route_path as rp on l.legID = rp.legID
join flight as f on rp.routeID = f.routeID
join airplane as a on f.support_tail = a.tail_num
join person as pe on pe.locationID = a.locationID
natural left join pilot as pi
natural left join passenger as pa
where f.airplane_status = 'in_flight' and f.progress = rp.sequence
group by l.departure, l.arrival
;

-- [17] people_on_the_ground()
-- -----------------------------------------------------------------------------
/* This view describes where people who are currently on the ground and in an 
airport are located. We need to display what airports these people are departing 
from by airport id, location id, and airport name, the city and state of these 
airports, the number of these people that are pilots, the number of these people 
that are passengers, the total number people at the airport, and the list of 
these people by their person id. */
-- -----------------------------------------------------------------------------
create or replace view people_on_the_ground (departing_from, airport, airport_name,
	city, state, country, num_pilots, num_passengers, joint_pilots_passengers, person_list) as
select distinct
aport.airportID as departing_from,
aport.locationID as airport,
aport.airport_name as airport_name,
aport.city as city,
aport.state as state,
aport.country as country,

count(distinct pi.taxID) as num_pilots,
count(pa.miles) as num_passengers,
count(pe.personID) as joint_pilots_passengers,
group_concat(distinct pe.personID order by pe.personID asc) as person_list

from airport as aport
join person as pe on aport.locationID = pe.locationID
left join pilot as pi on pe.personID = pi.personID
left join passenger as pa on pe.personID = pa.personID
group by aport.airportID
;

-- [18] route_summary()
-- -----------------------------------------------------------------------------
/* This view will give a summary of every route. This will include the routeID, 
the number of legs per route, the legs of the route in sequence, the total 
distance of the route, the number of flights on this route, the flightIDs of 
those flights by flight ID, and the sequence of airports visited by the route. */
-- -----------------------------------------------------------------------------
create or replace view route_summary (route, num_legs, leg_sequence, route_length,
	num_flights, flight_list, airport_sequence) as
select 
rp.routeID as route,
count(distinct rp.legID) as num_legs,
group_concat(distinct rp.legID order by rp.sequence asc) as leg_sequence,
sum(l.distance) as route_length,

(select count(distinct f.flightID) from flight as f where f.routeID = rp.routeID) as num_flights,
(select group_concat(distinct f.flightID order by f.flightID asc) from flight as f where f.routeID = rp.routeID) as flight_list,

group_concat(distinct concat(l.departure, '->', l.arrival) order by rp.sequence asc) as airport_sequence

from leg as l
join route_path as rp on l.legID = rp.legID
group by rp.routeID
;

-- [19] alternative_airports()
-- -----------------------------------------------------------------------------
/* This view displays airports that share the same city and state. It should 
specify the city, state, the number of airports shared, and the lists of the 
airport codes and airport names that are shared both by airport ID. */
-- -----------------------------------------------------------------------------
create or replace view alternative_airports (city, state, country, num_airports, 
	airport_code_list, airport_name_list) as
select
city,
state,
country,
count(*) as num_airports,
group_concat(airportID order by airportID separator ', ') as airport_code_list,
group_concat(airport_name order by airportID separator ', ') as airport_name_list
from airport group by city, state, country having count(*) > 1
;

