import mysql.connector
from createquiz import create_quiz

def search_old_quizzes():

	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="password",
	  database = 'LabProject'
	)

	mycursor = mydb.cursor()

	sql = "SELECT * FROM OldQuizzes"

	mycursor.execute(sql)

	myresult = mycursor.fetchall()

	if myresult != None:
		print("Old Quizzes: \n")

		quizzes_count = 1
		total_quizzes = []
		for row in myresult:
			print("\nQuiz " + str(quizzes_count) + "\n")
			quizzes_count += 1

			chapters = row[1].replace(" ", "").split(",")
			num_questions = row[2]

			# Making a list with elements that contain the chapters and number of questions per quiz
			list = [chapters, num_questions]
			total_quizzes.append(list)

			for index in range(len(chapters)):
				print("Chapter: " + chapters[index])
			print("\n" + num_questions[0] + " questions per chapter")

		user_choice = int(input("\nWhich quiz would you like to retake? (ex: '1')"))
		user_quiz = total_quizzes[user_choice-1]
		return user_quiz

	else:
		print("No old quizzes found\n")
		return


def main():
	quiz = search_old_quizzes()
	create_quiz(quiz)


if __name__ == '__main__':
    main()