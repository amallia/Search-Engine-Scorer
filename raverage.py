import pandas as pd
import numpy as np
import glob, os

def file_list():
    '''
    Shows the output-* files from the current directory
    :return: the list of namefiles
    '''
    lst = []
    os.chdir(".")
    for file in glob.glob("output-*"):
        lst.append(file)
    return lst

def save_to_tsv(header, filename, opt="w"):
    """
    Apends the list "header" to the file filename.txt.
    This is a tsv, so each element of the list is
    separated by a tab in the file
    :param header: list of elements
    :param filename: name of the file
    :param opt: w is write new file, a is append
    :return: nothing
    """
    with open(filename, opt) as f:
        f.write("\t".join(header))
        f.write("\n")

def mean_r_precision(scorer_file, truth_file):
    '''
    Calculates the mean r precision for scorer file and ground truth
    :param scorer_file: filename of the scorer tsv
    :param truth_file:  filename of the ground truth tsv
    :return: the average R-Precision
    '''
    scorer = pd.read_csv(scorer_file, sep="\t")
    truth = pd.read_csv(truth_file, sep="\t")

    # Number of queries IDs
    max_q_id = truth["Query_id"].values[-1]

    precision = []
    for i in range(1, max_q_id + 1):
        # Get relevant documents for query i
        set_docs_truth = set(truth.loc[truth['Query_id'] == i]["Relevant_Doc_id"].values)
        # get the toal number
        R = len(set_docs_truth)

        # Get the top R documents from the score file
        set_docs_scorer = set(scorer.loc[scorer['Query_ID'] == i]["Doc_ID"].values[:R])

        # find the intersection size
        r = len(set_docs_truth.intersection(set_docs_scorer))

        # calculate the precision (R=0 happens when the query ID is not in truth_file)
        if R != 0:
            precision.append(r/R)
    return(np.mean(precision))


# Create new tsv
header = ["Stemmer", "Scorer", "Field", "Average-R-Precision"]

# Filename of the output
filename = "collection1.tsv"

# Create a new file with the header
save_to_tsv(header, filename)

# Ground truth file
truth_file = "Cranfield_DATASET/cran_Ground_Truth.tsv"

# List all the output files
files_name = file_list()
i_max = len(files_name)
i = 0

# Calculate Average R-precision for each scorer file
print("Calculating the Average R-Precision:\n")
for scorer_file in files_name:
    i += 1
    m = mean_r_precision(scorer_file, truth_file)
    info = scorer_file.replace("output-","").replace(".tsv","").split("-") + [str(m)]
    save_to_tsv(info, filename, "a")
    print("[" + str(i) + "/" +  str(i_max) +"] " + scorer_file , round(float(info[-1]),2))
print("\nDone!!")
