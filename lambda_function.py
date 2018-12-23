from __future__ import print_function


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Google repeater. " \
                    "Tell me what you want to say to Google, " \
                    "I'll ask for you"
    reprompt_text = "Please tell me what I should say to Google, "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Have a nice day! "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def ask_to_google(intent, session, message, slots):
    if intent['name'] == "TurnOn" or intent['name'] == "TurnOff":
        try:
            slot = slots['light']['value']
        except Exception as e:
            slot = "all the lights"

    if intent['name'] == "iAm":
        slot = slots['action']['value']

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    speech_output = "Ok Google, " + message + slot
    reprompt_text = "Please tell me what I should say to Google, "

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_started(session_started_request, session):
    print("on_session_started requestId="
          + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return get_welcome_response()


def fallback_response():
    print('fallback_response')
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Fallback response"
    reprompt_text = "Fallback reprompt"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_intent(intent_request, session, event, context):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    try:
        slots = event['request']['intent']['slots']
        print('slots: ' + str(slots))
    except Exception as e:
        # raise e
        print('No slots')

    print('event: ' + str(event))
    print('intent_request: ' + str(intent_request))
    print('session: ' + str(session))
    print('intent: ' + str(intent))
    print('intent_name: ' + str(intent_name))

    if intent_name == "iAm":
        return ask_to_google(intent, session, "I am", slots)
    elif intent_name == "TurnOn":
        print('if turn on')
        return ask_to_google(intent, session, " Turn on ", slots)
    elif intent_name == "TurnOff":
        print('if turn off')
        return ask_to_google(intent, session, " Turn off ", slots)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or \
            intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.FallbackIntent":
        print('if fallback')
        return fallback_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], event, context)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
