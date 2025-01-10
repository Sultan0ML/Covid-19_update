# import streamlit as st
# from langchain_openai.chat_models import ChatOpenAI
# from langchain_openai.llms import OpenAI
# from langchain_community.document_loaders import PyPDFLoader
# import os
# from dotenv import load_dotenv
# from Get_Details import get_details_api
# from extract_pdf import extract_pdf_text
# load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    

# # Buyer_llm = OpenAI(temperature=0.9)
# Buyer_llm=ChatOpenAI(model="gpt-4", max_tokens=1080, temperature=0.7)

# Vendor_llm=OpenAI(temperature=0.7)
# #Vendor_llm=OpenAI(temperature=0.9)
# # Function to create the LLM prompt
# def create_prompt(benchmark_text, rfp_text, chat_history=None, current_question=None, vendor_response=None):
#     # Format the chat history into a string
#     chat_history_str = ""
#     if chat_history:
#         for entry in chat_history:
#             chat_history_str += f"**Buyer (Assistant):** {entry.get('bot_response', '')}\n"
#             if entry.get('vendor_responses'):
#                 chat_history_str += f"**Vendor Responses:** {', '.join(entry['vendor_responses'])}\n"
#     prompt = """
# Buyer Negotiation Representation

# Key Instructions:
# 1. Professionalism: Maintain a respectful and positive tone.
# 2. Vendor Interaction: Wait for the Vendor’s response before proceeding.
# 3. Negotiation Steps:
#    - Step 1: Greeting: Start with “Hello, I’m [Your Name], representing the Buyer. How are you today?” and wait for Vendor’s response.
#    - Step 2: Initial Offer:Present an initial offer that reflects the buyer's priorities,lower price, shorter timeline, and favorable terms.:
#      | Price     | Timeline     | Payment Terms         |
#      |-----------|--------------|-----------------------|
#      | [Price]   | [Timeline]   | [Terms]              |
#      Ask: “What do you think about this offer?”
#    - Step 3: Revised Proposals (if rejected): Provide 3 options:
#      Example:
#      | Option    | Price   | Timeline     | Payment Terms             |
#      |-----------|---------|--------------|---------------------------|
#      | Option 1  | ₹18,000 | 2025-01-15   | 50% upfront, 50% post-delivery |
#      | Option 2  | ₹18,300 | 2025-01-10   | 60% upfront, 40% post-delivery |
#      | Option 3  | ₹18,400 | 2024-12-31   | 40% upfront, 60% post-delivery |
#      Ask: “Which option works best for you, or would you like adjustments?”
#    - Step 4: Vendor Acceptance: If accepted, proceed to Confirm Agreement:
#      | Price      | Timeline       | Payment Terms      |
#      |------------|----------------|--------------------|
#      | [Final Price] | [Final Timeline] | [Final Terms]    |
#      Ask: “Please confirm the final agreement.”

# 4. Termination: When terms are confirmed:  
#    “Thank you for your time and cooperation; the deal is now finalized. This concludes our discussion.”

# 6. **Additional Negotiation Rules**:"""+extract_pdf_text()+f"""

# ### Context:
# - **Buyer’s Benchmarks**: {benchmark_text}.
# - **Vendor’s Proposal**: {rfp_text}.
# - **Chat History**: {f"Chat History: {chat_history_str}" if chat_history else "No previous chat history."}
# - **Vendor Response**: {f"**Vendor Response:** {vendor_response}" if vendor_response else "No response from Vendor."}

# ### Restrictions:
# - Do not proceed without Vendor’s response.
# - Focus on the buyer's priorities: ensuring a competitive price, an expedited timeline, and mutually favorable terms.
# Begin the negotiation now, using your expertise to craft the strategy.
# """
#     return prompt


# # Function to generate vendor response dynamically based on negotiation context
# def generate_vendor_responses(llm_response):

