from data import table, inverse_table, gematria_values, gematria_to_rune

def rune_to_text(runes):
	result = ""
	for rune in runes:
		if rune in table:
			result += table[rune]
		else:
			result += rune
	return result

def text_to_rune(text):
	text = text.upper().replace("U", "V")
	result = ""
	i = 0
	while i < len(text):
		if text[i:i+3] in inverse_table:
			result += inverse_table[text[i:i+3]]
			i += 3
			continue
		elif text[i:i+2] in inverse_table:
			result += inverse_table[text[i:i+2]]
			i += 2
			continue
		elif text[i] in inverse_table:
			result += inverse_table[text[i]]
			i += 1
			continue
		result += text[i]
		i += 1
	return result

def rune_to_gematria(runes):
	result = []
	for rune in runes:
		if rune in gematria_values:
			result.append(gematria_values[rune])
	return result