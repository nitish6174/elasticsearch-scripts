def formatCode(style="normal",color="white"):
	style_map = {
		"normal" : 0,
		"bold" : 1,
		"dim" : 2,
		"italic" : 3,
		"underline" : 4
	}
	color_map = {
		"black" : 30,
		"red" : 31,
		"green" : 32,
		"yellow" : 33,
		"blue" : 34,
		"purple" : 35,
		"cyan" : 36,
		"white" : 37,
	}
	x = "\033[0m"
	code = "\033[" + str(style_map[style]) + ";" + str(color_map[color]) + "m"
	return code


def cprint(text,color="white",style=["normal"],end="\n"):
	formatted_text = []
	for x in style:
		formatted_text.append(formatCode(x,color))
	formatted_text.append(text)
	formatted_text.append(formatCode())
	print("".join(formatted_text),end=end)