#     prompt = f"""
# You are a Vendor responding to the following Buyer conversation:
# - Buyer Statement: {llm_response} (This is the message from the Buyer. Pay close attention to their specific request, tone, and context.)

# Your task is to provide responses as required, ensuring the number of responses matches the context. For general queries, provide up to two responses (positive and negative). If the Buyer presents multiple options, respond to each option individually.. Each response should be **short and direct**, with no more than **3 words**:

# 1.  Provide a brief, positive reply directly addressing the Buyer’s statement (e.g., if the Buyer asks for a discount, respond with "Yes, we can"; if the Buyer agrees to terms, respond with "Great, let's proceed"). If the Buyer greets you, reply with a polite and short greeting (e.g., "Hello", "Good to hear").

# 2.  Provide a brief, negative reply based on the Buyer’s statement (e.g., if the Buyer asks for more, respond with "Not possible now"; if the Buyer’s request cannot be accommodated, respond with "Cannot accept terms"). If the Buyer greets you, provide a polite refusal or acknowledgment (e.g., "Not today", "Sorry, can't engage").

# **Key Instructions**: 
# - **Handling Multiple Options**:  
#    - Use this step only if the Buyer presents a proposal with multiple options in a table or list form.  
#    - Provide a short response to **each option separately** in the order presented, without additional commentary.
#    - For each option, respond with a simple acknowledgment such as "acceptable"; never say any option is "unacceptable".  
#      Example format:  
#     Buyer's response:
#             Option     | Price   | Timeline    | Payment Terms
#         ---------------------------------------------------
#         Option 1: Fastest  | $19,500 | 2025-01-31 | 92% post-delivery
#         Option 2: Balanced | $19,250 | 2025-02-07 | 85% post-delivery
#         Option 3: Cheapest | $19,000 | 2025-02-15 | 80% post-delivery
#     Vendor's response:
#         Option 1  
#         Option 2  
#         Option 3  
#         none of these

# - **End of Conversation**:  
#    - Use this step only If the Buyer concludes the conversation with a statement such as **"The deal is finalized. Please consider this the end of our discussion,"** respond only with **"Finalized. Take care!"**.  
#    - After this, never say "let's proceed" or "Great, let's proceed."
# - Always ensure your responses are concise, directly relevant to the Buyer’s specific statement, and reflect the negotiation context.  
# - Accurately interpret the Buyer’s statement, tone, and intent to provide meaningful responses.  
# - Deliver only the responses without any extra explanation or commentary.
# """
    
#     try:
#         response=Buyer_llm.invoke(prompt).content
#         #response = Vendor_llm.invoke(prompt)
#         if hasattr(response, 'text'):  # Adjust based on the actual attribute
#             responses = response.text.split('\n')
#             return [resp.strip() for resp in responses if resp.strip()]
#         elif isinstance(response, str):  # If it returns plain text
#             responses = response.split('\n')
#             return [resp.strip() for resp in responses if resp.strip()]
#         else:
#             raise AttributeError("Response object does not contain the expected attribute.")
#     except Exception as e:
#         st.error(f"Error generating vendor responses: {e}")
#         return ["Error generating responses. Please try again."]


# def get_final_agreed_term(chat_history):
#     agreed_prompt=f""" Analyze the following negotiation chat history {chat_history} and extract the agreed terms between the Assistant (representing the Buyer) and the Vendor. Provide the output strictly in JSON format containing the agreed values for "price", "delivery_date", and "payment_terms". Do not include any explanation or extra text.
#     """
#     try:
#         response = Vendor_llm.invoke(agreed_prompt).content
#         return st.write(response)
        
