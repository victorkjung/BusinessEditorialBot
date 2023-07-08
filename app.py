import streamlit as st
import pandas as pd
import os
import openai
from docx import Document

def generate_response(prompt, openai_key):
    openai.api_key = openai_key

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt
        )
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

    return completion.choices[0].message['content']

def generate_docx(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def main():
    st.title("Business Editorial :robot_face: Bot :tm: ")

    st.sidebar.header("**About this :rocket: App**")
    st.sidebar.write("""
        This app generates a prompt and business article summary using OpenAI ChatGPT.
    """)

    st.sidebar.header("**:ledger: Instructions**")
    st.sidebar.write("""
        1. Paste the URL in the 'Enter the URL' field.
        2. Select the tone of the article summary from the 'Select Tone' field.
        3. Click 'Generate' to create your custom article summary prompt.
        4. Enter your OpenAI API key in the 'Enter your OpenAI API Key' field below.
    """)

    openai_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

    st.sidebar.markdown(
        '[Access your OpenAI API :key: Key](https://platform.openai.com/account/api-keys)', unsafe_allow_html=True)

    st.sidebar.header("**About the Developer**")
    st.sidebar.write("""
        **Victor Jung** is a serial entrepreneur and technology hobbyist. He is passionate about building innovative solutions and leveraging technology to solve real-world problems. With a diverse background in business and technology, Victor has successfully launched and managed multiple ventures.

        This article summarizer was developed using **PyCharm**, a powerful integrated development environment (IDE), and **GitHub Co-Pilot**, an AI-powered coding assistant. The collaboration between Victor and GitHub Co-Pilot streamlined the programming process, ensuring efficient code generation and error correction.
    """)

    st.sidebar.markdown(
        '[Buy 🤩 me a :coffee: coffee](https://www.buymeacoffee.com/5gDeDWWMCI)', unsafe_allow_html=True)

    template = ("You are an :first_place_medal: award-winning business reporter for the :chart: Wall Street Journal. "
                "Summarize the following article into a **{Tone}** LinkedIn 500-word "
                "post of 7 sections - Headline, introduction about the topic, "
                "listicle on key points, an overview of the topic, an analysis of "
                "the topic, supporting argument, and conclusion: **{URL}**")
    st.write("**PROMPT TASK:** ", template)

    url = st.text_input("**Enter the URL**", "")
    tone = st.multiselect("**Select Tone**", ["Witty", "Professional", "Engaging", "Casual"])

    if st.button("Generate"):
        if not url:
            st.error("Please provide a **URL** before clicking 'Generate'.")
        elif not tone:
            st.error("Please select at least one tone before clicking 'Generate'.")
        else:
            for selected_tone in tone:
                result = template.format(Tone=selected_tone, URL=url)
                st.markdown(f'<div style="background-color: #f5f5f5; padding: 10px; border: 1px solid black; border-radius: 5px;">{result}</div>', unsafe_allow_html=True)

    user_input = st.text_area("**Review :eyes: the draft prompt and make :construction: edits before pasting final prompt below:**", height=125)
    start_button = st.button("Publish :ninja: ")

    if start_button:
        prompt = [
            {"role": "system", "content": "You are name is Timmy, a business reporter for the Wall Street Journal."},
            {"role": "user", "content": user_input}
        ]

        st.write("Generating the magic...")
        result = generate_response(prompt, openai_key)
        if result:
            st.write("**Article :memo: Draft**:")
            st.write(result)
            word_count = len(result.split())
            st.write("Word Count: ", word_count)

            # Generate .doc file and create download link
            generate_docx(result, "article_draft.docx")
            with open("article_draft.docx", "rb") as file:
                btn = st.download_button(
                    "Download Article Draft as .docx",
                    file,
                    "article_draft.docx",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )

if __name__ == "__main__":
    main()
