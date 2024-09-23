import numpy as np
import pandas as pd
import tqdm
import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ai_clinician.modeling.normalization import DataNormalization
from ai_clinician.preprocessing.utils import load_csv
from ai_clinician.preprocessing.gosh_columns import *
from ai_clinician.modeling.gosh_columns import *
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

tqdm.tqdm.pandas()

def save_data_files(dir, MIMICraw, MIMICzs, metadata):
    MIMICraw.to_csv(os.path.join(dir, "MIMICraw.csv"), index=False)
    MIMICzs.to_csv(os.path.join(dir, "MIMICzs.csv"), index=False)
    metadata.to_csv(os.path.join(dir, "metadata.csv"), index=False)

if __name__ == '__main__':

    # Set up argument parser
    parser = argparse.ArgumentParser(description=('Generates a train/test '
            'split of the selected dataset, and generates files labeled '
            '{train|test}/[dataset]raw.npy and {train|test}/[dataset]zs.npy.'))
    parser.add_argument('dataset', type=str, choices=['mimic', 'gosh', 'phoenix'],
                        help='Select the dataset to process: mimic, gosh, or phoenix')
    parser.add_argument('--train-size', dest='train_size', type=float, default=0.8,
                        help='Proportion of data to use in training (default 0.8)')
    parser.add_argument('--outcome', dest='outcome_col', type=str, default='mortality_90d',
                        help='Name of column to use for outcomes (probably "died_in_hosp" or "mortality_90d" [default])')

    args = parser.parse_args()

    # Resolve absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # You can then use args.dataset to determine which dataset to process
    selected_dataset = args.dataset

    # Define input and output directories based on the selected dataset
    if selected_dataset == 'mimic':
        input_dir = 'ai_clinician/implementation/mimic/data/'
        output_dir = 'ai_clinician/implementation/mimic/outputs/'
    elif selected_dataset == 'gosh':
        input_dir = 'ai_clinician/implementation/gosh/data/'
        output_dir = 'ai_clinician/implementation/gosh/outputs/'
    elif selected_dataset == 'phoenix':
        input_dir = 'ai_clinician/implementation/phoenix/data/'
        output_dir = 'ai_clinician/implementation/phoenix/outputs/'

    # Find sepsis cohort in the mimic dataset
    MIMICtable = load_csv(os.path.join(input_dir, "mimic_dataset.csv"))
    # sepsis_cohort = load_csv(os.path.join(in_dir, "sepsis_cohort.csv"))

    # MIMICtable = mdp_data[mdp_data[C_ICUSTAYID].isin(sepsis_cohort[C_ICUSTAYID])].reset_index(drop=True)
    assert args.outcome_col in MIMICtable.columns, "Outcome column '{}' not found in MIMICtable".format(args.outcome_col)

    # find patients who died in ICU during data collection period
    icuuniqueids = MIMICtable[C_ICUSTAYID].unique()
    train_ids, test_ids = train_test_split(icuuniqueids, train_size=args.train_size)
    train_indexes = MIMICtable[MIMICtable[C_ICUSTAYID].isin(train_ids)].index
    test_indexes = MIMICtable[MIMICtable[C_ICUSTAYID].isin(test_ids)].index
    print("Training: {} IDs ({} rows)".format(len(train_ids), len(train_indexes)))
    print("Test: {} IDs ({} rows)".format(len(test_ids), len(test_indexes)))

    MIMICraw = MIMICtable[ALL_FEATURE_COLUMNS]

    print("Proportion of NA values:", MIMICraw.isna().sum() / len(MIMICraw))

    normer = DataNormalization(MIMICtable.iloc[train_indexes])
    MIMICzs_train = normer.transform(MIMICtable.iloc[train_indexes])
    MIMICzs_test = normer.transform(MIMICtable.iloc[test_indexes])

    train_dir = os.path.join(output_dir, "train")
    test_dir = os.path.join(output_dir, "test")
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
        
    metadata = MIMICtable[[C_BLOC, C_ICUSTAYID, args.outcome_col]].rename({args.outcome_col: C_OUTCOME}, axis=1)
    
    # Save files
    print("Saving files")
    normer.save(os.path.join(output_dir, 'normalization.pkl'))
    save_data_files(train_dir,
                    MIMICraw.iloc[train_indexes],
                    MIMICzs_train,
                    metadata.iloc[train_indexes])
    save_data_files(test_dir,
                    MIMICraw.iloc[test_indexes],
                    MIMICzs_test,
                    metadata.iloc[test_indexes])    
    print("Done.")
    