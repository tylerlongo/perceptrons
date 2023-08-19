import requests
from bs4 import BeautifulSoup
import numpy as np
from logreg import LogisticRegression


# Initialize a 2D list to store the table data
data = []

# URL of the webpage containing the table

nums = [11, 5, 6, 31, 10, 38, 42]
yrs = [yr for yr in range(2022, 2024)]
type = {"Daytona": "ss",
        "Talladega": "ss",
        "Atlanta": "ss",
        "Sonoma": "rc",
        "Watkins Glen": "rc",
        "Charlotte Roval": "rc",
        "COTA": "rc",
        "Road America": "rc",
        "Indy Road Course": "rc",
        "Chicago Street": "rc",
        "Richmond": "s",
        "Phoenix": "s",
        "Martinsville": "s",
        "Charlotte": "s",
        "Texas": "s",
        "Kansas": "s",
        "Dover": "s",
        "Bristol": "s",
        "New Hampshire": "s",
        "Pocono": "s",
        "Las Vegas": "s",
        "Michigan": "s",
        "Atlanta": "s",
        "Darlington": "s",
        "California (Auto Club)": "s",
        "Homestead": "s",
        "Indianapolis": "s",
        "Nashville": "s",
        "Bristol Dirt": "s",
        "Gateway (WWT)": "s"}

for num in nums:

    finishes = []
    ssfins = []
    rcfins = []
    sfins = []

    for yr in yrs:
        url = "https://www.driveraverages.com/nascar/numberyear.php?carno_id=" + str(num) + "&yr_id=" + str(yr)

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")
            
        # Find the table containing the data
        table = soup.find("table")

        # Loop through each row in the table
        rownum = 0
        for row in table.find_all("tr"):
            if rownum < 5:
                rownum += 1
            else:
                cells = row.find_all(["th", "td"])
                index = cells[3]
                if not index.get_text(strip=True) == "":
                    races = len(finishes)
                    if races > 0:
                        q1 = np.percentile(finishes, 25)
                        med = np.median(finishes)
                        q3 = np.percentile(finishes, 75)
                    finish = int(cells[6].get_text(strip=True))
                    finishes.append(finish)
                    if yr == 2023:
                        week = []
                        start = int(cells[7].get_text(strip=True))
                        track = cells[5].get_text(strip=True)
                        week.append(start)
                        week.append(q1)
                        week.append(med)
                        week.append(q3)
                        week.append(finish)
                        data.append(week)

# Splitting data into features (X) and labels (y)
inputs = np.array(data)[:, :-1]
results = np.array(data)[:, -1]
outputs = []
for result in results:
    if result > 15:
        outputs.append(0)
    else:
        outputs.append(1)


# Creating and training the Logistic Regression model
model = LogisticRegression()
model.fit(inputs, outputs)

# New point to classify
new_point = np.array([[30, 20, 25, 30]])

# Predicting the probability of each class for the new point
prediction = model.predict_prob(new_point)

print("Predicted Probabilities:", prediction)