#     except Exception as e:
#         st.error(f"Error generating vendor responses: {e}")
#         return ["Error generating responses. Please try again."]
    
    
# # Function to check if the vendor response indicates conversation termination
# def check_for_termination(vendor_response):
#     termination_phrases = [
#         "Thank you, looking forward.",
#         "Looking forward, thanks!",
#         "Excited to proceed!",
#         "Thanks, we’ll follow-up!",
#         "Appreciate your response!",
#         "We’ll finalize shortly!",
#         "Thank you, let's proceed.",
#         "Thank you, happy to.",
#         "Thank you, Buyer.",
#         "Let's proceed then.",
#         "Excited for partnership.",
#         "Thank you, excited too.",
#         "Enjoy your day.",
#         "Thank you. Have a great day!",
#         "Thanks! Looking forward to working together.",
#         "Finalized. Take care!",
#         "Appreciate it. Goodbye!"
#     ]
    
#     # If any termination phrase is found in the vendor's response
#     for phrase in termination_phrases:
#         if phrase in vendor_response:
#             return True
#     return False


# # Streamlit App
# def main():
#     st.title("Negotiation Chatbot")
#     token =st.query_params.get("uniqueToken")
#     #st.write(token)
#     # docs=extract_pdf_text()
#     # st.write(docs)
#     # Output the token (note: use st.write in Streamlit instead of print)
#     vendor_rfp_text,benchmark_text = get_details_api(token)
#     # Initialize session state
#     if "conversation_history" not in st.session_state:
#         st.session_state.conversation_history = []

#     # Initialize conversation and first prompt
#     if not st.session_state.conversation_history:
#         prompt = create_prompt(benchmark_text, vendor_rfp_text, chat_history=st.session_state.conversation_history)
#         try:
#             response = Buyer_llm.invoke(prompt).content  # Access the 'content' instead of 'text'
#             st.session_state.conversation_history.append({
#                 "bot_response": response.strip(),
#                 "vendor_responses": generate_vendor_responses(response.strip())
#             })
#         except Exception as e:
#             st.error(f"Error generating response: {e}")
#             st.session_state.conversation_history.append({
#                 "bot_response": "Error generating response.",
#                 "vendor_responses": []
#             })

#     # Display chat history
#     st.subheader("Chat History")
#     for index, entry in enumerate(st.session_state.conversation_history):
#         st.write(f"**Assistant:** {entry.get('bot_response', 'No response generated.')}")

#         # Display vendor response buttons
#         st.write("**Vendor Responses:**")
#         for response_index, vendor_response in enumerate(entry.get('vendor_responses', [])):
#             # Check if the vendor response indicates termination
#             if check_for_termination(vendor_response):
#                 st.write("**Conversation Terminated**: All terms have been finalized and confirmed by the Vendor.")

                
#                 get_final_agreed_term(st.session_state.conversation_history)
                
#                 return  # End the conversation if termination condition is met

#             # Create unique keys for each button
#             button_key = f"vendor_response_{index}_{response_index}"
#             if st.button(vendor_response, key=button_key):
#                 # Add vendor response and bot follow-up to history
#                 new_prompt = create_prompt(benchmark_text, vendor_rfp_text, chat_history=st.session_state.conversation_history,
#                                            vendor_response=vendor_response)
#                 try:
#                     bot_response = Buyer_llm.invoke(new_prompt).content # Access 'content' instead of 'text'
#                     st.session_state.conversation_history.append({
#                         "bot_response": bot_response.strip(),
#                         "vendor_responses": generate_vendor_responses(bot_response.strip())
#                     })
#                 except Exception as e:
#                     st.error(f"Error generating follow-up response: {e}")
#                     st.session_state.conversation_history.append({
#                         "bot_response": "Error generating follow-up response.",
#                         "vendor_responses": []
#                     })
                    
# # Run the if __name__ == "__main__":
# if __name__ == "__main__":
#     main()


from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain_openai.llms import OpenAI
import streamlit as st
from dotenv import load_dotenv
from Get_Details import get_details_api
from extract_pdf import extract_pdf_text
import os

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Initialize LLMs
Buyer_llm = ChatOpenAI(model="gpt-4", max_tokens=1080, temperature=0.7)
Vendor_llm = OpenAI(temperature=0.7)

