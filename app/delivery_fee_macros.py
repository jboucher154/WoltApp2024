
# MAX FEE and FREE THRESHOLD #

MAXIMUM_DELIVERY_FEE = 1500
"""
Maximum fee for deliveries in cents.
1500 = 15€
"""

FREE_THRESHOLD = 20000
"""
Value of cart in cents to have no delivery fee applied to order.
A cart of equal or greater value will have no delivery fee.
20000 = 200€
"""

# ORDER SIZE AND RELATED FEES #
SMALL_ORDER_THRESHOLD = 1000
"""
Integer representing minimum price in cents to not be charged 
small order surcharge. Surcharge will be the cart value difference
from the threshold set.
1000 = 10€
"""

LARGE_ORDER_THRESHOLD = 4
"""
Number of items in cart to trigger prior to triggeringlarge order 
fee per item.
4 = charges will be applied begining on the next item after 4, i.e. item 5.
"""

LARGE_ORDER_ITEM_FEE = 50
"""
Fee in cents of per item surcharge for orders above the LARGE_ORDER_THRESHOLD
50 = 0.50€
"""

BULK_ORDER_THRESHOLD = 12
"""
Number of items in cart to trigger bulk order fee
"""

BULK_ORDER_FEE = 120
"""
Fee in cents of the one time bulk order fee
120 = 1.20€
"""

# DISTANCE FEES AND RELATED MEASUREMENTS #

BASE_DISTANCE_FEE = 200
"""
Integer of minimum charge in cents for delivery distance.
Covers intial delivery distance before addtional fees invoked
"""

ADDITIONAL_DISTANCE_FEE = 100
"""
Fee in cents for each addtional distance unit for delivery
100 = 1€
"""

BASE_DISTANCE = 1000
"""
Distance in meters covered by BASE_DISTANCE_FEE
"""

ADDITIONAL_DISTANCE_UNIT = 500
"""
Length in meters that will invoke additional delivery fee 
Important: If set to 0 no additional fees will be applied
"""

# RUSH HOUR SETTINGS #

RUSH_DAY = 4
"""
Day that rush hours occur on.
Given integer corresponding to datetime object mapping of days
    0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 
    4 = Friday, 5 = Saturday, 6 = Sunday
"""

RUSH_HOUR_BEGIN = 15
"""
Hour in 24-hr format that the rush hour rates begin. 
Must be > RUSH_HOUR_END.
if this == 15 then rush hours begin from 15:00 (3pm)
"""

RUSH_HOUR_END = 19
"""
Hour in 24-hr format that the rush hour rates end. 
Must be < RUSH_HOUR_END.
if this == 19 then rush hours end are not charged from 19:00 (7pm)
"""

RUSH_HOUR_MULTIPLIER = 1.2
"""
Rate to multiply the delivery fee total by to apply rate increase
"""
