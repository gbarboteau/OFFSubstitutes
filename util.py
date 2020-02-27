def is_integer(string_to_check):
	try:
		int(string_to_check)
		return True
	except ValueError:
		return False

def list_to_num_string(my_list):
    string_to_return = ""
    for i in range(1, len(my_list) +1):
        string_to_return = string_to_return + str(i) + ") " + my_list[i - 1] + "\n"
    return string_to_return