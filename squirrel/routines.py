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

def rune_frequency(runes):
	freqs = {
		"ᚠ": 0, 
		"ᚢ": 0,
		"ᚦ": 0,
		"ᚩ": 0,
		"ᚱ": 0,
		"ᚳ": 0,
		"ᚷ": 0,
		"ᚹ": 0,
		"ᚻ": 0,
		"ᚾ": 0,
		"ᛁ": 0,
		"ᛂ": 0,
		"ᛇ": 0,
		"ᛈ": 0,
		"ᛉ": 0,
		"ᛋ": 0,
		"ᛏ": 0,
		"ᛒ": 0,
		"ᛖ": 0,
		"ᛗ": 0,
		"ᛚ": 0,
		"ᛝ": 0,
		"ᛟ": 0,
		"ᛞ": 0,
		"ᚪ": 0,
		"ᚫ": 0,
		"ᚣ": 0,
		"ᛡ": 0,
		"ᛠ": 0
	}
	for rune in runes:
		if rune in freqs:
			freqs[rune] += 1
	return freqs