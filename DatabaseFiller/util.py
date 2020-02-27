def does_exist_in_dict(my_key, my_dict):
    if my_key in my_dict:
        return my_dict[my_key]
    else:
        return "NONE"