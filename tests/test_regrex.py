import re

# pattern = r'\b[A-Za-z0-9._%+-]+@emailprovider.(?:com|net)\b'
#
# # test the pattern on some strings
# strings = ['john.doe@emailproviders.com', 'jane_smith@emailprovider.net', 'abc@gmail.com', 'xyz@hotmail.com']
# for s in strings:
#     match = re.search(pattern, s)
#     if match:
#         print(f"{s}: {match.group(0)} is a valid email address")
#     else:
#         print(f"{s}: is not a valid email address")

# import re
# from datetime import datetime
#
# pattern = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])' #%Y-%m-%d
#
# # test the pattern on some strings
# strings = ['2022-01-01', '2022-12-31', '2022-00-15', '2022-13-20', '2022-12-32']
# for s in strings:
#     match = re.search(pattern, s)
#     if match:
#         print(f"{s}: valid date")
#     else:
#         print(f"{s}: Invalid date")

from common.utils import is_file_exist

print(is_file_exist(""))