# Create ChatPromptTemplate with MessagesPlaceholder
def create_prompt(benchmark_text, rfp_text,margin):
    system_message = SystemMessage(
        content=f"""
        Buyer Negotiation Representation

Key Instructions:
1. Professionalism: Maintain a respectful and positive tone.
2. Always present proposals in a table format.
3. Vendor Interaction: Wait for the Vendor’s response before proceeding.
4. Negotiation Steps:
   - Step 1: Greeting: Start with “Hello, I’m [Your Name], representing the Buyer. How are you today?” and wait for Vendor’s response.
            -If the Vendor gives a negative response, respond politely: “Sorry to hear that. Hope things improve. Shall we continue the negotiation details later?”
   - Step 2: Initial Offer:Present an initial offer 15% below the buyer's margin or a randomly proposed amount, reflecting priorities like lower price, shorter timeline, and favorable terms. 
     | Price     | Timeline     | Payment Terms         |
     |-----------|--------------|-----------------------|
     | [Price]   | [Timeline]   | [Terms]              |
     Ask: “What do you think about this offer?”
   - Step 3: Revised Proposals (if rejected): Provide 3 options:
     Example:
     | Option    | Price   | Timeline     | Payment Terms|
     |-----------|---------|--------------|--------------|
     | Option 1  | [Price] | [Timeline]   | [Terms] |
     | Option 2  | [Price] | [Timeline]   | [Terms] |
     | Option 3  | [Price] | [Timeline]   | [Terms] |
     Ask: “Which option works best for you, or would you like adjustments?”
   - Step 4: Vendor Acceptance: If accepted, proceed to Confirm Agreement:
     | Price      | Timeline       | Payment Terms      |
     |------------|----------------|--------------------|
     | [Final Price] | [Final Timeline] | [Final Terms]    |
     Ask: “Please confirm the final agreement.”

    - If the vendor rejects the revised proposals three times, present the final options and say, 'This is my last proposal. Please choose one if suitable to finalize the deal; otherwise, we must conclude the negotiation. Let me know your thoughts.
    - End the Conversation if Rejected:
        "Thank you for your time. It seems we cannot align on the terms at this moment, so I must conclude our discussion. I wish you the best in your future endeavors."
5. Termination: When terms are confirmed:  
   “Thank you for your time and cooperation; the deal is now finalized. This concludes our discussion.”

6. **Negotiation Strategy : Strictly adhere to this
 {extract_pdf_text()}  during the negotiation.
### Context:
- **Buyer’s Benchmarks**: {benchmark_text}.
- **Vendor’s Proposal**: {rfp_text}.
- **Buyer's Margin**: The margin limit is {margin}, which is less than the final benchmark price**

### Restrictions:
- Do not proceed without Vendor’s response.
- Based on the vendor's response context, initiate negotiation by following the defined strategy and step-by-step flow.
Begin the negotiation now.
        """
    )

    return ChatPromptTemplate.from_messages(
        [system_message, MessagesPlaceholder(variable_name="messages")]
    )

# Prepare chat history for MessagesPlaceholder
def prepare_chat_history(chat_history):
    messages = []
    for entry in chat_history:
        bot_response = entry.get("bot_response", "")
        if bot_response:
            messages.append(AIMessage(content=bot_response))
        
        vendor_responses = entry.get("vendor_responses", [])
        for vendor_response in vendor_responses:
            messages.append(HumanMessage(content=vendor_response))
    
    return messages

