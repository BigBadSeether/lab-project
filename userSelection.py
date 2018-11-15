import mysql.connector
from random import shuffle


def main():
    print("Welcome! Please choose an option.")
    while True:
        print("\n1.) Create new quiz\n2.) Take an existing quiz")
        try:
            i = int(input("Choose an option (Ex: 1): "))
            if i < 1 or i > 2:
                print("Please choose one of the options available.")
                continue
            break
        except ValueError:
            print("Please input an integer for the response.")
    if i == 1:
        new_quiz = create_quiz()
        save_quiz(new_quiz)
    if i == 2:
        quiz = choose_quiz()
        take_quiz(quiz)


def create_quiz():
    allowed_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',']
    chapters = []
    while True:
        check = True
        i = str(input("What chapters would you like? (Input integers from 1-10 divided by commas; Ex: 1,3,5): "))
        for char in i:
            try:
                b = int(allowed_chars.index(char))
            except ValueError:
                print("Please only use numbers from 1-9 and commas in your response.")
                check = False
        if check:
            chapters = i.split(',')
            for chapter in chapters:
                if int(chapter) < 1 or int(chapter) > 10:
                    print("Please only use integers from 1-10.")
                    check = False
        if not check:
            continue
        break
    while True:
        try:
            num = int(input("How many questions would you like per chapter? Please input a single integer greater than"
                            " 0:"))
        except ValueError:
            print("Please input an integer.")
            continue
        if num < 1:
            print("Please input an integer that is greater than 0.")
            continue
        break
    return [chapters, num]


def save_quiz(quiz_content):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="labproject"
    )

    chapters = ""
    chapter_count = 0
    for chapter in quiz_content[0]:
        chapters += chapter
        if not chapter_count + 1 == quiz_content[0].__sizeof__():
            chapters += ','


    sql = "INSERT INTO oldquizzes (chapters,questions) VALUES ('" + chapters + "','" + quiz_content[1] + "')"




def choose_quiz():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database='labproject'
    )

    mycursor = mydb.cursor()

    sql = "SELECT * FROM oldquizzes"

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
        user_quiz = total_quizzes[user_choice - 1]
        return user_quiz

    else:
        print("No old quizzes found\n")
        return


def take_quiz(quiz_content):
    chapters = quiz_content[0]
    num_questions = quiz_content[1]

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database='labproject'
    )

    mycursor = mydb.cursor()

    # Query the database and make lists of all the questions and answers
    chapter_answers = []
    chapter_count = 0
    num_incorrect = 0
    total_questions = 0
    for chapter in chapters:
        sql = "SELECT * FROM questions WHERE questions.chapter = " + str(chapter)
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

        # Printing out the question and answer and accepting user input
        question_count = 0

        for question in questions:
            print("\n" + question + ": \n")
            answer_count = 0

            for answer in chapter_answers[chapter_count][question_count]:
                print(str(answer_count + 1) + ". " + answer)
                answer_count += 1

            user_answer = int(input("\n Select your answer: ")) - 1
            if (chapter_answers[chapter_count][question_count][user_answer] != cor_answers[question_count]):
                num_incorrect += 1

            question_count += 1
            total_questions += 1

        chapter_count += 1

    num_correct = total_questions - num_incorrect
    print("\n\n Percentage: " + str((float(num_correct) / float(total_questions)) * 100))


main()
