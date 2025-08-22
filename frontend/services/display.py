import streamlit as st

def json_to_markdown(results: dict):
    full_text = ''

    # Add main text if exists
    if results.get('text'):
        full_text += f"## Text:\n{results.get('text')}\n\n"

    # Add Q&A section if exists
    if results.get('QA'):
        qa_list = results.get('QA')
        full_text += "## Question & Answer:\n"
        for idx, qa_item in enumerate(qa_list):
            full_text += f"#### Q{idx+1}:\n{qa_item.get('question')}\n"
            full_text += f"#### Answer {idx+1}:\n{qa_item.get('answer')}\n\n"
            full_text += "-"*15 + "\n\n"  # separator with extra newline

    return full_text



def qa_result_display(response:dict):
        

    ##Tabs for Choose The Tab:
    tab1,tab2=st.tabs(['text plain','json'])

    #for tab1 for text display
    tab1.markdown(json_to_markdown(response))
    col1, col2, col3,col4 = tab1.columns(4)
    col1.metric("Total Tokens:", f"{response.get('total_input_tokens')+response.get('total_output_tokens')}", None)
    col2.metric("Total Input Cost", f"{response.get('input_cost'):.4f}$", None)
    col3.metric("Total Output Cost", f"{response.get('output_cost'):4f}$", None)
    col4.metric("Total Cost", f"{response.get('total_cost'):.4f}$", None)

    #tab2 For Json Display
    tab2.json(response)