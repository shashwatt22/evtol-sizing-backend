import math

def calculate_multirotor(data):
    # Inputs
    gtow = float(data['gtow'])     
    no_of_rotor= float(data['no_of_rotor'])          
    disk_loading = float(data['bl'])                        
    cl = float(data['cl'])                
    no_of_blade = int(data['no_of_blade']) 
    rho = float(data['rho'])               
    ct = float(data['ct']) 
    cd = float(data['cd'])                 
    solidity = float(data['solidity'])    
    cd_profile = float(data['cd_profile'])
    rate_of_climb= float(data['rate_of_climb'])

    # Tip Speeds (user inputs)
       
    v_tip_cruise = float(data['v_tip_cruise'])    
    v_tip_climb = float(data['v_tip_climb'])      

    # Constants
    g = 9.81
    thrust = gtow * g
    radius = math.sqrt(gtow / (disk_loading * math.pi * no_of_rotor))
    area = math.pi * radius ** 2
    mean_chord_length = (solidity * math.pi * radius) / no_of_blade

    # Velocities
    v_stall = math.sqrt((2 * disk_loading * 9.81) / (rho * cl)) 
    v_cruise = 1.3*v_stall
    v_climb = 1.2*v_stall
    v_downwash = 0.5 * math.sqrt(rate_of_climb ** 2 + ((2 * gtow) / (rho * area))) - rate_of_climb

    #lift and drag
    lift_hover= (1/2)*rho*cl*(v_downwash**2)
    lift_cruise= (1/2)*rho*cl*(v_cruise**2)
    lift_climb= (1/2)*rho*cl*(v_climb**2)

    drag_hover= (1/2)*rho*cd*(v_downwash**2)
    drag_cruise= (1/2)*rho*cd*(v_cruise**2)
    drag_climb= (1/2)*rho*cd*(v_climb**2)

    # Angular Speeds & RPMs
    inflow_ratio_hover= math.sqrt(ct/2)
    v_tip_hover= v_downwash/inflow_ratio_hover
    omega_hover = v_tip_hover / radius
    omega_cruise = v_tip_cruise / radius
    omega_climb = v_tip_climb / radius

    rpm_hover = (60 / (2 * math.pi)) * omega_hover
    rpm_cruise = (60 / (2 * math.pi)) * omega_cruise
    rpm_climb = (60 / (2 * math.pi)) * omega_climb

    # Drag Area & Fuselage Drag
    drag_area = 4.2 * ((2.205 * gtow) / 1000) ** 0.67
    fuselage_drag_hover = 0.5 * rho * v_downwash ** 2 * drag_area
    fuselage_drag_cruise = 0.5 * rho * v_cruise ** 2 * drag_area
    fuselage_drag_climb = 0.5 * rho * v_climb ** 2 * drag_area

    # Shaft Tilt Angles
    shaft_tilt_angle_hover = math.atan(fuselage_drag_hover / thrust)
    shaft_tilt_angle_cruise = math.atan(fuselage_drag_cruise / thrust)
    shaft_tilt_angle_climb = math.atan(fuselage_drag_climb / thrust)

    # Advance Ratios
    advance_ratio_hover = (v_downwash * math.cos(shaft_tilt_angle_hover)) / (radius * omega_hover)
    advance_ratio_cruise = (v_cruise * math.cos(shaft_tilt_angle_cruise)) / (radius * omega_cruise)
    advance_ratio_climb = (v_climb * math.cos(shaft_tilt_angle_climb)) / (radius * omega_climb)

    # Inflow Ratios
    #inflow_ratio_hover = ((v_downwash * math.sin(shaft_tilt_angle_hover)) / (omega_hover * radius)) + (ct / (2 * advance_ratio_hover))
    inflow_ratio_cruise = ((v_cruise * math.sin(shaft_tilt_angle_cruise)) / (omega_cruise * radius)) + (ct / (2 * advance_ratio_cruise))
    inflow_ratio_climb = ((v_climb * math.sin(shaft_tilt_angle_climb)) / (omega_climb * radius)) + (ct / (2 * advance_ratio_climb))

    # Reynolds Number
    reynolds_number = (v_cruise * mean_chord_length) / (1.55e-5)

    # Powers
    induced_power_hover = 1.15 * ((ct ** 2) / (2 * math.sqrt(inflow_ratio_hover ** 2 + advance_ratio_hover ** 2))) * rho * area * v_downwash ** 3
    induced_power_cruise = 1.15 * ((ct ** 2) / (2 * math.sqrt(inflow_ratio_cruise ** 2 + advance_ratio_cruise ** 2))) * rho * area * v_cruise ** 3
    induced_power_climb = 1.15 * ((ct ** 2) / (2 * math.sqrt(inflow_ratio_climb ** 2 + advance_ratio_climb ** 2))) * rho * area * v_climb ** 3
    total_induced_power = (induced_power_hover + induced_power_cruise + induced_power_climb)

    profile_power_hover = (1/8) * solidity * cd_profile * (1 + 4.65 * advance_ratio_hover ** 2) * rho * area * v_downwash ** 3
    profile_power_cruise = (1/8) * solidity * cd_profile * (1 + 4.65 * advance_ratio_cruise ** 2) * rho * area * v_cruise ** 3
    profile_power_climb = (1/8) * solidity * cd_profile * (1 + 4.65 * advance_ratio_climb ** 2) * rho * area * v_climb ** 3
    total_profile_power = (profile_power_hover + profile_power_cruise + profile_power_climb)

    drag_power_hover = 0.5 * advance_ratio_hover ** 3 * (drag_area / area) * rho * area * v_downwash ** 3
    drag_power_cruise = 0.5 * advance_ratio_cruise ** 3 * (drag_area / area) * rho * area * v_cruise ** 3
    drag_power_climb = 0.5 * advance_ratio_climb ** 3 * (drag_area / area) * rho * area * v_climb ** 3
    total_drag_power = (drag_power_hover + drag_power_cruise + drag_power_climb)

    total_hover_power = (induced_power_hover + profile_power_hover + drag_power_hover)
    total_cruise_power = (induced_power_cruise + profile_power_cruise + drag_power_cruise)
    total_climb_power = (induced_power_climb + profile_power_climb + drag_power_climb)
    total_power = (total_hover_power + total_cruise_power + total_climb_power)*no_of_rotor

    return {
        # Rotor geometry
        "thrust (N)": round(thrust, 2),
        "radius (m)": round(radius, 3),
        "area (m²)": round(area, 3),
        "mean_chord_length (m)": round(mean_chord_length, 3),

        # Velocities
        "v_stall (m/s)": round(v_stall, 2),
        "v_cruise (m/s)": round(v_cruise, 2),
        "v_climb (m/s)": round(v_climb, 2),
        "v_downwash (m/s)": round(v_downwash, 2),

        # Tip Speeds (input)
        "v_tip_hover (m/s)": round(v_tip_hover, 2),
        "v_tip_cruise (m/s)": round(v_tip_cruise, 2),
        "v_tip_climb (m/s)": round(v_tip_climb, 2),

        # RPMs
        "rpm_hover ": round(rpm_hover, 2),
        "rpm_cruise": round(rpm_cruise, 2),
        "rpm_climb": round(rpm_climb, 2),

        # Omegas
        "angular_velocity_hover (rad/s)": round(omega_hover, 3),
        "angular_velocity_cruise (rad/s)": round(omega_cruise, 3),
        "angular_velocity_climb (rad/s)": round(omega_climb, 3),

        # Inflow Ratios
        "inflow_ratio_hover": round(inflow_ratio_hover, 4),
        "inflow_ratio_cruise": round(inflow_ratio_cruise, 4),
        "inflow_ratio_climb": round(inflow_ratio_climb, 4),

        # Advance Ratios
        "advance_ratio_hover": round(advance_ratio_hover, 4),
        "advance_ratio_cruise": round(advance_ratio_cruise, 4),
        "advance_ratio_climb": round(advance_ratio_climb, 4),

        # Reynolds
        "reynolds_number": round(reynolds_number),

        # Drag Area
        "drag_area (m²)": round(drag_area, 3),

        # Powers per rotor
        "induced_power_hover (W)": round(induced_power_hover, 2),
        "induced_power_cruise (W)": round(induced_power_cruise, 2),
        "induced_power_climb (W)": round(induced_power_climb, 2),

        "profile_power_hover (W)": round(profile_power_hover, 2),
        "profile_power_cruise (W)": round(profile_power_cruise, 2),
        "profile_power_climb (W)": round(profile_power_climb, 2),

        "drag_power_hover (W)": round(drag_power_hover, 2),
        "drag_power_cruise (W)": round(drag_power_cruise, 2),
        "drag_power_climb (W)": round(drag_power_climb, 2),

        "total_induced_power (W)": round(total_induced_power, 2),
        "total_profile_power (W)": round(total_profile_power, 2),
        "total_drag_power (W)": round(total_drag_power, 2),

        "total_hover_power (W)": round(total_hover_power, 2),
        "total_cruise_power (W)": round(total_cruise_power, 2),
        "total_climb_power (W)": round(total_climb_power, 2),

        #total power all rotors
        "total_power (W)": round(total_power, 2)
    }

