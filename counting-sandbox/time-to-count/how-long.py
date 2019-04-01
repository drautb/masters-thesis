instructions_per_second = 4000000000
seconds_per_hour = 60 * 60
hours_per_day = 24
days_per_year = 365

total = pow(2, 122)

hours = (total / instructions_per_second) / seconds_per_hour
print("{} hours to count to {}".format(hours, total))

days = hours / hours_per_day
print("{} days to count to {}".format(days, total))

years = days / days_per_year
print("{} years to count to {}".format(years, total))

millenia = years / 1000
print("{} millenia to count to {}".format(millenia, total))