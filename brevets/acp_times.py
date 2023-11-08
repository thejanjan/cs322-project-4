"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


def seconds(hour = 0, minute = 0, second = 0):
    """Returns the number of seconds given other time arguments."""
    return hour * 3600 + minute * 60 + second


# A dictionary mapping the control locations
# to their minimum and maximum speeds (km/hr).
control_spans_to_speed_ranges = {
    (0, 200):     (15, 34),
    (200, 400):   (15, 32),
    (400, 600):   (15, 30),
    (600, 1000):  (11.428, 28),
    (1000, 1300): (13.333, 26),
}


# A mapping between brevet distance to overall time limits
# (defined on https://rusa.org/pages/rulesForRiders).
brevet_time_limits = {
    200:  seconds(hour=13, minute=30),
    300:  seconds(hour=20),
    400:  seconds(hour=27),
    600:  seconds(hour=40),
    1000: seconds(hour=75),
}


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    assert brevet_dist_km in brevet_time_limits, "Invalid distance specified"
    assert control_dist_km <= brevet_dist_km, "Control distance exceeds brevet distance"

    # Iterate over each speed range.
    duration = 0
    for control_locations, control_speed_ranges in control_spans_to_speed_ranges.items():
        # Get constants for this location.
        control_start, control_end = control_locations
        speed = control_speed_ranges[1]

        # Is our control distance within bounds?
        if control_start < control_dist_km:
            # OK, then we add duration based on this control.
            control_end = min(control_end, control_dist_km)
            distance = control_end - control_start
            duration += round((distance / speed) * 60) * 60

    # Return arrow object.
    a = arrow.get(brevet_start_time)
    a = a.shift(seconds=duration)
    a.replace(tzinfo=brevet_start_time.tzinfo)
    return a


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    assert brevet_dist_km in brevet_time_limits, "Invalid distance specified"
    assert control_dist_km <= brevet_dist_km, "Control distance exceeds brevet distance"

    # For the opening control, we always allot 1 hour to close
    if control_dist_km == 0:
        duration = 3600

    # If we're closing at the end, use the overall brevet time limit
    elif control_dist_km == brevet_dist_km:
        duration = brevet_time_limits.get(brevet_dist_km)

    else:
        # Iterate over each speed range.
        duration = 0
        for control_locations, control_speed_ranges in control_spans_to_speed_ranges.items():
            # Get constants for this location.
            control_start, control_end = control_locations
            speed = control_speed_ranges[0]

            # Is our control distance within bounds?
            if control_start < control_dist_km:
                # OK, then we add duration based on this control.
                control_end = min(control_end, control_dist_km)
                distance = control_end - control_start
                duration += round((distance / speed) * 60) * 60

    # Return arrow object.
    a = arrow.get(brevet_start_time)
    a = a.shift(seconds=duration)
    a.replace(tzinfo=brevet_start_time.tzinfo)
    return a
