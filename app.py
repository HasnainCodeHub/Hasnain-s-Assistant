from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from dotenv import load_dotenv
import streamlit as st
from googlesearch import search
import os
import requests


# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# =========================================TOOLS=======================================================


#============INTRO===============
@tool
def intro(input_str: str = "") -> str:
    """
    Provide Hasnain's introduction.

    Args:
        input_str (str): Optional input string.

    Returns:
        str: Hasnain's introduction.

    Example:
        >>> intro()
        "Hasnain Ali is a skilled web developer and programmer..."
    """
    print("Tool Message: Introduction Tool is Called!")
    print("=" * 40)
    return (
        """Hasnain Ali is a skilled web developer and programmer with a passion for creating dynamic, user-focused projects.
        Here is His LinkedIn Profile: https://www.linkedin.com/in/hasnain-ali-developer/ 
        His portfolio features innovative Python projects and AI solutions, including a chatbot built with LangChain and Google Gemini LLM.
        https://my-portfolio-next-js-7olh.vercel.app/
        He is exploring Agentic AI and intelligent agents, driving advancements in automation and artificial intelligence."""
    )



#============CREATOR===============





@tool
def creator(input_str: str = "") -> str:
    """
    Provide information about the tool creator.

    Args:
        input_str (str): Optional input string to customize the message.

    Returns:
        str: Information about the developer.

    Example:
        >>> creator()
        "I am a Chatbot Agent Developed By Hasnain Ali..."
    """
    print("Tool Message: Creator Details Tool is Called!")
    print("=" * 40)
    return (
        """I am a Chatbot Agent Developed By Hasnain Ali.
        If you want to know more about Hasnain Ali, just ask!
        """
    )


#============google_search_tool===============



@tool
def google_search_tool(query: str, num_results: int = 5):
    """
    Perform a Google search for a given query and return the top results.

    Args:
        query (str): The search query.
        num_results (int): Number of search results to return. Default is 5.

    Returns:
        list: A list of URLs for the top search results.
    """
    print("Tool Message: Google Search Tool is Called!")
    print("=" * 40)
    try:
        # Perform the search
        results = search(query, num_results=num_results)
        return list(results)
    except Exception as e:
        return f"An error occurred during the search: {e}"



#============goodbye===============



@tool
def goodbye(input_str: str = "") -> str:
    """
    Stop the agent and provide a farewell message.

    Args:
        input_str (str): Optional input string.

    Returns:
        str: Farewell message.

    Example:
        >>> goodbye()
        "Goodbye! Thanks for your visit. Come again!"
    """
    print("Tool Message: Goodbye Tool is Called!")
    print("=" * 40)
    return "Goodbye! Thanks for your visit. Come again!"



#============get_latest_news===============


@tool(parse_docstring=True)
def get_latest_news(topic: str) -> str:
    """
    Fetches the latest news for a given topic.

    Args:
        topic (str): The topic to search for news articles.

    Returns:
        str: A formatted string containing the tool name, the latest news titles, and their respective links.

    Example:
        get_latest_news("Technology")
    """
    api_key = '85fb755af35f41fbb3b79921facffa5f'  # Replace with your actual API key
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"
    print("Tool Message: News Tool is Called!")
    print("=" * 40)
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get('articles'):
            articles = data['articles']
            result = f"Tool used: get_latest_news\n get_latest_news tool is used \nHere are the latest news articles related to {topic}:\n"

            for article in articles[:10]:  # Limiting to 5 articles
                title = article['title']
                url = article['url']
                result += f"- {title}: {url}\n"

            return result
        else:
            return f"Error: Could not fetch news for {topic}. Reason: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error: Unable to fetch news. Details: {str(e)}"





#============give_social_accounts===============



@tool
def give_social_accounts(input_str: str = "") -> str:
    """
    Provide Hasnain's social account details.

    Args:
        input_str (str): Optional input string.

    Returns:
        str: Links to Hasnain's social accounts.

    Example:
        >>> give_social_accounts()
        "Hasnain's LinkedIn: ... \nHasnain's GitHub: ..."
    """
    print("Tool Message: Contact Details Tool is Called!")
    print("=" * 40)
    return (
        """
        Hasnain's LinkedIn: https://www.linkedin.com/in/hasnain-ali-developer/ \n
        Hasnain's GitHub: https://github.com/HasnainCodeHub \n
        Hasnain's Instagram: https://www.instagram.com/i_hasnainaliofficial/ \n
        Hasnain's Facebook Profile: https://www.facebook.com/hasnainazeem.hasnainazeem.1 \n
        Hasnain's Email Address: husnainazeem048@gmail.com \n
        Hasnain's Contact Number: 03702537927
        """
    )





