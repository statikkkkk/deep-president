"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib.request



# --------------- Events ------------------

# def on_session_started(session_started_request, session):
#     """ Called when the session starts """

#     print("on_session_started requestId=" + session_started_request['requestId']
#           + ", sessionId=" + session['sessionId'])


# def on_launch(launch_request, session):
#     """ Called when the user launches the skill without specifying what they
#     want
#     """

#     print("on_launch requestId=" + launch_request['requestId'] +
#           ", sessionId=" + session['sessionId'])
#     # Dispatch to your skill's launch
#     return "Welcome to Polispeech!"


def on_intent(intent_request):
    """ Called when the user specifies an intent for this skill """

    # print("on_intent requestId=" + intent_request['requestId'] +
    #       ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print(intent_name)
    # # Dispatch to your skill's intent handlers
    if intent_name == "DemocratIntent":
        return urllib.request.urlopen("http://54.224.141.100/generate_democrat_sentence").read()
    elif intent_name == "RepublicanIntent":
        return urllib.request.urlopen("http://54.224.141.100/generate_republican_sentence").read()
    elif intent_name == "SandersIntent":
        return urllib.request.urlopen("http://54.224.141.100/generate_sanders_sentence").read()
    elif intent_name == "ClintonIntent":
        return urllib.request.urlopen("http://54.224.141.100/generate_clinton_sentence").read()
    elif intent_name == "TrumpIntent":
        return urllib.request.urlopen("http://54.224.141.100/generate_trump_sentence").read()
    # elif intent_name == "AMAZON.HelpIntent":
    #     return get_welcome_response()
    # elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
    #     return handle_session_end_request()
    # else:
    #     raise ValueError("Invalid intent")


# def on_session_ended(session_ended_request, session):
#     """ Called when the user ends the session.

#     Is not called when the skill returns should_end_session=true
#     """
#     print("on_session_ended requestId=" + session_ended_request['requestId'] +
#           ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------



def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
  

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    

    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
    
    if event['request']['type'] == "IntentRequest": 
        return  {"version": "1.0", "sessionAttributes": {}, "response": {"outputSpeech": {"type": "PlainText","text": on_intent(event['request']).decode("utf8")},"shouldEndSession" : False}}
    else:
        return {"version": "1.0", "sessionAttributes": {}, "response": {"outputSpeech": {"type": "PlainText","text": "Welcome! Please say a command."},"shouldEndSession" : False}}