#still incomplete as tilting power will be added later
def calculate_tiltrotor(data):
    # Inputs
    no_of_rotor = int(data['no_of_rotor'])
    no_of_blade = int(data['no_of_blade'])
    gtow = float(data['gtow'])
    disk_loading = float(data['disk loading'])
    solidity = float(data['solidity'])
    drag_area = float(data['drag_area'])
    cl = float(data['cl'])
    cd = float(data['cd'])
    cd_profile = float(data['cd_profile'])
    ct = float(data['ct'])
    rate_of_climb = float(data['rate_of_climb'])
    delta_cl = float(data['delta_cl'])
    wing_loading = float(data['wing_loading'])
    aspect_ratio = float(data['aspect_ratio'])
    rho = float(data['rho'])
    cd_induced = float(data['cd_induced'])
    v_tip_cruise= float(data['v_tip_cruise'])
    v_tip_climb= float(data['v_tip_climb'])


    #rotor parameters
    radius = math.sqrt(gtow / (disk_loading * math.pi * no_of_rotor))
    swept_area = math.pi * radius ** 2
    disk_loading = gtow / (no_of_rotor * swept_area)
    mean_chord_length = (solidity * math.pi * radius) / no_of_blade
    thrust_per_rotor = gtow / no_of_rotor
    thrust_available = no_of_rotor * swept_area * 9.81 * disk_loading

    #thrust_climb= (gtow*9.81*math.cos(theta)+ gtow*9.81*math.sin(gamma))/4*math.cos(alpha)
    #thrust_cruise=(rho*(v_cruise**2)*wing_area*cd)/8

    #wing parameters
    wing_area = gtow / wing_loading
    wing_span = math.sqrt(wing_area * aspect_ratio)


    #velocities
    v_stall = math.sqrt((2 * wing_loading * 9.81) / (rho * (cl + delta_cl)))
    v_climb = 1.2 * v_stall
    v_cruise = 1.3 * v_stall
    v_downwash = 0.5 * math.sqrt(rate_of_climb ** 2 + ((2 * gtow) / (rho * swept_area))) - rate_of_climb
    inflow_ratio_hover = math.sqrt(ct / 2)
    v_tip_hover = v_downwash / inflow_ratio_hover  #this will also go under velocities

    # Lift and Drag for Cruise
    lift_rotor_cruise = 0.5 * rho * cl * v_cruise ** 2
    lift_wing_cruise = 0.5 * rho * cl * wing_area * v_cruise ** 2
    total_lift_cruise = lift_rotor_cruise + lift_wing_cruise

    drag_rotor_cruise = 0.5 * rho * v_cruise ** 2 * cd
    drag_wing_cruise = 0.5 * rho * cd * wing_area * v_cruise ** 2
    total_drag_cruise = drag_rotor_cruise + drag_wing_cruise

    # Hover lift and drag
    lift_rotor_hover = 0.5 * rho * cl * v_downwash ** 2
    lift_wing_hover = 0.5 * rho * cl * wing_area * v_downwash ** 2
    total_lift_hover = lift_rotor_hover + lift_wing_hover

    drag_rotor_hover = 0.5 * rho * v_downwash ** 2 * cd
    drag_wing_hover = 0.5 * rho * cd * wing_area * v_downwash ** 2
    total_drag_hover = drag_rotor_hover + drag_wing_hover

    # Climb lift and drag
    lift_rotor_climb = 0.5 * rho * cl * v_climb ** 2
    lift_wing_climb = 0.5 * rho * cl * wing_area * v_climb ** 2
    total_lift_climb = lift_rotor_climb + lift_wing_climb

    drag_rotor_climb = 0.5 * rho * v_climb ** 2 * cd
    drag_wing_climb = 0.5 * rho * cd * wing_area * v_climb ** 2
    total_drag_climb = drag_rotor_climb + drag_wing_climb

    #constants
    e = (cl ** 2) / (math.pi * aspect_ratio * cd_induced)

    
    inflow_ratio_cruise = v_cruise / v_tip_cruise
    inflow_ratio_climb = v_climb / v_tip_climb

    #induced power all segments
    induced_power_cruise = (gtow / v_cruise) * ((2 * gtow * total_lift_cruise) / rho) * (1 / (math.pi * aspect_ratio * e))
    induced_power_climb = (gtow / v_climb) * ((2 * gtow * total_lift_climb) / rho) * (1 / (math.pi * aspect_ratio * e))+((1.15*(ct**2))/(2*inflow_ratio_climb))
    induced_power_hover = (gtow / v_downwash) * ((2 * gtow * total_lift_hover) / rho) * (1 / (math.pi * aspect_ratio * e))+((1.15*(ct**2))/(2*inflow_ratio_hover))

    #drag power all segments
    drag_power_cruise = 0.5 * rho * (v_cruise ** 3) * (drag_area + wing_area * cd_profile)
    drag_power_climb = 0.5 * rho * (v_climb ** 3) * (drag_area + wing_area * cd_profile)
    drag_power_hover = 0.5 * rho * (v_downwash ** 3) * (drag_area + wing_area * cd_profile)

    
    fp_hover = math.sqrt(1 + inflow_ratio_hover) * (1 + (5 / 2) * inflow_ratio_hover ** 2) + \
               (3 / 2) * (inflow_ratio_hover ** 4) * math.log(1 + math.sqrt(1 + inflow_ratio_hover ** 2) / inflow_ratio_hover)
    fp_cruise = math.sqrt(1 + inflow_ratio_cruise) * (1 + (5 / 2) * inflow_ratio_cruise ** 2) + \
                (3 / 2) * (inflow_ratio_cruise ** 4) * math.log(1 + math.sqrt(1 + inflow_ratio_cruise ** 2) / inflow_ratio_cruise)
    fp_climb = math.sqrt(1 + inflow_ratio_climb) * (1 + (5 / 2) * inflow_ratio_climb ** 2) + \
               (3 / 2) * (inflow_ratio_climb ** 4) * math.log(1 + math.sqrt(1 + inflow_ratio_climb ** 2) / inflow_ratio_climb)

    profile_power_hover = (1 / 8) * solidity * cd_profile * fp_hover * rho * swept_area * v_tip_hover ** 2
    profile_power_cruise = (1 / 8) * solidity * cd_profile * fp_cruise * rho * swept_area * v_tip_cruise ** 2 
    profile_power_climb = (1 / 8) * solidity * cd_profile * fp_climb * rho * swept_area * v_tip_climb ** 2

    
    total_power = (
        induced_power_cruise + induced_power_climb + induced_power_hover +
        drag_power_cruise + drag_power_climb + drag_power_hover +
        profile_power_cruise + profile_power_climb + profile_power_hover
    )

    rpm_hover = (60 / (2 * math.pi)) * (v_tip_hover / radius) #velocities

    reynolds_number = (v_cruise * mean_chord_length) / (1.55e-5) #constants

    return { #rotor parameters
        "radius (m)": round(radius, 3),
        "swept_area (m²)": round(swept_area, 3),
        "mean_chord_length (m)": round(mean_chord_length, 3),
        "thrust_per_rotor (N)": round(thrust_per_rotor, 3),
        "thrust_available (N)": round(thrust_available, 3),
        #velocities
        "v_stall (m/s)": round(v_stall, 3),
        "v_climb (m/s)": round(v_climb, 3),
        "v_cruise (m/s)": round(v_cruise, 3),
        "v_downwash (m/s)": round(v_downwash, 3),
        "rpm_hover (RPM)": round(rpm_hover, 1),

        #lift and drag for climb
        "lift_climb (N)": round(total_lift_climb, 3),
        "drag_climb (N)": round(total_drag_climb, 3),

        #lift and drag for hover
        "lift_hover (N)": round(total_lift_hover, 3),
        "drag_hover (N)": round(total_drag_hover, 3),

         #lift and drag for cruise
        "lift_cruise (N)": round(total_lift_cruise, 3),
        "drag_cruise (N)": round(total_drag_cruise, 3),


        #induced power
        "induced_power_cruise (W)": round(induced_power_cruise, 3),
        "induced_power_climb (W)": round(induced_power_climb, 3),
        "induced_power_hover (W)": round(induced_power_hover, 3),

        #drag power
        "drag_power_cruise (W)": round(drag_power_cruise, 3),
        "drag_power_climb (W)": round(drag_power_climb, 3),
        "drag_power_hover (W)": round(drag_power_hover, 3),

        #constants
        "reynolds_number": round(reynolds_number, 0),
        "inflow_ratio_hover": round(inflow_ratio_hover, 4),
        "inflow_ratio_cruise": round(inflow_ratio_cruise, 4),
        "inflow_ratio_climb": round(inflow_ratio_climb, 4),

        # Profile power
        "profile_power_hover (W)": round(profile_power_hover, 3),
        "profile_power_cruise (W)": round(profile_power_cruise, 3),
        "profile_power_climb (W)": round(profile_power_climb, 3),

        # Total power
        "total_power (W)": round(total_power, 3),
    }

