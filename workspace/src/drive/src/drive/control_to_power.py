def clamp(val, smallest, largest):
    return max(smallest, min(val, largest))

# tank drive left and right go in opposite directions to forward
# when they go in same direction we turn
# left ->   100 = left full forward
# left ->  -100 = left full reverse
# right ->  100 = right full reverse
# right -> -100 = right full forward
def control_to_power(linear, angular):
    angular = clamp(angular, -100, 100)
    linear = clamp(linear, -100, 100)

    # angular 100 -> 100 right, -100 left (max left)
    # thus angular translates 1:1 to right and -angular for left
    right = angular
    left = angular

    # track remaining power
    right_remaining = 100 - abs(angular)
    left_remaining = 100 - abs(angular)

    linear_power = min([right_remaining, left_remaining, abs(linear)])

    # if there is remaing power, we can put the max
    if linear_power > 0:
        if linear > 0:
            right -= linear_power
            left += linear_power
        else:
            right += linear_power
            left -= linear_power

    return [left, right]