import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

st.set_page_config(page_title="Workout Builder GPT")

openai_api_key = st.secrets["OPENAI_API_KEY"]
llm = OpenAI(openai_api_key=openai_api_key, temperature = 0)

st.title("Workout GPT")

template = """
You are a personal fitness trainer.
Create a single full body workout plan in a bullet list.
You only have body weight and {eq}.
"""

prompt = PromptTemplate(
    input_variables=['eq'],
    template=template
)

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="log"
)

with st.form("eq_list"):
    equipments = st.multiselect(
        "Available equipments",
        options = ['Dumbbell','Barbell','Bench','Pull up bar','Leg press machine','Leg curl machine','Lat pull down','Cable row machine'],
        default = ['Dumbbell']
    )

    equipments = ", ".join(equipments)

    submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner("Building workout plan..."):
        response = llm_chain({'eq':equipments})
        st.write(response['log'])