def calculate_lift_plus_cruise(data):
    #Inputs
    no_of_rotor = int(data['no_of_rotor'])
    no_of_blade = int(data['no_of_blade'])
    gtow = float(data['gtow'])
    disk_loading = float(data['disk loading'])
    solidity = float(data['solidity'])
    cl = float(data['cl'])
    cd = float(data['cd'])
    cd_profile = float(data['cd_profile'])
    ct = float(data['ct'])
    rate_of_climb = float(data['rate_of_climb'])
    delta_cl = float(data['delta_cl'])
    wing_loading = float(data['wing_loading'])
    aspect_ratio = float(data['aspect_ratio'])
    rho = float(data['rho'])
    cd_induced = float(data['cd_induced'])
    np= float(data['propellor efficiency'])
    nh = float(data['hover efficiency'])
    v_tip_climb= float(data['v_tip_climb'])
    v_tip_cruise= float(data['v_tip_cruise'])


    radius = math.sqrt(gtow / (disk_loading * math.pi * no_of_rotor))
    swept_area = math.pi * radius ** 2
    mean_chord_length = (solidity * math.pi * radius) / no_of_blade
    thrust_per_rotor = gtow / no_of_rotor 
    thrust_available = no_of_rotor * swept_area * 9.81 * disk_loading
    drag_area = (2 * 9.81 * gtow / 2500) ** 0.67 

    wing_area = gtow / wing_loading
    wing_span = math.sqrt(wing_area * aspect_ratio)

    v_stall = math.sqrt((2 * wing_loading * 9.81) / (rho * (cl + delta_cl)))
    v_climb = 1.2 * v_stall
    v_cruise = 1.3 * v_stall
    v_downwash = 0.5 * math.sqrt(rate_of_climb ** 2 + ((2 * gtow*9.81) / (rho * swept_area))) - rate_of_climb

    lift_rotor_cruise = 0.5 * rho * cl * v_cruise ** 2
    lift_wing_cruise = 0.5 * rho * cl * wing_area * v_cruise ** 2
    total_lift_cruise = lift_rotor_cruise + lift_wing_cruise

    drag_rotor_cruise = 0.5 * rho * v_cruise ** 2 * cd
    drag_wing_cruise = 0.5 * rho * cd * wing_area * v_cruise ** 2
    total_drag_cruise = drag_rotor_cruise + drag_wing_cruise

    lift_rotor_hover = 0.5 * rho * cl * v_downwash ** 2
    lift_wing_hover = 0.5 * rho * cl * wing_area * v_downwash ** 2
    total_lift_hover = lift_rotor_hover + lift_wing_hover

    drag_rotor_hover = 0.5 * rho * v_downwash ** 2 * cd
    drag_wing_hover = 0.5 * rho * cd * wing_area * v_downwash ** 2
    total_drag_hover = drag_rotor_hover + drag_wing_hover

    lift_rotor_climb = 0.5 * rho * cl * v_climb ** 2
    lift_wing_climb = 0.5 * rho * cl * wing_area * v_climb ** 2
    total_lift_climb = lift_rotor_climb + lift_wing_climb

    drag_rotor_climb = 0.5 * rho * v_climb ** 2 * cd * swept_area
    drag_wing_climb = 0.5 * rho * cd * wing_area * v_climb ** 2
    total_drag_climb = drag_rotor_climb + drag_wing_climb

    e = (cl ** 2) / (math.pi * aspect_ratio * cd_induced)

    inflow_ratio_hover = math.sqrt(ct / 2)
    inflow_ratio_cruise = v_cruise / v_tip_cruise
    inflow_ratio_climb = v_climb / v_tip_climb

    
    advance_ratio_hover = math.pi*math.sqrt(ct / 2)
    advance_ratio_cruise =  math.pi*(v_cruise / v_tip_cruise)
    advance_ratio_climb =  math.pi*(v_climb / v_tip_climb)



    v_tip_hover= v_downwash/inflow_ratio_hover

    fp_hover = math.sqrt(1 + inflow_ratio_hover) * (1 + (5 / 2) * inflow_ratio_hover ** 2) + \
               (3 / 2) * (inflow_ratio_hover ** 4) * math.log(1 + math.sqrt(1 + inflow_ratio_hover ** 2) / inflow_ratio_hover)
    fp_cruise = math.sqrt(1 + inflow_ratio_cruise) * (1 + (5 / 2) * inflow_ratio_cruise ** 2) + \
                (3 / 2) * (inflow_ratio_cruise ** 4) * math.log(1 + math.sqrt(1 + inflow_ratio_cruise ** 2) / inflow_ratio_cruise)
    fp_climb = math.sqrt(1 + inflow_ratio_climb) * (1 + (5 / 2) * inflow_ratio_climb ** 2) + \
               (3 / 2) * (inflow_ratio_climb ** 4) * math.log(1 + math.sqrt(1 + inflow_ratio_climb ** 2) / inflow_ratio_climb)

    induced_power_cruise = (gtow / v_cruise) * ((2 * total_lift_cruise) / rho) * \
                           (1 / (math.pi * aspect_ratio * e)) * (1 / np)
    induced_power_climb = ((gtow / v_climb) * ((2 * total_lift_climb) / rho) * \
                          (1 / (math.pi * aspect_ratio * e)) +((1.15*(ct**2))/(2*inflow_ratio_climb))) * (1 / np)
    induced_power_hover = ((gtow / v_downwash) * ((2 * total_lift_hover) / rho) * \
                          (1 / (math.pi * aspect_ratio * e))+((1.15*(ct**2))/(2*inflow_ratio_hover)) )* (1 / nh)

    drag_power_cruise = 0.5 * rho * (v_cruise ** 3) * (drag_area + wing_area * cd_profile) * (1 / np)
    drag_power_climb = 0.5 * rho * (v_climb ** 3) * (drag_area + wing_area * cd_profile) * (1 / np)
    drag_power_hover = 0.5 * rho * (v_downwash ** 3) * (drag_area + wing_area * cd_profile) * (1 / nh)

    profile_power_hover = (1 / 8) * solidity * cd_profile * fp_hover * rho * swept_area * v_tip_hover ** 2 * (1 / nh)
    profile_power_cruise = (1 / 8) * solidity * cd_profile * fp_cruise * rho * swept_area * v_tip_cruise ** 2 * (1 / np)
    profile_power_climb = (1 / 8) * solidity * cd_profile * fp_climb * rho * swept_area * v_tip_climb ** 2 * (1 / np)

    reynolds_number = (v_cruise * mean_chord_length) / (1.55e-5)

    total_power = (
        induced_power_cruise + induced_power_climb + induced_power_hover +
        drag_power_cruise + drag_power_climb + drag_power_hover +
        profile_power_cruise + profile_power_climb + profile_power_hover
    )

    return {
    "gtow (kg)": gtow,
    "no_of_rotor": no_of_rotor,
    "no_of_blade": no_of_blade,
    "radius (m)": round(radius, 3),
    "swept_area (m^2)": round(swept_area, 2),
    "mean_chord_length (m)": round(mean_chord_length, 3),
    "thrust_per_rotor (N)": round(thrust_per_rotor, 2),
    "thrust_available (N)": round(thrust_available, 2),
    "drag_area (m^2)": round(drag_area, 3),

    "wing_area (m^2)": round(wing_area, 2),
    "wing_span (m)": round(wing_span, 2),

    "v_stall (m/s)": round(v_stall, 2),
    "v_climb (m/s)": round(v_climb, 2),
    "v_cruise (m/s)": round(v_cruise, 2),
    "v_downwash (m/s)": round(v_downwash, 2),

    "v_tip_hover (m/s)": round(v_tip_hover, 2),
    "v_tip_cruise (m/s)": round(v_tip_cruise, 2),
    "v_tip_climb (m/s)": round(v_tip_climb, 2),

    "lift_cruise (N)": round(total_lift_cruise, 2),
    "lift_hover (N)": round(total_lift_hover, 2),
    "lift_climb (N)": round(total_lift_climb, 2),

    "drag_cruise (N)": round(total_drag_cruise, 2),
    "drag_hover (N)": round(total_drag_hover, 2),
    "drag_climb (N)": round(total_drag_climb, 2),

    "induced_power_cruise (W)": round(induced_power_cruise, 2),
    "induced_power_climb (W)": round(induced_power_climb, 2),
    "induced_power_hover (W)": round(induced_power_hover, 2),

    "drag_power_cruise (W)": round(drag_power_cruise, 2),
    "drag_power_climb (W)": round(drag_power_climb, 2),
    "drag_power_hover (W)": round(drag_power_hover, 2),

    "profile_power_cruise (W)": round(profile_power_cruise, 2),
    "profile_power_climb (W)": round(profile_power_climb, 2),
    "profile_power_hover (W)": round(profile_power_hover, 2),

    "inflow_ratio_hover": round(inflow_ratio_hover, 3),
    "inflow_ratio_cruise": round(inflow_ratio_cruise, 3),
    "inflow_ratio_climb": round(inflow_ratio_climb, 3),

    "advance_ratio_hover": round(advance_ratio_hover, 3),
    "advance_ratio_cruise": round(advance_ratio_cruise, 3),
    "advance_ratio_climb": round(advance_ratio_climb, 3),

    "e": round(e, 3),
    "solidity ": round(solidity, 3),
    "aspect_ratio": round(aspect_ratio, 2),
    "reynolds_number": round(reynolds_number, 2),
    "total_power (W)": round(total_power, 2),
}


