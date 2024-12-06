import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataFrameProcessor:
    def __init__(self):
        self.df = None
    
    def load_csv(self, file_path):
        """Load a CSV file into a DataFrame"""
        try:
            self.df = pd.read_csv(file_path)
            print(f"Loaded DataFrame with shape: {self.df.shape}")
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def get_basic_info(self):
        """Get basic information about the DataFrame"""
        if self.df is None:
            return "No DataFrame loaded"
        
        info = {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.to_dict(),
            "null_counts": self.df.isnull().sum().to_dict()
        }
        return info
    
    def describe_data(self):
        """Get statistical description of the DataFrame"""
        if self.df is None:
            return "No DataFrame loaded"
        return self.df.describe()
    
    def clean_data(self):
        """Basic data cleaning operations"""
        if self.df is None:
            return "No DataFrame loaded"
        
        # Remove duplicate rows
        initial_rows = len(self.df)
        self.df.drop_duplicates(inplace=True)
        
        # Handle missing values (fill numeric with mean, categorical with mode)
        for column in self.df.columns:
            if self.df[column].dtype in ['int64', 'float64']:
                self.df[column].fillna(self.df[column].mean(), inplace=True)
            else:
                self.df[column].fillna(self.df[column].mode()[0], inplace=True)
        
        print(f"Removed {initial_rows - len(self.df)} duplicate rows")
        print("Filled missing values")
        return "Data cleaning completed"

if __name__ == "__main__":
    # Example usage
    processor = DataFrameProcessor()
    
    # You can use it like this:
    # processor.load_csv("your_file.csv")
    # print(processor.get_basic_info())
    # print(processor.describe_data())
    # processor.clean_data()
