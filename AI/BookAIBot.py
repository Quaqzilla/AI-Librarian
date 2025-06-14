import warnings
from crewai import Crew, Task, Agent
from crewai_tools import FirecrawlSearchTool
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

load_dotenv()

book_search = FirecrawlSearchTool()

#Create the Agents
books_agent = Agent(
    role = "Book Searcher",
    goal = "Find well rated books based on the genre and price",
    backstory= "I specialize in discovering well-rated books that are based on a specific genre at a good price",
    tools= [book_search],
    allow_delegation= False,
)

summary_agent = Agent(
    role= "Book Consultant",
    goal="Create a clear list of book recommendations based on a genre",
    backstory="I specialize in translating complex data into a more clear response that save a readers time and money",
    allow_delegation= False,
)

#Define the tasts for the Agents
search_task = Task(
    description= (
        "Search for {book_genre} books with a minimum rating of {rating}"
    ),
    expected_output=
    """ 
        Here are three highly rated finance books that have stood the test of time:

        1.The Intelligent Investor by Benjamin Graham – A classic on value investing, this book teaches principles that Warren Buffett himself has praised.

        2.One Up On Wall Street by Peter Lynch – Offers insights on how everyday investors can identify winning stocks before Wall Street catches on.

        3.A Random Walk Down Wall Street by Burton G. Malkiel – Explores different investment strategies and argues for the efficiency of markets.

        These books provide a solid foundation for understanding financial markets and investment strategies. 
    """,

    agent= books_agent,
)

selections_task = Task(
    description="Analyze the different book options and recommend the best",

    expected_output=
    """
        Here is a list of the books I recommend:

        1.The Intelligent Investor by Benjamin Graham This book is a cornerstone of value investing. 
          Graham emphasizes the importance of analyzing companies based on their intrinsic value rather
          than market speculation. He introduces concepts like Mr. Market, a metaphor for the stock 
          market’s irrational behavior, and the margin of safety, which helps investors minimize risk.
          If you're interested in long-term investing strategies, this book is a must-read.

        2.One Up On Wall Street by Peter Lynch Lynch, a legendary fund manager, shares his philosophy 
          that individual investors can outperform professionals by spotting promising companies early. 
          He encourages readers to invest in businesses they understand and introduces categories like 
          stalwarts, fast growers, and turnarounds to classify stocks. His practical approach makes this 
          book ideal for those looking to develop a keen eye for stock picking.

        3.A Random Walk Down Wall Street by Burton G. Malkiel This book argues that stock prices follow 
          a random pattern, making it difficult to consistently beat the market. Malkiel advocates for 
          passive investing through index funds rather than trying to time the market. He also covers 
          behavioral finance, explaining how psychological biases affect investment decisions. If you're 
          interested in efficient market theory and long-term wealth-building, this book provides valuable
          insights.
    """,

    agent= summary_agent,

)

#Assemble the Crew with agents and tasks
crew = Crew(
    agents=[books_agent, summary_agent],
    tasks= [search_task, selections_task],
    verbose= True,
)

#Code execution
if __name__ == "__main__":
    print("Hi I am the AI Librarian\n")
    genre = input("Enter the genre of the books you are interested in: ")
    rate = int(input("Enter the rating of the book"))

    output = crew.kickoff(
        inputs={
            "book_genre": genre,
            "rating": rate,
        }
    )

    print(output)