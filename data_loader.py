import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Example for testing (outside Streamlit):
if __name__ == "__main__":
    data = load_data('./dataset/test.csv')
    print(data.head())
