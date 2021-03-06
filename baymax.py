import boto3
ddb = boto3.client("dynamodb")
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Welcome to BayMax. Choose agenda or medicine ....").set_should_end_session(False)
        return handler_input.response_builder.response    

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print(exception)
        handler_input.response_builder.speak("Sorry, there was some problem. Please try again!!")
        return handler_input.response_builder.response
class AgendaAskIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AgendaAskIntent")(handler_input)   
    def handle(self, handler_input):
        year = handler_input.request_envelope.request.intent.slots['year'].value
        try:
            data = ddb.get_item(
                TableName="event_bay_max3",
                Key={
                    'id': {
                        'N': year
                    }
                }
            )
         except BaseException as e:
            print(e)
            raise(e)
        speech_text = "The agenda is:"+ data['Item']['event']['S']+ " on "+data['Item']['date']['S']+" at "+data['Item']['time']['S'] + " in "+ data['Item']['place']['S']
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response    

class MedicineAskIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("MedicineAskIntent")(handler_input)   
    def handle(self, handler_input):
        year = handler_input.request_envelope.request.intent.slots['year'].value
        try:
            data = ddb.get_item(
                TableName="medicine_baymax",
                Key={
                    'id': {
                        'N': year
                    }
                }
            )
         except BaseException as e:
            print(e)
            raise(e)
        speech_text = "The medicine is"+ data['Item']['Medicine']['S']+ " on "+data['Item']['date']['S']+" at "+data['Item']['time']['S'] + " in "+ data['Item']['hospital']['S']
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response
        
def handler(event, context):
    
    return sb.lambda_handler()(event, context)
