def _merge_dicts(user_dict, **system_dict):
	if user_dict is None:
		return system_dict
	for key in system_dict:
		system_value = system_dict[key]
		if key in user_dict:
			user_value = user_dict[key]
			if isinstance(user_value, dict) and isinstance(system_value, dict):
				user_value.update(system_value)
			elif user_value == system_value:
				pass
			else:
				raise ValueError("Key {} has differing values {} and {}".format(key, user_value, system_value))
		else:
			user_dict[key] = system_value
	return user_dict
