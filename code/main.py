import pandas as pd
import matplotlib.pyplot as plt
import csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def get_data(categories, file_name):
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader if float(row['G']) >= 160]
    
    requested_data = [[float(row[category]) for row in rows] for category in categories]

    return requested_data

def get_2024_data(file_name):
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)  
        
        requested_data = [[], [], [], []]

        for i, row in enumerate(reader):
            if i >= 30:  
                break
            requested_data[0].append(row["Team"])
            requested_data[1].append(row["W"])
            requested_data[2].append(row["OBP"])
            requested_data[3].append(row["ERA"])
        return requested_data

def create_model(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    lr = LinearRegression()
    lr.fit(x_train, y_train)

    # Predict the score
    print(f'Model Score: {lr.score(x_test, y_test)}')

    return lr

def predict(model, stat1, stat2):
    x_df = pd.DataFrame([[stat1, stat2]], columns = ['x1', 'x2'])
    prediction = model.predict(x_df)
    return prediction

if __name__ == '__main__':

    # Replace with the file path for the csv file
    csv_file = ''

    categories = ['OBP', 'ERA', 'W']
    data = get_data(categories, csv_file)
    x = pd.DataFrame({
        'x1': data[0],
        'x2': data[1]
    })
    y = pd.DataFrame({'y': data[2]})

    model = create_model(x, y)

    mlb_2024 = get_2024_data(csv_file)    
    count = 0
    while count < 30:
        prediciton = predict(model, mlb_2024[2][count], mlb_2024[3][count])
        print(f'{mlb_2024[0][count]}: Predicted: {prediciton}, Actual: {mlb_2024[1][count]}')
        count += 1
