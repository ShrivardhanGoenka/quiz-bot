
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

## I have also made some changes to the chat.html file. This was due to some faults in the code that I found from the frontend perspective. Firstly, \n in the python code was not getting converted to <br> in html format and hence the questions were not being displayed properly. Secondly, one of the options to question 4: <!-- Comment --> was not being displayed in html because of it being a comment in html. I have changed it to &lt;!-- Comment --&gt; to display it properly.

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")

    #This is wrong. It should not be if not current_question_id. It should be if current_question_id is None. Because this is negating the 0 current id as well and then sending the welcome message again.
    # if not current_question_id:
    #     bot_responses.append(BOT_WELCOME_MESSAGE)\
    if current_question_id == None:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''

    # No need for validation if current_question_id is None. This means that this is the hi sent by the user. 
    if current_question_id == None:
        return True, ""

    # Backend validation. No need technically as the frontend is handling this. 
    if not answer:
        return False, "Please provide an answer."
    
    #check if the answer is a nummber
    if not answer.isdigit():
        return False, "Please provide a valid number."
    
    answer = int(answer)
    
    #check if the answer is in the range of the options
    if answer < 1 or answer > len(PYTHON_QUESTION_LIST[current_question_id]["options"]):
        return False, "Please provide a valid number between 1 and " + str(len(PYTHON_QUESTION_LIST[current_question_id]["options"]))

    #store the answer in the session
    session["answer_" + str(current_question_id)] = PYTHON_QUESTION_LIST[current_question_id]["options"][answer-1]
    session.save()

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    next_question_id = None
    # first question
    if current_question_id == None:
        next_question_id = 0
    # last question
    elif current_question_id == len(PYTHON_QUESTION_LIST) - 1:
        return None, None
    # middle questions
    else:
        next_question_id = current_question_id + 1
    
    #display the next question
    next_question = "Question " + str((next_question_id+1)) + "\n" + PYTHON_QUESTION_LIST[next_question_id]["question_text"] + "\n\n" + "The Options are: \n"
    for i, option in enumerate(PYTHON_QUESTION_LIST[next_question_id]["options"]):
        next_question += f"{i+1}. {option} \n"

    return next_question, next_question_id


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    #count the number of correct answers
    for i, question in enumerate(PYTHON_QUESTION_LIST):
        print( session.get("answer_" + str(i)) + " " + question["answer"])
        if session.get("answer_" + str(i)) == question["answer"]:
            correct_answers += 1

    #display the final result
    result = f"You have answered {correct_answers} out of {total_questions} questions correctly.\n Thank you for taking the quiz!"

    return result
