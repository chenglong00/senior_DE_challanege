ACCEPTABLE_FILE_TYPES = ["csv", "txt"]
DATETIME_FORMAT = "%Y-%m-%d"
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9._%+-]+.(?:com|net)\b'

# Common Patterns
# D-M-Y
# M/D/Y
# Y/M/D

DATE_PATTERN_DASH_Y_M_D = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])'  # dash %Y-%m-%d
DATE_PATTERN_DASH_Y_D_M = r'\d{4}-(0[1-9]|1[0-9]|2[0-9]|3[0-1])-(0[1-9]|1[0-2])'  # dash %Y-%d-%m

DATE_PATTERN_DASH_D_M_Y = r'(0[1-9]|1[0-9]|2[0-9]|3[0-1])-(0[1-9]|1[0-2])-\d{4}'  # dash %d-%m-%Y
DATE_PATTERN_DASH_M_D_Y = r'(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])-\d{4}'  # dash %m-%d-%Y

DATE_PATTERN_SLASH_M_D_Y = r'(0[1-9]|1[0-2])/(0[1-9]|1[0-9]|2[0-9]|3[0-1])/\d{4}'  # slash %m/%d/%Y
DATE_PATTERN_SLASH_D_M_Y = r'(0[1-9]|1[0-9]|2[0-9]|3[0-1])/(0[1-9]|1[0-2])/\d{4}}'  # slash %d/%m/%Y

DATE_PATTERN_SLASH_Y_M_D = r'\d{4}/(0[1-9]|1[0-2])/(0[1-9]|1[0-9]|2[0-9]|3[0-1])'  # slash %Y/%m/%d
DATE_PATTERN_SLASH_Y_D_M = r'\d{4}/(0[1-9]|1[0-9]|2[0-9]|3[0-1])/(0[1-9]|1[0-2])'  # slash %Y/%d/%m

