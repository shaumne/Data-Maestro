# Data-Maestro
This Flask app is designed to collect news headlines from multiple sources based on specified keywords and generate a short summary based on other user-defined criteria.

### Installation
- Clone this repository to your local machine.
- Install the required packages by running pip install -r requirements.txt in your terminal.
- Create an OpenAI API key here and replace <your-api-key-here> in NewsBriefCompiler_KWFilter.py with your actual key.

### Usage
- Run  `pip install -r requirements.txt`
- Run the app by running python BriefApp.py in your terminal.
- Go to http://localhost:5000/ in your web browser.
- Enter your desired keywords, political view, challenge/reinforce, tone, profession, and favourite artist.
- Click the "Generate Summary" button to see your personalized summary.

### Files
- BriefApp.py: The main Flask app file.
- NewsBriefCompiler_KWFilter.py: The script that collects news headlines and generates the summary.
- template/index.html: The HTML file for the homepage.
- template/summary.html: The HTML file for the summary page.

### Credits
This app was created by shaumne with the help of the following resources:

- Flask: https://flask.palletsprojects.com/en/2.1.x/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- OpenAI API: https://beta.openai.com/docs/api-reference/introduction