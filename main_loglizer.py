#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from loglizer import InvariantsMiner, PCA, IsolationForest, OneClassSVM, LogClustering, LR
from loglizer import dataloader, preprocessing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", metavar="DIR", help="output directory")
    parser.add_argument("--dataset_name", help="which dataset to use")
    parser.add_argument('--baselines', type=str, help='options: im pca iforest svm logcluster lr')

    args = parser.parse_args()
    print("select baselines", args)

    selected_baselines = args.baselines.split('_')

    ouput_dir = os.path.expanduser(args.output_dir + args.dataset_name + "/")
    (x_train, y_train), (x_test, y_test) = dataloader.load_data(data_dir=ouput_dir)

    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train)
    x_test = feature_extractor.transform(x_test)

    if 'im' in selected_baselines:
        print("="*20 + " Model: InvariantsMiner " + "="*20)
        epsilon = 0.5  # threshold for estimating invariant space
        model = InvariantsMiner(epsilon=epsilon)
        model.fit(x_train)
        print('Train validation:')
        precision, recall, f1 = model.evaluate(x_train, y_train)
        print('Test validation:')
        precision, recall, f1 = model.evaluate(x_test, y_test)

    if 'pca' in selected_baselines:
        print("="*20 + " Model: PCA " + "="*20)
        model = PCA(n_components=0.95, threshold=50, c_alpha=3.2905)
        model.fit(x_train)
        print('Train validation:')
        precision, recall, f1 = model.evaluate(x_train, y_train)
        print('Test validation:')
        precision, recall, f1 = model.evaluate(x_test, y_test)

    if 'iforest' in selected_baselines:
        print("="*20 + " Model: IsolationForest " + "="*20)
        model = IsolationForest(n_estimators=100, max_samples='auto', contamination='auto', random_state=88)
        model.fit(x_train)
        print('Train validation:')
        precision, recall, f1 = model.evaluate(x_train, y_train)
        print('Test validation:')
        precision, recall, f1 = model.evaluate(x_test, y_test)

    if 'svm' in selected_baselines:
        print("="*20 + " Model: SVM " + "="*20)
        model = OneClassSVM()
        model.fit(x_train, y_train)
        print('Train validation:')
        precision, recall, f1 = model.evaluate(x_train, y_train)
        print('Test validation:')
        precision, recall, f1 = model.evaluate(x_test, y_test)

    if 'logcluster' in selected_baselines:
        print("="*20 + " Model: LogClustering " + "="*20)
        max_dist = 0.3  # the threshold to stop the clustering process
        anomaly_threshold = 0.3  # the threshold for anomaly detection
        model = LogClustering(max_dist=max_dist, anomaly_threshold=anomaly_threshold)
        model.fit(x_train[y_train == 0, :])  # Use only normal samples for training
        print('Train validation:')
        precision, recall, f1 = model.evaluate(x_train, y_train)
        print('Test validation:')
        precision, recall, f1 = model.evaluate(x_test, y_test)

    if 'lr' in selected_baselines:
        print("="*20 + " Model: LR " + "="*20)
        model = LR()
        model.fit(x_train, y_train)
        print('Train validation:')
        precision, recall, f1 = model.evaluate(x_train, y_train)
        print('Test validation:')
        precision, recall, f1 = model.evaluate(x_test, y_test)


if __name__ == "__main__":
    main()
