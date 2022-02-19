from collections import Counter
from statistics import median, mean, stdev
import pandas as pd

path_input_csv = 'D:/Documents/PETERCHAN/#myResearch/myResearch_Acne/ECK/acne_grading/result.csv'
path_output_csv = 'D:/Documents/PETERCHAN/#myResearch/myResearch_Acne/ECK/acne_grading/result_label.csv'

def get_label(numbers):
    '''
    : number: list. i.e. (1,2,4,4,3)
    : input: number
    : output: list. i.e. (4)
    '''
    counts = Counter(numbers)
    if counts.most_common(1)[0][1] >= 3:
        return counts.most_common(1)[0][0]
    else:
        return median(numbers)

df = pd.read_csv(path_input_csv, encoding='UTF-8')
df['Label'] = 0
#print(df.head())

for i in range(df.shape[0]):
    df.loc[i, 'Label'] = get_label(list(df.iloc[i, 1:-1]))
df.to_csv(path_output_csv, encoding='UTF-8')

MAE = {}; MSE = {}
for col in df.columns[1:-1]:
    MAE[col] = mean(abs(df[col] - df['Label']))
    MSE[col] = mean((df[col] - df['Label']) ** 2)

print(f'MAE: {MAE}')
print(f'MAE avg: {mean(list(MAE.values())): .3f}, MAE sd: {stdev(list(MAE.values())): .3f}')
print(f'MSE: {MSE}')
print(f'MSE avg: {mean(list(MSE.values())): .3f}, MSE sd: {stdev(list(MSE.values())): .3f}')