def calculate_smr(data):
    # Inputs
    gtow = float(data['gtow'])             
    bl = float(data['bl'])                 
    cl_max = float(data['cl_max'])        
    cl = float(data['cl'])                
    no_of_blade = int(data['no_of_blade']) 
    rho = float(data['rho'])               
    ct = float(data['ct'])      
    cd = float(data['cd'])           
    solidity = float(data['solidity'])    
    cd_profile = float(data['cd_profile'])
    rate_of_climb= float(data['rate_of_climb'])

    # Tip Speeds (user inputs)
     
    v_tip_cruise = float(data['v_tip_cruise'])    
    v_tip_climb = float(data['v_tip_climb'])      

    # Constants
    g = 9.81
    thrust = gtow * g
    radius = math.sqrt(thrust / (math.pi * bl))
    area = math.pi * radius ** 2
    mean_chord_length = (solidity * math.pi * radius) / no_of_blade

    # Velocities
    v_stall = math.sqrt((2 * bl * g) / (rho * cl_max))
    v_cruise = 1.3*v_stall
    v_climb = 1.2*v_stall
    v_downwash = 0.5 * math.sqrt(rate_of_climb ** 2 + ((2 * gtow) / (rho * area))) - rate_of_climb

    #lift and drag
    lift_hover= (1/2)*rho*cl*(v_downwash**2)
    lift_cruise= (1/2)*rho*cl*(v_cruise**2)
    lift_climb= (1/2)*rho*cl*(v_climb**2)

    drag_hover= (1/2)*rho*cd*(v_downwash**2)
    drag_cruise= (1/2)*rho*cd*(v_cruise**2)
    drag_climb= (1/2)*rho*cd*(v_climb**2)

    # Angular Speeds & RPMs
    v_tip_hover = math.sqrt(ct/2)   
    omega_hover = v_tip_hover / radius
    omega_cruise = v_tip_cruise / radius
    omega_climb = v_tip_climb / radius

    rpm_hover = (60 / (2 * math.pi)) * omega_hover
    rpm_cruise = (60 / (2 * math.pi)) * omega_cruise
    rpm_climb = (60 / (2 * math.pi)) * omega_climb

    # Drag Area & Fuselage Drag
    drag_area = 4.2 * ((2.205 * gtow) / 1000) ** 0.67
    fuselage_drag_hover = 0.5 * rho * v_downwash ** 2 * drag_area
    fuselage_drag_cruise = 0.5 * rho * v_cruise ** 2 * drag_area
    fuselage_drag_climb = 0.5 * rho * v_climb ** 2 * drag_area

    # Shaft Tilt Angles
    shaft_tilt_angle_hover = math.atan(fuselage_drag_hover / thrust)
    shaft_tilt_angle_cruise = math.atan(fuselage_drag_cruise / thrust)
    shaft_tilt_angle_climb = math.atan(fuselage_drag_climb / thrust)

    # Advance Ratios
    advance_ratio_hover = (v_downwash * math.cos(shaft_tilt_angle_hover)) / (radius * omega_hover)
    advance_ratio_cruise = (v_cruise * math.cos(shaft_tilt_angle_cruise)) / (radius * omega_cruise)
    advance_ratio_climb = (v_climb * math.cos(shaft_tilt_angle_climb)) / (radius * omega_climb)

    # Inflow Ratios
    inflow_ratio_hover = ((v_downwash * math.sin(shaft_tilt_angle_hover)) / (omega_hover * radius)) + (ct / (2 * advance_ratio_hover))
    inflow_ratio_cruise = ((v_cruise * math.sin(shaft_tilt_angle_cruise)) / (omega_cruise * radius)) + (ct / (2 * advance_ratio_cruise))
    inflow_ratio_climb = ((v_climb * math.sin(shaft_tilt_angle_climb)) / (omega_climb * radius)) + (ct / (2 * advance_ratio_climb))

    # Reynolds Number
    reynolds_number = (v_cruise * mean_chord_length) / (1.55e-5)

    # Powers
    induced_power_hover = 1.15 * ((ct ** 2) / (2 * math.sqrt(inflow_ratio_hover ** 2 + advance_ratio_hover ** 2))) * rho * area * v_downwash ** 3
    induced_power_cruise = 1.15 * ((ct ** 2) / (2 * math.sqrt(inflow_ratio_cruise ** 2 + advance_ratio_cruise ** 2))) * rho * area * v_cruise ** 3
    induced_power_climb = 1.15 * ((ct ** 2) / (2 * math.sqrt(inflow_ratio_climb ** 2 + advance_ratio_climb ** 2))) * rho * area * v_climb ** 3
    total_induced_power = induced_power_hover + induced_power_cruise + induced_power_climb

    profile_power_hover = (1/8) * solidity * cd_profile * (1 + 4.65 * advance_ratio_hover ** 2) * rho * area * v_downwash ** 3
    profile_power_cruise = (1/8) * solidity * cd_profile * (1 + 4.65 * advance_ratio_cruise ** 2) * rho * area * v_cruise ** 3
    profile_power_climb = (1/8) * solidity * cd_profile * (1 + 4.65 * advance_ratio_climb ** 2) * rho * area * v_climb ** 3
    total_profile_power = profile_power_hover + profile_power_cruise + profile_power_climb

    drag_power_hover = 0.5 * advance_ratio_hover ** 3 * (drag_area / area) * rho * area * v_downwash ** 3
    drag_power_cruise = 0.5 * advance_ratio_cruise ** 3 * (drag_area / area) * rho * area * v_cruise ** 3
    drag_power_climb = 0.5 * advance_ratio_climb ** 3 * (drag_area / area) * rho * area * v_climb ** 3
    total_drag_power = drag_power_hover + drag_power_cruise + drag_power_climb

    total_hover_power = induced_power_hover + profile_power_hover + drag_power_hover
    total_cruise_power = induced_power_cruise + profile_power_cruise + drag_power_cruise
    total_climb_power = induced_power_climb + profile_power_climb + drag_power_climb
    total_power = total_hover_power + total_cruise_power + total_climb_power

    return {
        # Rotor geometry
        "thrust (N)": round(thrust, 2),
        "radius (m)": round(radius, 3),
        "area (m^2)": round(area, 3),
        "mean_chord_length (m)": round(mean_chord_length, 3),

        # Velocities
        "v_stall (m/s)": round(v_stall, 2),
        "v_cruise (m/s)": round(v_cruise, 2),
        "v_climb (m/s)": round(v_climb, 2),
        "v_downwash (m/s)": round(v_downwash, 2),

        # Tip Speeds (input)
        "v_tip_hover (m/s)": round(v_tip_hover, 2),
        "v_tip_cruise (m/s)": round(v_tip_cruise, 2),
        "v_tip_climb (m/s)": round(v_tip_climb, 2),

        # RPMs
        "rpm_hover": round(rpm_hover, 2),
        "rpm_cruise": round(rpm_cruise, 2),
        "rpm_climb": round(rpm_climb, 2),

        # Omegas
        "angular_velocity_hover (rad/s)": round(omega_hover, 3),
        "angular_velocity_cruise (rad/s)": round(omega_cruise, 3),
        "angular_velocity_climb (rad/s)": round(omega_climb, 3),

        # Inflow Ratios
        "inflow_ratio_hover": round(inflow_ratio_hover, 4),
        "inflow_ratio_cruise": round(inflow_ratio_cruise, 4),
        "inflow_ratio_climb": round(inflow_ratio_climb, 4),

        # Advance Ratios
        "advance_ratio_hover": round(advance_ratio_hover, 4),
        "advance_ratio_cruise": round(advance_ratio_cruise, 4),
        "advance_ratio_climb": round(advance_ratio_climb, 4),

        # Reynolds
        "reynolds_number": round(reynolds_number),

        # Drag Area
        "drag_area (m^2)": round(drag_area, 3),

        # Powers
        "induced_power_hover (W)": round(induced_power_hover, 2),
        "induced_power_cruise (W)": round(induced_power_cruise, 2),
        "induced_power_climb (W)": round(induced_power_climb, 2),

        "profile_power_hover (W)": round(profile_power_hover, 2),
        "profile_power_cruise (W)": round(profile_power_cruise, 2),
        "profile_power_climb (W)": round(profile_power_climb, 2),

        "drag_power_hover (W)": round(drag_power_hover, 2),
        "drag_power_cruise (W)": round(drag_power_cruise, 2),
        "drag_power_climb (W)": round(drag_power_climb, 2),

        "total_induced_power (W)": round(total_induced_power, 2),
        "total_profile_power (W)": round(total_profile_power, 2),
        "total_drag_power (W)": round(total_drag_power, 2),

        "total_hover_power (W)": round(total_hover_power, 2),
        "total_cruise_power (W)": round(total_cruise_power, 2),
        "total_climb_power (W)": round(total_climb_power, 2),
        "total_power (W)": round(total_power, 2)
    }

