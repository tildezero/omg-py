def no_id(d: dict) -> dict:
	dict_copy = d.copy()
	dict_copy.pop("id")
	return dict_copy
