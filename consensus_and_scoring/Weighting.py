import numpy as np
import pandas as pd
import os


def launch_Weighting(directory, reporting = False):
    print("WEIGHTING STARTING")
    iaaFiles = []
    for root, dir, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv') and 'Dep' in file:
                print('gotaFile', file)
                iaaFiles.append(directory+'/'+file)
    weight_list = []
    for f in iaaFiles:
        weight = weighting_alg(f, './config/weight_key.csv', './config/weight_key_scaling_guide.csv', directory,reporting=reporting)
        weight_list.append(weight)
    weights = pd.concat(weight_list)
    return weights

def weighting_alg(IAA_csv_file, credibility_weights_csv_file, weight_scale_csv, directory = './', reporting = False):

    IAA_csv = pd.read_csv(IAA_csv_file)
    #IndexError when the csv is empty
    try:
        IAA_csv_schema_name = IAA_csv.namespace.iloc[0]
    except IndexError:
        if IAA_csv.shape[0]<1:
            return
        else:
            print(len(IAA_csv))
            print(IAA_csv)
            raise Exception('EricIsAnIdiotError')

    print('schemnam',IAA_csv_schema_name)
    if "uage" in IAA_csv_schema_name:
        IAA_csv_schema_type = "Language"
    elif "Reason" in IAA_csv_schema_name:
        IAA_csv_schema_type = "Reasoning"
    elif "Evidence" in IAA_csv_schema_name:
        IAA_csv_schema_type = "Evidence"
    elif "Probability" in IAA_csv_schema_name:
        IAA_csv_schema_type = "Probability"
    elif 'olistic' in IAA_csv_schema_name:
        IAA_csv_schema_type = "Holistic"
    else:
        print("unweighted IAA", IAA_csv_file, "aborting")
        return
    print("WEIGHINGWITHSCHEMA", IAA_csv_schema_type, IAA_csv_file)

    IAA_csv = IAA_csv.rename(columns={ "question_Number": "Question_Number", 'agreed_Answer': 'Answer_Number'})
    IAA_csv['Schema'] = IAA_csv_schema_type
    credibility_weights_csv = pd.read_csv(credibility_weights_csv_file)
    weight_scale_table = pd.read_csv(weight_scale_csv)

    IAA_csv["Question_Number"] = IAA_csv["Question_Number"].apply(int)

    IAA_csv['Answer_Number'] = IAA_csv['Answer_Number'].apply(convertToInt)
    IAA_csv = IAA_csv.loc[IAA_csv.Answer_Number != -1]
    for_visualization = pd.DataFrame()
    #uncomment when we want to scale question scores based on answers to other questions
    for task in np.unique(IAA_csv['source_task_uuid']):
        task_IAA = IAA_csv[IAA_csv['source_task_uuid'] == task]
        scaled_cred_weights = scale_weights_csv(credibility_weights_csv, weight_scale_table, task_IAA,
                                                    IAA_csv_schema_type)

    new_csv = pd.merge(scaled_cred_weights, IAA_csv, on =["Schema", "Question_Number", 'Answer_Number'])

    points = new_csv["Point_Recommendation"] * new_csv["agreement_score"]
    new_csv = new_csv.assign(agreement_adjusted_points = points)
    for_visualization = for_visualization.append(new_csv)

    for_visualization['schema'] = pd.Series(IAA_csv_schema_type for i in range(len(for_visualization['article_sha256'])+1))
    for_visualization = for_visualization.loc[:, ~for_visualization.columns.duplicated()]
    if reporting:
        out_file = directory+"/Point_recs_"+IAA_csv_schema_type+".csv"
        print(out_file)
        for_visualization.to_csv(out_file, encoding = 'utf-8')
    return for_visualization

def weighted_q6(num):
    if num >= 160:
        score = 0
    elif 150 <= num < 160:
        score = 0.5
    elif 100 <= num <150:
        score = 2
    elif 50 <= num <100:
        score = 3
    elif num < 50:
        score = 4
    else:
        score = 5
    return score

def scale_weights_csv(weight_df, scale_df, iaa_df, schema):
    '''

    :param weight_df: weight_key
    :param scale_df: weight_scale_key
    :return: scaled weights dataframe
    '''
    if schema not in scale_df['if_schema']:
        return weight_df
    weight_df = weight_df[weight_df['Schema'] == schema]
    scale_df = scale_df[scale_df['if_schema'==schema]]
    scaled = weight_df
    for a in scale_df['if_ans_uuid']:
        #Gotta make this not be uuid, not stable enough, for now its fine cuase this isn't used
        if a in iaa_df['answer_uuid']:
            row = iaa_df[iaa_df['answer_uuid' == a]]
            #guaranteed to only happen once
            q = int(row['question_Number'].iloc[0])
            a = convertToInt(row['agreed_Answer'])
            mulrow = scale_df[scale_df['if_ans_uuid'] == a]
            mul = mulrow['mult'].iloc[0]
            scaled.loc[['Question_Number' == q, 'Answer_Number' == a, ['Point_Recommendation']]] = \
                scaled.loc[['Question_Number' == q, 'Answer_Number' == a, ['Point_Recommendation']]]*mul
    return scaled

def convertToInt(string):
    try:
        out = int(string)
        return out
    except:
        return -1

if __name__ == '__main__':
        launch_Weighting('../data/out_scoring/')
