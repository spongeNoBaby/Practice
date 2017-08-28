import string
from collections import Counter

# 1. read file
def read_file(file_name, test_file_flg):
	file_word_list = []

	if '.' in file_name and file_name.rsplit('.', 1)[1] == "txt":
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


# 2. count all words
def get_count(text_list):
	count_list = []
	for line in text_list:
		count_list.append(Counter(line))
	return count_list

# 3. count synonym
def final_count_result(syn_file_name, ant_file_name, test_file_name):
	test_word_list = read_file(test_file_name, True)
	synonym_word_list = read_file(syn_file_name, False)
	antonym_word_list = read_file(ant_file_name, False)

	count_list = get_count(test_word_list)

	final_syn_result = [{} for j in range(len(test_word_list))]
	final_ant_result = [{} for j in range(len(test_word_list))]
	i = 0
	for line_count_dict in count_list:
		for syn_word_line in synonym_word_list:
			for syn_word in syn_word_line:
				if syn_word in line_count_dict.keys():
					final_syn_result[i][syn_word] = line_count_dict[syn_word]

		for ant_word_line in antonym_word_list:
			for ant_word in ant_word_line:
				if ant_word in line_count_dict.keys():
					final_ant_result[i][ant_word] = line_count_dict[ant_word]
		i += 1

	# Question A
	final_syn_file_count = {}
	final_syn_line_count = [{} for j in range(len(test_word_list))]
	for syn_word_line in synonym_word_list:
		sub_count = 0
		i = 0
		for item_line in final_syn_result:
			sub_line_count = 0
			for k, v in item_line.items():
				if k in syn_word_line:
					sub_count += v
					sub_line_count += v
				final_syn_line_count[i][syn_word_line[0]] = sub_line_count
			i += 1
		final_syn_file_count[syn_word_line[0]] = sub_count

	f_write = open('Q1_Synonym.txt', 'w')
	for syn_word_line in synonym_word_list:
		f_write.write("%s\n" % syn_word_line[0])
		for j in range(len(final_syn_line_count)):
			if syn_word_line[0] in final_syn_line_count[j].keys():
				f_write.write("Line %d : %d\n" % (j + 1, final_syn_line_count[j][syn_word_line[0]]))
		f_write.write("Total per file: %d\n\n" % final_syn_file_count[syn_word_line[0]])
	f_write.close()

	# Question B
	final_ant_file_count = {}
	for ant_word_line in antonym_word_list:
		for word in ant_word_line:
			final_ant_file_count[word] = 0
			for item_line in final_ant_result:
				if word in item_line.keys():
					final_ant_file_count[word] += item_line[word]

	f_write = open('Q1_Antonym.txt', 'w')
	for k, v in final_ant_file_count.items():
		if v > 0:
			f_write.write("%s\n" % k)
			for j in range(len(final_ant_result)):
				if k in final_ant_result[j].keys():
					f_write.write("Line %d : %d\n" % (j + 1, final_ant_result[j][k]))
			f_write.write("Total per file: %d\n\n" % final_ant_file_count[k])
	f_write.close()

	return

def read_output(file_name):
	output_string = ""

	# read and display the content of the output file
	f_output_read = open(file_name, "r")
	for line in f_output_read.readlines():
		output_string += line
		print(line.strip("\n"))
	f_output_read.close()

	return output_string

print('''
I'm refactoring Q1. Because there are some duplicate codes in it. Three files are read. Actually we can use one function
to read these files, set the file name as the parameter of the function. Besides, we want to read the output file. There
are totally two output files, which can also be read by a same function. After refactoring, we can invoke these functions
directly in Q7.
''')