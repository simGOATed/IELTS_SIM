import google.generativeai as genai


class TextGen:
    def __init__(self, mode='chat_intro'):
        genai.configure(api_key = "AIzaSyBEnq-XO7cNHs8byP7ZNkkT1x0R2vHslpg")
        self.setup_model(mode)

    def setup_model(self, mode):
        if mode == 'chat_intro':
            self.model = self.initialize_model_chat_intro()
            self.chat = self.model.start_chat()
        elif mode == 'chat_long_turn':
            self.model = self.initialize_model_chat_long_turn()
            self.chat = self.model.start_chat()
        elif mode == 'chat_discussion':
            self.model = self.initialize_model_chat_discussion()
            self.chat = self.model.start_chat()
        elif mode == 'chat_test':
            self.model = self.initialize_model_chat_test()
            self.chat = self.model.start_chat()
        elif mode == 'eval':
            self.model = self.initialize_model_eval()

    def initialize_model_chat_intro(self):
        return genai.GenerativeModel(model_name = "gemini-1.5-flash",
                                     system_instruction = "You are an IELTS spoken test examiner. You are to conduct "
                                                          "conversations for part 1: introduction and interview in the "
                                                          "IELTS spoken test format and give opportunities for the "
                                                          "examinee to show their capabilities in spoken English. "
                                                          "After each response from the examinee, you will be shown how "
                                                          "much time has elapsed in the round. After 2 minutes have "
                                                          "passed, wrap up the conversation. Do not include unnecessary "
                                                          "punctuation in your responses. Do not ask for ID at the start. "
                                                          "Instead, introduce yourself (you're a lady) and ask the "
                                                          "examinee to introduce themselves. Keep in mind that responses "
                                                          "by examinees are transcribed using AI so mistakes can occur in "
                                                          "that process. Do not mention anything about how much time has "
                                                          "elapsed unless it is relevant.")

    def initialize_model_chat_long_turn(self):
        return genai.GenerativeModel(model_name = "gemini-1.5-flash",
                                     system_instruction = "You are an IELTS spoken test examiner. You are to conduct "
                                                          "part 2: long turn in the IELTS spoken test. You are to "
                                                          "generate a task card in paragraph form that asks the "
                                                          "examinee to talk about a particular topic, including points "
                                                          "to cover during their talk. After each response from the "
                                                          "examinee, you will be shown how much time has elapsed in "
                                                          "the round. If less than 1 minute has passed, encourage the "
                                                          "examinee to add some more detail to the topic, otherwise "
                                                          "thank them for their response and wrap up the conversation. "
                                                          "Do not include unnecessary punctuation in your responses. "
                                                          "Do not ask for ID at the start. Instead, introduce yourself "
                                                          "(female) and ask the examinee to introduce themselves. "
                                                          "Keep in mind that responses by examinees are transcribed "
                                                          "using AI so mistakes can occur in that process. Feel free "
                                                          "to seek clarification if necessary."
                                                          "Do not mention anything about how much time has "
                                                          "elapsed unless it is relevant.")

    def initialize_model_chat_discussion(self):
        return genai.GenerativeModel(model_name = "gemini-1.5-flash",
                                     system_instruction = "You are an IELTS spoken test examiner. You are to conduct "
                                                          "the Two-Way Discussion section of the IELTS spoken test. "
                                                          "Engage in a discussion with the examinee on a given topic, "
                                                          "encouraging them to express their ideas, opinions, and "
                                                          "arguments. Provide prompts and follow-up questions to keep "
                                                          "the conversation flowing. After each response from the "
                                                          "examinee, you will be shown how much time has elapsed in "
                                                          "the round. After 2 minutes have passed, wrap up the "
                                                          "conversation and thank the examinee for participating."
                                                          "Do not include unnecessary punctuation in your responses. "
                                                          "Keep in mind that responses by examinees are transcribed "
                                                          "using AI so mistakes can occur in that process. Feel free "
                                                          "to seek clarification if necessary."
                                                          "Do not mention anything about how much time has "
                                                          "elapsed unless it is relevant.")

    def initialize_model_chat_test(self):
        return genai.GenerativeModel(model_name = "gemini-1.5-flash",
                                     system_instruction = "You are a female IELTS spoken test examiner. You are to conduct "
                                                          "a full IELTS spoken test. After each response from the "
                                                          "examinee, you will be shown how much time has elapsed in "
                                                          "the test."
                                                          "For part 1: introduction and interview in the test, first "
                                                          "ask the examinee for their name instead of asking for ID. "
                                                          "Afterward, ask about general topics such as home, work, "
                                                          "family and studies."
                                                          "For part 2: long turn in the IELTS spoken test. generate "
                                                          "a task card in paragraph form that asks the examinee "
                                                          "to talk about a particular topic, including points to cover "
                                                          "during their talk. Ideally it should be related to a topic "
                                                          "touched on in part 1. If less than 1 minute has passed, "
                                                          "since the start of the part 2, encourage the examinee to "
                                                          "add some more detail to the topic, otherwise thank them "
                                                          "for their response and move on to part 3." 
                                                          "For part 3, engage in a discussion with the examinee on the "
                                                          "topic talked about in part 2. Encourage them to express "
                                                          "their ideas, opinions, and arguments. Provide prompts "
                                                          "and follow-up questions to keep the conversation flowing."
                                                          "6 minutes after the start of the test, make sure you "
                                                          "wrap up the conversation and thank the examinee for "
                                                          "participating. Make sure not to  include unnecessary "
                                                          "punctuation in your responses."
                                                          "Keep in mind that responses by examinees are transcribed "
                                                          "using AI so mistakes can occur in that process. Feel free "
                                                          "to seek clarification if necessary."
                                                          "Do not mention anything about how much time has "
                                                          "elapsed unless it is relevant.")

    def initialize_model_eval(self):
        return genai.GenerativeModel(model_name = "gemini-1.5-flash",
                                     system_instruction = "You are an IELTS spoken test evaluator that provides feedback "
                                                          "to examinees. You are tasked with reviewing transcribed "
                                                          "conversations and providing custom feedback like corrected "
                                                          "sentences, pronunciation tips, vocabulary suggestions etc. "
                                                          "Keep in mind that these are AI-generated transcripts so if "
                                                          "what is apparently said is incoherent but there is a coherent "
                                                          "idea with similar phonetics, give the examinee the benefit of "
                                                          "the doubt. You are also tasked with scoring examinees based "
                                                          "on the IELTS criteria of Fluency & Coherence, Lexical Resource "
                                                          "and Grammatical Range & Accuracy. Use the band system for each "
                                                          "criterion, then give an overall estimated band.")

    def conversation(self, message):
        response = self.chat.send_message(message, stream = False)
        return response.text

    def feedback(self, conv, f_type='partial'):
        if f_type == 'partial':
            response = self.model.generate_content(f"This is an extract from an IELTS spoken test: \n{conv}\n"
                                                   "Examine it keeping in mind it's an AI generated transcript and "
                                                   "some transcription errors may be present. Address the candidate "
                                                   "directly with your response. Keep your response to about 100 words."
                                                   , stream = False)
            return response.text
        elif f_type == 'full':
            response = self.model.generate_content(f"This is a conversation from an IELTS spoken test: \n{conv}\n"
                                                   "Examine it keeping in mind it's an AI generated transcript and "
                                                   "some transcription errors may be present. Address the candidate "
                                                   "directly with your response. Start by thanking the candidate for "
                                                   "participating."
                                                   "Address each section individually with a paragraph of about 100 "
                                                   "words each, then with a final paragraph, summarize your findings "
                                                   "and show their final scores.",
                                                   stream = False)
            return response.text
