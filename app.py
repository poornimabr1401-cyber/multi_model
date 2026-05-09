import streamlit as st
from googletrans import Translator
from PIL import Image
import pytesseract
import json
from datetime import datetime

st.set_page_config(
    page_title="Multi-Modal Translator Studio",
    layout="wide"
)

st.title("🌍 Multi-Modal Translator Studio")

translator = Translator()


languages = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}


menu = st.sidebar.selectbox(
    "Select Mode",
    [
        "Text Translator",
        "Image Translator",
        "History"
    ]
)


def save_history(original, translated, lang):

    data = {
        "time": str(datetime.now()),
        "original_text": original,
        "translated_text": translated,
        "language": lang
    }

    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append(data)

    with open("history.json", "w") as f:
        json.dump(history, f, indent=4)


if menu == "Text Translator":

    st.header("📝 Text Translator")

    text = st.text_area("Enter Text")

    lang = st.selectbox(
        "Select Language",
        list(languages.keys())
    )

    if st.button("Translate"):

        if text != "":

            translated = translator.translate(
                text,
                dest=languages[lang]
            ).text

            st.success("Translation Completed")

            st.subheader("Translated Text")
            st.write(translated)

            save_history(text, translated, lang)

            st.download_button(
                "Download Translation",
                translated,
                file_name="translated.txt"
            )

        else:
            st.warning("Please enter some text")


elif menu == "Image Translator":

    st.header("🖼️ Image Translator")

    uploaded_image = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"]
    )

    lang = st.selectbox(
        "Translate To",
        list(languages.keys())
    )

    if uploaded_image is not None:

        image = Image.open(uploaded_image)

        st.image(image, caption="Uploaded Image")

        if st.button("Extract & Translate"):

            extracted_text = pytesseract.image_to_string(image)

            translated = translator.translate(
                extracted_text,
                dest=languages[lang]
            ).text

            st.subheader("Extracted Text")
            st.write(extracted_text)

            st.subheader("Translated Text")
            st.write(translated)

            save_history(extracted_text, translated, lang)

            st.download_button(
                "Download Translation",
                translated,
                file_name="image_translation.txt"
            )


elif menu == "History":

    st.header("📜 Translation History")

    try:
        with open("history.json", "r") as f:
            history = json.load(f)

        if len(history) == 0:
            st.info("No History Available")

        else:

            for item in reversed(history):

                st.subheader(item["time"])

                st.write("Original Text:")
                st.write(item["original_text"])

                st.write("Translated Text:")
                st.write(item["translated_text"])

                st.write("Language:")
                st.write(item["language"])

                st.markdown("---")

    except:
        st.warning("No History File Found")
