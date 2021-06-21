"""
[Question.py]
@description: a class which helps with asking console questions.
"""


class Question:

    @staticmethod
    def ask(question):
        print(question)
        answer = input("Response: ")
        return answer

    @staticmethod
    def ask_bool_positive_safe(question):
        answer = input(question + " ")
        return (answer.lower() == "true") or \
               (answer.lower() == "t") or \
               (answer.lower() == "yes") or \
               (answer.lower() == "y") or \
               (answer == "1")

    @staticmethod
    def bool_negative_safe_question(question):
        answer = input(question + " ")
        return (answer.lower() == "false") or \
               (answer.lower() == "f") or \
               (answer.lower() == "no") or \
               (answer.lower() == "n") or \
               (answer == "0")

    @staticmethod
    def ask_type(question, ans_type, loop=True):
        """
        Used to ask and assert that the response to the question will be an integer
        :param question: what to ask
        :return: the result, of type specified
        """
        answer = Question.ask(question)

        if loop:
            # Loops until the user
            while loop:
                try:
                    ans_type(answer)
                    loop = False
                except:
                    print("Please enter an", ans_type, "answer.")
                    answer = Question.ask(question)
        else:
            try:
                ans_type(answer)
            except:
                print("Error. The answer was not an " + str(ans_type) + ".")

        return int(answer)

    @staticmethod
    def ask_int(question, loop=True):
        return Question.ask_type(question=question, ans_type=int, loop=loop)

    @staticmethod
    def ask_float(question, loop=True):
        return Question.ask_type(question=question, ans_type=float, loop=loop)