# Generate vendor responses
# Function to generate vendor response dynamically based on negotiation context
def generate_vendor_responses(llm_response):

    # prompt = f"""
    # You are a Vendor responding to the following Buyer conversation:
    # - Buyer Statement: {llm_response} (This is the message from the Buyer. Pay close attention to their specific request, tone, and context.)

    # Your task is to provide response as required, ensuring the number of responses matches the context. For general queries, provide up to two responses (positive and negative). If the Buyer presents multiple options, respond to each option individually.. Each response should be **short and direct**, with no more than **3 words**:

    # 1.  Provide a brief, positive reply directly addressing the Buyer’s statement (e.g., if the Buyer asks for a discount, respond with "Yes, we can"; if the Buyer agrees to terms, respond with "Great, let's proceed"). If the Buyer greets you, reply with a polite and short greeting **"Hello", "Good to hear"**.

    # 2.  Provide a brief, negative reply based on the Buyer’s statement (e.g., if the Buyer asks for more, respond with "Not possible now"; if the Buyer’s request cannot be accommodated, respond with "Cannot accept terms"). If the Buyer greets you, provide a polite refusal or acknowledgment (e.g., "Not today", "Sorry, can't engage").

    # **Key Instructions**: 
    # - **Handling Multiple Options**:  
    # - Use this step only if the Buyer presents a proposal with multiple options in a table or list form.  
    # - Provide a short response to each option separately, following the format shown in the example output below, without additional commentary:
    #     Vendor's response:
    #     Option 1: acceptable
    #     Option 2: acceptable
    #     Option 3: acceptable
    #     Need adjustment.

    # - **End of Conversation**:
    # - use this step only if the Buyer concludes the conversation with statement such as **"Thank you for your time. It seems we cannot align on the terms at this moment, so I must conclude our discussion. I wish you the best in your future endeavors."** respond only with **"Goodbye, all the best."**
    # - Use this step only If the Buyer concludes the conversation with a statement such as **"The deal is finalized. Please consider this the end of our discussion,"** respond only with **"Finalized. Take care!"**.  
    # - After this, never say "let's proceed" or "Great, let's proceed."
    # - **
    # - Always ensure your responses are concise, directly relevant to the Buyer’s specific statement, and reflect the negotiation context.  
    # - Accurately interpret the Buyer’s statement, tone, and intent to provide meaningful responses to the Buyer on behalf of the Vendor.  
    # - Deliver only the responses without any extra explanation or commentary.
    # """
    prompt = f"""
    You are a Vendor responding to the following Buyer conversation:
    - Buyer Statement: {llm_response} (This is the message from the Buyer. Pay close attention to their specific request, tone, and context.)

     Your task is to provide response as required, ensuring the number of responses matches the context. For general queries and single-option tables, provide up to two responses: one positive and one negative. If the Buyer presents multiple options, respond to each option individually. Each response should be **short and direct**, with no more than **3 words**:

     1.  Provide a brief, positive reply directly addressing the Buyer’s statement (e.g., if the Buyer asks for a discount, respond with "Yes, we can"; if the Buyer agrees to terms, respond with "Great, let's proceed"). If the Buyer greets you, reply with a polite and short greeting **"Hello", "Good to hear"**.

     2.  Provide a brief, negative reply based on the Buyer’s statement (e.g., if the Buyer asks for more, respond with "Not possible now"; if the Buyer’s request cannot be accommodated, respond with "Cannot accept terms"). If the Buyer greets you, provide a polite refusal or acknowledgment (e.g., "Not today", "Sorry, can't engage").

     **Handling Multiple Options**:  
    - Use this step only if the Buyer presents a proposal with multiple options in a table or list form.  
    - Provide a  only four response separately, following the **Expected output format** shown below, without additional commentary and extra responses:
        **Expected output format:
        - Option 1: acceptable
        - Option 2: acceptable
        - Option 3: acceptable
        - Need adjustment.

     **End of Conversation**:  
    - If the Buyer concludes the conversation, respond as follows:  
        - If the statement is: “Sorry to hear that. Hope things improve. Shall we continue the negotiation details later?"** respond only with **"Let's talk later."
        - If the statement is: "Thank you for your time. It seems we cannot align on the terms at this moment, so I must conclude our discussion. I wish you the best in your future endeavors." ** respond only with **"Goodbye, all the best."**  
        - If the statement is: "The deal is finalized. Please consider this the end of our discussion." ** respond only with **"Finalized. Take care!"**.  
    **Key Guidelines**:
    - Keep responses concise, directly relevant, and aligned with the negotiation context.
    - Accurately interpret the Buyer’s statement, tone, and intent to provide meaningful responses on behalf of the Vendor.
    - Deliver only the responses without any explanation or commentary.
    - Stay in Character: Always maintain the perspective of the Vendor. Do not switch roles or perspectives.
    """

    try:
        response=Buyer_llm.invoke(prompt).content
        #response = Vendor_llm.invoke(prompt)
        if hasattr(response, 'text'):  # Adjust based on the actual attribute
            responses = response.text.split('\n')
            return [resp.strip() for resp in responses if resp.strip()]
        elif isinstance(response, str):  # If it returns plain text
            responses = response.split('\n')
            return [resp.strip() for resp in responses if resp.strip()]
        else:
            raise AttributeError("Response object does not contain the expected attribute.")
    except Exception as e:
        st.error(f"Error generating vendor responses: {e}")
        return ["Error generating responses. Please try again."]


