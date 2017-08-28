import string

# 1. read file and process file(split, lower case)
def read_file(file_name, test_file_flg):
	file_word_list = []
	f_test = open(file_name, "r")
	for line in f_test.readlines():
		if test_file_flg:
			split_words_list = [w for w in line.lower().strip('\n').split(" ")]
		else:
			split_words_list = [w for w in line.lower().strip('\n').split(",")]
		split_words_list = ["".join(l for l in w if l not in string.punctuation) for w in split_words_list]
		file_word_list.append(split_words_list)
	f_test.close()
	return file_word_list

# 2. read raw testing file
def read_raw_file(file_name):
	test_word_list = []
	f_test = open(file_name, "r")
	for line in f_test.readlines():
		test_word_list.append(line.strip("\n"))
	f_test.close()
	return test_word_list


# 3. replace antonym
def replace_antonym(ant_file_name, test_file_filename):
	test_word_list = read_raw_file(test_file_filename)
	antonym_word_list = read_file(ant_file_name, False)

	output_string = ""
	for line in test_word_list:
		replaced_result = line.lower()
		for replace_word in antonym_word_list:
			replaced_result = replaced_result.replace(replace_word[0], replace_word[1])
		print(replaced_result)
		output_string += replaced_result + "\n"

	return output_string

