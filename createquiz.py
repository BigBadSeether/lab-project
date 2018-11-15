import mysql.connector
from random import shuffle

def create_quiz(quiz_content):
	chapters = quiz_content[0]
	num_questions = quiz_content[1]

	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="password",
	  database = 'LabProject'
	)

	mycursor = mydb.cursor()

	#Query the database and make lists of all the questions and answers
	chapter_answers = []
	chapter_count = 0
	num_incorrect = 0
	total_questions = 0
	for chapter in chapters:
		sql = "SELECT * FROM Questions WHERE Questions.chapter = " + str(chapter)
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		
		count = 0
		questions = []
		inc_answers = []
		cor_answers = []
		for row in myresult:
			if count >= num_questions[0]:
				break
			else:
				count += 1
				questions.append(row[1])
				inc_answers.append(row[2])
				cor_answers.append(row[3])

		count = 0
		question_answers = []
		for inc_answer in inc_answers:
			question_answers.append(inc_answer.replace("\n", "").split("/"))
			question_answers[count].append(cor_answers[count])
			shuffle(question_answers[count])
			count += 1
		
		chapter_answers.append(question_answers)

		#Printing out the question and answer and accepting user input
		question_count = 0

		for question in questions:
			print ("\n" + question + ": \n")
			answer_count = 0

			for answer in chapter_answers[chapter_count][question_count]:
				print (str(answer_count +1) + ". " + answer)
				answer_count += 1

			user_answer = int(input("\n Select your answer: ")) - 1
			if (chapter_answers[chapter_count][question_count][user_answer] != cor_answers[question_count]):
				num_incorrect += 1
			
			question_count += 1
			total_questions += 1

		chapter_count += 1	

	num_correct = total_questions - num_incorrect
	print("\n\n Percentage: " + str((float(num_correct) / float(total_questions)) * 100))