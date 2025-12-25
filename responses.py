import re
import asyncio

async def process_message(message, response_array, response):
    #split message and punctuation into an array
    list_message = re.findall(r"[\w']+|[.,!?;]", message.lower())

    #scores amount of words in message
    score = 0
    for word in list_message:
        if word in response_array:
            score = score + 1

    #returns response and score
    #print(score, response)
    return [score, response]

async def get_response(message):
    response_list = [
        await process_message(message, ['hello', 'hi', 'hey'], 'Hey there!!'),
        await process_message(message, ['bye', 'goodbye'], 'Goodbye!'),
        await process_message(message, ['how', 'are', 'you'], 'I\'m doing great wby?'),
        await process_message(message, ['your', 'name'], 'My name is Magnus, nice to meet you'),
        await process_message(message, ['help', 'me'], 'I will do my best buddy, ssup?'),
        #add responses
    ]

    #check all response scores and return best matching
    response_scores = []
    for response in response_list:
        response_scores.append(response[0])

    # Get the max value for the best response and store it into a variable
    winning_response = max(response_scores)
    matching_response = response_list[response_scores.index(winning_response)]

    #return the match response to user
    if winning_response == 0:
        bot_response = 'Didn\'t quite get that, pardon?'
    else:
        bot_response = matching_response[1]

    print('Bot response: ', bot_response)
    return bot_response

    #test system
#asyncio.run(get_response('What is your name brev?'))