#============Give Stock Price===============


@tool
def get_stock_price(symbol: str) -> str:
    """Fetches the current stock price of a company based on its stock symbol using the Polygon API.

    Args:
        symbol (str): The stock symbol of the company (e.g., 'AAPL' for Apple, 'GOOGL' for Google).

    Returns:
        str: A message containing the current stock price of the company.

    Raises:
        HTTPError: If the HTTP request to the stock API fails (e.g., 404 or 500 status).
        RequestException: If there is an issue with the request itself (e.g., connection error).
        Exception: For any other unexpected errors during the execution of the function.

    """
    api_key =  '8pAMt7yDR03RyrywzLsMZ7gevHSC0GAU'  # Replace this with your actual secret API key from Polygon
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev"  # Polygon endpoint for previous close price
    
    print("Tool Message: Stock Price Tool is Called!")
    print("=" * 40)


    try:
        # Send a GET request with the API key
        response = requests.get(url, params={'apiKey': api_key})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

        # Assuming the data contains 'close' in the response for the last closing price
        data = response.json()
        price = data.get('results', [{}])[0].get('c')  # 'c' is the closing price

        if price:
            return f"Tool used: get_stock_price\n get_stock_price tool is used to find The current price of {symbol} is ${price}"
        else:
            return f"Error: Could not retrieve stock data for {symbol}.\nTool used: get_stock_price"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}\nTool used: get_stock_price"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}\nTool used: get_stock_price"
    except Exception as err:
        return f"An unexpected error occurred: {err}\nTool used: get_stock_price"



#===========Convert Currency=============

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str, api_key: str) -> float:
    """
    Convert a given amount from one currency to another using a currency exchange API.

    Parameters:
        amount (float): The amount of money to convert.
        from_currency (str): The currency code of the source currency (e.g., "USD").
        to_currency (str): The currency code of the target currency (e.g., "EUR").
        api_key (str): Your API key for the currency exchange API.

    Returns:
        float: The converted amount in the target currency.

    Raises:
        ValueError: If the API request fails or the response contains an error.
    """
    url = f"https://openexchangerates.org/api/latest.json"

    # PLACE YOUR API KEY HERE
    params = {
        "app_id": 'fa89393965414a19b5e1a50755259b6c'  # <-- REPLACE 'api_key' WITH YOUR API KEY
    }
    print("Tool Message: Currency Converter Tool is Called!")
    print("=" * 40)

    try:
        # Fetch exchange rates
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Check if the currencies exist in the data
        rates = data.get("rates", {})
        if from_currency not in rates or to_currency not in rates:
            raise ValueError(f"Currency code '{from_currency}' or '{to_currency}' not found.")

        # Perform conversion
        from_rate = rates[from_currency]
        to_rate = rates[to_currency]
        converted_amount = (amount / from_rate) * to_rate

        return round(converted_amount, 2)

    except requests.RequestException as e:
        raise ValueError(f"API request failed: {str(e)}")

#================Get Weather==================

