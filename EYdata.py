import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np


def main():

    # os.chdir('../c.Data')
    file = 'EYdata.xlsx'
    raw_data = pd.ExcelFile(file)                                   # read the excel file
    sheets = raw_data.sheet_names                                   # get the names of the sheets
    '''df = raw_data.parse(1)
    header = (df.columns.values[1]).split(',')
    print(header)
    name = header[0]
    print(name)
    compare = header[1]
    print(compare)
    criteria = float(header[2])
    print(criteria)
    target = int(header[3])
    print(target)'''


    combined_data = pd.DataFrame(index=reversed(sheets))            # initialize an empty dataframe to hold results

    for i in reversed(sheets):                                      # loop through each excel sheet
        df = raw_data.parse(i)                                      # get data from current sheet
        columns = df.columns.values                                 # get column names
        limit = len(columns)                                        # find out how many columns there are

        for j in range(1, limit):                                   # loop through each column of current sheet

            num_of_rows = len(df.iloc[:,j])
            skill = df.iloc[:,j]
            consecutive = 0                                         # reset consecutive days to zero

            for k in range(num_of_rows):                            # check each data point in each row the column
                header = (df.columns.values[j]).split(',')
                name = header[0]
                compare =header[1]
                criteria = float(header[2])
                if pd.isnull(skill[k]):
                    consecutive = consecutive
                elif compare == '>':
                    if skill[k] >= criteria:
                        consecutive += 1
                    else:
                        consecutive = 0
                elif compare == '<':
                    if skill[k] <= criteria:
                        consecutive += 1
                    else:
                        consecutive = 0

            combined_data.set_value(i, skill.name, consecutive)     # place number of consecutive days in combined_data df

    # os.chdir('../b.TreatmentPlans/20170228-20171115')

    for obj in combined_data.columns.values:
        headers = obj.split(',')
        name = headers[0]
        compare = headers[1]
        criteria = float(headers[2])
        target = float(headers[3])
        plt.plot(combined_data.index, combined_data[obj], color='k')
        plt.scatter([combined_data.index], combined_data[obj], color='k')
        plt.ylim(-1, 11)
        plt.xlabel('Month')
        plt.ylabel(str('Consecutive Sessions ' + compare + ' ' + str(criteria)))
        plt.title(name)
        plt.minorticks_off()
        plt.axhline(y=target, color='red', linestyle='dashed')
        plt.xticks(np.arange(int(combined_data.index[0]), int(combined_data.index[len(combined_data.index)-1])+1 , 1.0))
        plt.savefig(name)
        plt.show()


if __name__ == '__main__':
    main()
