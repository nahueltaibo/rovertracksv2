# Maps a value from a range to another range
def mapBetweenRanges(v, in_min, in_max, out_min, out_max):
    # Check that the value is at least in_min
    # if v < in_min:
    # 	v = in_min
    # # Check that the value is at most in_max
    # if v > in_max:
    # 	v = in_max
    return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min