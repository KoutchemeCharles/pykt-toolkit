import time
import numpy as np 
import pandas as pd 
from pykt.preprocess.utils import format_list2str, write_txt


def read_data_from_csv(read_file, write_file, data_split):
    
    # Load information about students sequences 
    dataframe = pd.read_csv(read_file)
    dataframe.timestamp = pd.to_datetime(dataframe.timestamp)
    # Converting to miliseconds 
    dataframe.timestamp = dataframe.timestamp.astype(np.int64) / int(1e6)

    dataframe = dataframe.sort_values(by="timestamp")
    # the data contains also students run in between, 
    # which we need to filter out. We also remove the 
    # submissions to exercises which do not have a maximum score
    dataframe = dataframe[(dataframe.max_score == 100)]
    dataframe = dataframe[(dataframe.score > -1)]

    data = []
    course_ids = [("train", data_split[0]), ("test", data_split[1])]
    for split, course_id in course_ids:
        df = dataframe[dataframe.course_id == course_id].reset_index(drop=True)
        assert not df.empty
        groups = df.groupby("student_id")
        for user_id, user_data in groups:
            # we need to save some specific information
            seq_len = user_data.shape[0]
            seq_question_id = list(user_data.problem_id.values)
            seq_skill_id = list(user_data.concept_list.values)
            seq_answer_result = list((user_data.score == 100).astype(int))
            seq_submission_time = list(user_data.timestamp)
            seq_use_time = ["NA"]
            
            header = [str(user_id), str(seq_len), split]
            information = [
                header, 
                format_list2str(seq_question_id), 
                format_list2str(seq_skill_id), 
                format_list2str(seq_answer_result),
                format_list2str(seq_submission_time),
                seq_use_time
            ]
            
            data.append(information)
            
    write_txt(write_file, data)
       