def get_final_agreed_term(chat_history):
    agreed_prompt=f""" 
    - Analyze the following negotiation chat history {chat_history} and extract the agreed terms between the Assistant (representing the Buyer) and the Vendor. 
    - Provide the output strictly in JSON format containing the agreed values for "price", "delivery_date", and "payment_terms".
    - If there are no agreed terms in the chat history, return "Deal is not finalized."

    """
    try:
        response = Vendor_llm.invoke(agreed_prompt)
        return st.write(response)
        
    except Exception as e:
        st.error(f"Error generating vendor responses: {e}")
        return ["Error generating responses. Please try again."]
    
    
# Function to check if the vendor response indicates conversation termination
def check_for_termination(vendor_response):
    termination_phrases = [
        "Finalized. Take care!",
        "Goodbye, all the best.",
        "Let's talk later."
    ]
    
    # If any termination phrase is found in the vendor's response
    for phrase in termination_phrases:
        if phrase in vendor_response:
            return True
    return False

# Streamlit App
def main():
    st.title("Negotiation Chatbot")
    token = st.query_params.get("uniqueToken")
    vendor_rfp_text, benchmark_text = get_details_api(token)
    margin="10%"
    # Initialize session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Create ChatPromptTemplate
    prompt = create_prompt(benchmark_text, vendor_rfp_text,margin)
    messages = prepare_chat_history(st.session_state.conversation_history)
    chain = prompt | Buyer_llm

    # Start the conversation if no history exists
    if not st.session_state.conversation_history:
        response = chain.invoke({"messages": messages}).content
        st.session_state.conversation_history.append({
            "bot_response": response.strip(),
            "vendor_responses": generate_vendor_responses(response.strip())
        })

    # Display chat history
    st.subheader("Chat History")
    for index, entry in enumerate(st.session_state.conversation_history):
        st.write(f"**Assistant:** {entry.get('bot_response', 'No response generated.')}")
        st.write("**Vendor Responses:**")
        for response_idx, response in enumerate(entry.get("vendor_responses", [])):
            if st.button(response, key=f"response_{index}_{response_idx}"):
                if check_for_termination(response):
                    st.write("**Conversation Terminated**")
                    st.write("Thank you for your time and consideration; I look forward to the possibility of working together in the future.")
                    if response=="Finalized. Take care!":
                        final_terms = get_final_agreed_term(st.session_state.conversation_history)
                        st.json(final_terms)
                        return
                    else:
                        return None
                else:
                    #new_prompt = create_prompt(benchmark_text, vendor_rfp_text,,margin)
                    new_messages = prepare_chat_history(st.session_state.conversation_history + [{"bot_response": response}])
                    next_response = chain.invoke({"messages": new_messages}).content
                    st.session_state.conversation_history.append({
                        "bot_response": next_response.strip(),
                        "vendor_responses": generate_vendor_responses(next_response.strip())
                    })


if __name__ == "__main__":
    main()