@tool
def get_weather(city: str) -> str:
    """
    Fetches the current weather for a given city using the OpenWeatherMap API.

    Args:
        city (str): Name of the city to get weather for.

    Returns:
        str: Weather information or error message.
    """
    api_key = "049048adef5f0ac4aa3012b93db79b78"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Extract weather details
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Format the result
        return (
            f"Weather in {city_name}:\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {weather_description.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

    except requests.exceptions.HTTPError:
        return "City not found. Please check the city name."
    except Exception as e:
        return f"An error occurred: {e}"








tools = [
    intro,
    google_search_tool,
    convert_currency,
    get_stock_price,
    get_latest_news,
    creator,
    goodbye,
    give_social_accounts,
    get_weather
]




# Initialize LLM
llm = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.0-flash-exp", verbose=True)

# =========================================AGENT=======================================================
# Initialize the agent
# System Message
SYSTEM_MESSAGE = (
    "You are an AI-based calculator agent designed exclusively to operate within the scope of the provided tools. "
    "These tools include operations like addition, subtraction, multiplication, division, percentage calculations, introductions, "
    "creator information, contact details, and goodbye messages. "
    "If you receive a query or action outside the capabilities of these tools, respond politely and clearly, stating that the requested action "
    "is beyond your functionality. Avoid providing speculative or unsupported responses."
)

# Initialize the agent with system message
agent = initialize_agent(
    tools,                         # Provide the tools
    llm,                           # LLM for fallback
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    max_iterations=50,
    system_message=SYSTEM_MESSAGE,  # Add system message to restrict the agent
)

import streamlit as st

# Streamlit App Setup
st.set_page_config(page_title="Hasnain's Coding World", page_icon=":robot:", layout="centered")
st.title("Welcome to Hasnain's Coding World")
st.markdown("<h2 style='color: #4CAF50;'>Empowering Your Digital Journey with Cutting-edge AI Solutions</h2>", unsafe_allow_html=True)

# Suggested Queries
suggested_queries = [
    "Get Me The Current Weather Of Karachi",
    "Get The Current Political News Of Pakistan",
    "5000 Dollor to Pkr",
    "Perform A Google Search And Suggest Me The Best Programming Linkedin Profiles",
    "Current Stock Price Of Tesla",
    "Who is Founder/Developer/Creator?",
    "Give me Hasnain's social accounts.",
    "What technologies does Hasnain use?",
    "Where can I view Hasnain's portfolio?",
    "What is the purpose of this agent?",

]

st.write("### Suggested Queries:")
for query in suggested_queries:
    st.write(f"- {query}")

# Custom Styling for Response
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='background-color: #f1f1f1; padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
# st.write("### Conversation History:")
if "conversation" not in st.session_state:
    st.session_state.conversation = []  # Store user queries and responses

# Display conversation history (Agent responses and user queries)
for query, reply in st.session_state.conversation:
    st.write(f"**Human Message:** {query}")
    st.write(f"**Agent Response:** {reply}")
    st.write("---")
st.markdown("</div>", unsafe_allow_html=True)

# Input box and Button UI (Placed at the bottom)
st.markdown("<hr>", unsafe_allow_html=True)

# Display query input and send button
# Adjust column sizes
col1, col2 = st.columns([4, 1])  
with col1:
    user_query = st.text_input("Enter your query:")
    st.success("You Can Also Matched The Live Searching Manually By Google Search For Satisfaction!")
    
with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Add space between input and button
    if st.button("Ask ➡️"):  # Change the button text to "Ask"
        if user_query.strip():  # Check if input is not empty
            try:
                # Invoke the agent with the user's query
                response = agent.invoke({"input": user_query})
                agent_response = response.get('output', 'No output available')

                # Append the conversation history
                st.session_state.conversation.append((user_query, agent_response))

                # Refresh the app to show the updated conversation
                st.rerun()

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a query to proceed.")

# Sidebar with Social Links and Contact Information
st.sidebar.title("Available Tools ")
tools = [
    ("Introduction Tool", "An AI-powered tool to introduce and engage users with a custom message."),
    ("Google Search", "Search the web for the latest information and results."),
    ("Currency Converter", "Convert currencies with real-time exchange rates."),
    ("Stock Price Checker", "Get the latest stock prices and financial insights."),
    ("Latest News", "Stay updated with the most recent news across various categories."),
    ("Creator Tool", "Create and manage AI models and projects with ease."),
    ("Social Media Accounts", "Share your social media profiles in style."),
    ("Weather Information", "Get the latest weather updates for any location.")
]

    
# Display tools with attractive text
for tool_name, description in tools:
    st.sidebar.markdown(f"### {tool_name}")
    st.sidebar.write(description)
    st.sidebar.write("---")


st.sidebar.markdown("### Connect with Hasnain")
st.sidebar.write("[LinkedIn](https://www.linkedin.com/in/hasnain-ali-developer/)")
st.sidebar.write("[GitHub](https://github.com/HasnainCodeHub)")
st.sidebar.write("[Instagram](https://www.instagram.com/i_hasnainaliofficial/)")
st.sidebar.write("[Facebook](https://www.facebook.com/hasnainazeem.hasnainazeem.1)")
