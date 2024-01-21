import sys
import pandas as pd

def topsis(input_file, weights, impacts, result_file):
    try:
        
        df = pd.read_csv(input_file)

        data = df.iloc[:, 1:].values

        weights = list(map(int, weights.split(',')))
        impacts = impacts.split(',')

        if len(weights) != len(data[0]) or len(impacts) != len(data[0]):
            raise ValueError("Number of weights, impacts, and columns must be the same.")
        
        if not all(isinstance(val, (int, float)) for row in data for val in row):
            raise ValueError("Input file must contain numeric values only.")
        
        if not all(impact in ['+', '-'] for impact in impacts):
            raise ValueError("Impacts must be either +ve or -ve.")

        normalized_data = data / ((data ** 2).sum(axis=0) ** 0.5)

        weighted_normalized_data = normalized_data * weights

        ideal_best = weighted_normalized_data.max(axis=0)
        ideal_worst = weighted_normalized_data.min(axis=0)

        separation_plus = ((weighted_normalized_data - ideal_best) ** 2).sum(axis=1) ** 0.5
        separation_minus = ((weighted_normalized_data - ideal_worst) ** 2).sum(axis=1) ** 0.5

        topsis_score = separation_minus / (separation_minus + separation_plus)

        df['Topsis Score'] = topsis_score
        df['Rank'] = df['Topsis Score'].rank(ascending=False)

        df.to_csv(result_file, index=False)
        
        print(f"Result saved to {result_file}")

    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "_main_":
    if len(sys.argv) != 5:
        print("Usage: python program.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
    else:
        input_file = sys.argv[1]
        weights = sys.argv[2]
        impacts = sys.argv[3]
        result_file = sys.argv[4]

        topsis(input_file, weights, impacts, result_file)

