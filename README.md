# Outfit Recommender

![Outfit Recommender screenshot](<Project Images/Screenshot%202026-09-11%20114901.png>)

An AI agent that recommends what to wear based on real-time weather forecasts. Tell it where you're going and for how long, and it geocodes the location, pulls an hourly weather forecast, and reasons over the next several hours of conditions to suggest a practical outfit and any extra items to carry.

## How it works

```
User query (free text)
        │
        ▼
  LangChain agent (Gemini)
        │  decides to call the tool
        ▼
  outfit_recommender tool
        │
        ▼
  get_weather_forecast(location, hours)
        │
   ┌────┴─────┐
   ▼          ▼
Nominatim   Open-Meteo
(geocoding) (hourly forecast)
        │
        ▼
  Structured weather JSON returned to the agent
        │
        ▼
  Agent reasons over the forecast and produces:
   - weather_forecast_string (summary)
   - agent_recommendation (outfit + extra items)
```

The agent doesn't need the location or number of hours as separate structured inputs — it extracts them itself from a natural-language description of the trip (e.g. *"I'm going on a 6-hour hike in Ramgarh Cantt, Jharkhand"*).

## Project structure

| File | Purpose |
|---|---|
| `location_extractor.py` | Geocodes a place name into latitude/longitude using OpenStreetMap's Nominatim API. |
| `data_extraction.py` | Fetches the hourly weather forecast for a location from Open-Meteo and returns it as structured data (temperature, humidity, dew point, rain, showers, snowfall, snow depth, precipitation). |
| `main.py` | The core LangChain agent. Wraps the weather fetch as a tool, defines the system prompt and structured output schema, and runs the agent. |
| `streamlit_app.py` | A simple web UI on top of the agent — enter a trip description, get back a weather summary and outfit recommendation. |

## Tech stack

- **Language:** Python
- **Agent framework:** [LangChain](https://python.langchain.com/) (`create_agent`)
- **LLM:** Google Gemini, via `langchain-google-genai`
- **Geocoding:** [Nominatim](https://nominatim.openstreetmap.org/) (OpenStreetMap)
- **Weather data:** [Open-Meteo](https://open-meteo.com/) forecast API
- **UI:** [Streamlit](https://streamlit.io/)
- **Structured output:** Pydantic

## Screenshots

| | |
|---|---|
| ![Screenshot 2](<Project Images/Screenshot%202026-09-11%20114946.png>) | ![Screenshot 3](<Project Images/Screenshot%202026-09-11%20115604.png>) |
| ![Screenshot 4](<Project Images/Screenshot%202026-09-11%20115721.png>) | |

## Setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/jawaidaakif01/AIAgent_OutFitRecommender_BasedOn_Weather.git
cd outfit-recommender
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install langchain langchain-google-genai openmeteo-requests requests-cache retry-requests requests python-dotenv pydantic streamlit
```

### 3. Get a Google Gemini API key

Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Configure environment variables

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_api_key_here
```

## Running the project

### Command line

```bash
python main.py
```

This runs the agent against the hardcoded example prompt in `main.py`'s `if __name__ == "__main__":` block. Edit that prompt to try your own trip description.

### Streamlit web app

```bash
streamlit run streamlit_app.py
```

This opens a browser tab where you can type a trip description, click a button, and see the weather forecast and outfit recommendation rendered on the page.

## Notes

- Weather forecast requests are cached for 1 hour (via `requests_cache`) to avoid redundant API calls for the same location.
- Open-Meteo and Nominatim are both free, keyless APIs, so no additional credentials are needed for the weather/geocoding steps — only the Gemini API key is required.
- The `hours` parameter controls how many hours of forecast data the agent reasons over (default: 6). The agent decides this value itself based on the trip description, or falls back to the default.

## Possible next steps

- Add memory so the agent can adjust recommendations based on past feedback ("it was too cold last time").
- Support multi-day trips.
- Cache/display which tool calls the agent made, for debugging.
