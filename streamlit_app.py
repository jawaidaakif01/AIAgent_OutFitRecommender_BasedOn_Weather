import streamlit as st

from main import agent

st.set_page_config(page_title="Outfit Recommender", page_icon="🧥")

st.title("🧥 Outfit Recommender")
st.caption("Tell it where you're going and for how long — it checks the weather and suggests what to wear.")

user_input = st.text_area(
    "Describe your trip",
    placeholder="e.g. I'm going on a 6-hour hike in Ramgarh Cantt, Jharkhand tomorrow morning.",
    height=100,
)

if st.button("Get outfit recommendation", type="primary"):
    if not user_input.strip():
        st.warning("Please describe your trip first.")
    else:
        with st.spinner("Checking the forecast and picking an outfit..."):
            try:
                result = agent.invoke({
                    "messages": [{"role": "user", "content": user_input}]
                })
                structured = result["structured_response"]

                st.subheader("Weather forecast")
                st.write(structured.weather_forecast_string)

                st.subheader("Recommended outfit")
                st.markdown(structured.agent_recommendation)
            except Exception as e:
                st.error(f"Something went wrong: {e}")