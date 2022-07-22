from typing import Any, Text, Dict, List
import re
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from pymongo import MongoClient



class ValidateDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_details_form"

    def validate_fname(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `fname` value."""

        # Matching RegEx for Name.
        pattern = "[a-zA-Z][a-zA-Z ]+[a-zA-Z]$"
        test_string = slot_value
        result = re.match(pattern, test_string)
        if result:
            return {"fname": slot_value}
        else:
            dispatcher.utter_message(text="Please enter a valid Name")
            return {"fname": None}

    def validate_lname(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `lname` value."""

        # Matching RegEx for Name.
        pattern = "[a-zA-Z][a-zA-Z ]+[a-zA-Z]$"
        test_string = slot_value
        result = re.match(pattern, test_string)
        if result:
            return {"lname": slot_value}
        else:
            dispatcher.utter_message(text="Please enter a valid Name")
            return {"lname": None}

    def validate_company(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `company` value."""

        # Matching RegEx for Name.
        pattern = "^[A-Z]+[a-zA-Z]*$"
        test_string = slot_value
        result = re.match(pattern, test_string)
        if result:
            return {"company": slot_value}
        else:
            dispatcher.utter_message(text="Please enter a valid Company Name")
            return {"company": None}


    def validate_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `phone` value."""

        # Matching RegEx for Name.
        pattern = "^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$"
        test_string = slot_value
        result = re.match(pattern, test_string)
        if result:
            return {"phone": slot_value}
        else:
            dispatcher.utter_message(text="Please enter a valid Phone number..")
            return {"phone": None}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `email` value."""

        # Matching RegEx for Name.
        pattern = "^([\w.-]+)@(\[(\d{1,3}\.){3}|(?!hotmail|gmail|googlemail|yahoo|gmx|ymail|outlook|bluewin|protonmail|t\-online|web\.|online\.|aol\.|live\.)(([a-zA-Z\d-]+\.)+))([a-zA-Z]{2,63}|\d{1,3})(\]?)$"
        test_string = slot_value
        result = re.match(pattern, test_string)
        if result:
            return {"email": slot_value}
        else:
            dispatcher.utter_message(text="Please enter a valid E-mail address")
            return {"email": None}
    

class ActionSaveConversation(Action):
    
    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import os.path
        conversation = tracker.events
        chat_data=''
        for i in conversation:
            if i['event'] == 'user':
                chat_data+=f"user: {i['text']}\n"
            elif i['event'] == 'bot':
                chat_data+=f"bot: {i['text']}\n"
        client = MongoClient("mongodb+srv://pranavmm:IKJmGfPCmq2OeYpG@cluster0.ywa3s.mongodb.net/?retryWrites=true&w=majority")
        db=client.get_database('Chatbot')
        fname = tracker.get_slot("fname")
        lname = tracker.get_slot("lname")
        company = tracker.get_slot("company")
        phone = tracker.get_slot("phone")
        email = tracker.get_slot("email")
        details = {
                'First Name' : fname,
                'Last Name' : lname,
                'Company Name': company,
                'phone' : phone,
                'email' : email,
                'transcript': chat_data
            }
        db.Details.insert_one(details)
            # global id 
            # id = result.inserted_id
        client.close()
        # save_path = 'J:/OneDrive - Alp Consulting Ltd/ChatBot/Transcripts/'
        # filename = "transcript_{0}.txt".format(id)
        # completeName = os.path.join(save_path, filename)
        
        # with open(completeName,'w') as file:
        #     file.write(chat_data) 
        return []


class ActionRestart(Action):

    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("fname",None),SlotSet("lname",None),SlotSet("company",None),SlotSet("phone",None),SlotSet("email",None)]
