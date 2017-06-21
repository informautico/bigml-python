# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2015-2017 BigML
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


""" Comparing remote and local predictions

"""
from world import world, setup_module, teardown_module, show_doc
import create_source_steps as source_create
import create_dataset_steps as dataset_create
import create_model_steps as model_create
import create_association_steps as association_create
import create_cluster_steps as cluster_create
import create_anomaly_steps as anomaly_create
import create_prediction_steps as prediction_create
import compare_predictions_steps as prediction_compare
import create_lda_steps as topic_create


class TestComparePrediction(object):

    def setup(self):
        """
            Debug information
        """
        print "\n-------------------\nTests in: %s\n" % __name__

    def teardown(self):
        """
            Debug information
        """
        print "\nEnd of tests in: %s\n-------------------\n" % __name__

    def test_scenario1(self):
        """
            Scenario: Successfully comparing predictions:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a model
                And I wait until the model is ready less than <time_3> secs
                And I create a local model
                When I create a prediction for "<data_input>"
                Then the prediction for "<objective>" is "<prediction>"
                And I create a local prediction for "<data_input>"
                Then the local prediction is "<prediction>"

                Examples:
                | data             | time_1  | time_2 | time_3 | data_input                             | objective | prediction  |

        """
        examples = [
            ['data/iris.csv', '10', '10', '10', '{"petal width": 0.5}', '000004', 'Iris-setosa'],
            ['data/iris.csv', '10', '10', '10', '{"petal length": 6, "petal width": 2}', '000004', 'Iris-virginica'],
            ['data/iris.csv', '10', '10', '10', '{"petal length": 4, "petal width": 1.5}', '000004', 'Iris-versicolor'],
            ['data/iris_sp_chars.csv', '10', '10', '10', '{"pétal.length": 4, "pétal&width\u0000": 1.5}', '000004', 'Iris-versicolor']]
        show_doc(self.test_scenario1, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_model(self)
            model_create.the_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_model(self)
            prediction_create.i_create_a_prediction(self, example[4])
            prediction_create.the_prediction_is(self, example[5], example[6])
            prediction_compare.i_create_a_local_prediction(self, example[4])
            prediction_compare.the_local_prediction_is(self, example[6])

    def test_scenario2(self):
        """
            Scenario: Successfully comparing predictions with text options:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I update the source with params "<options>"
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a model
                And I wait until the model is ready less than <time_3> secs
                And I create a local model
                When I create a prediction for "<data_input>"
                Then the prediction for "<objective>" is "<prediction>"
                And I create a local prediction for "<data_input>"
                Then the local prediction is "<prediction>"

                Examples:
                | data             | time_1  | time_2 | time_3 | options | data_input                             | objective | prediction  |

        """
        examples = [
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": true, "stem_words": true, "use_stopwords": false, "language": "en"}}}}', '{"Message": "Mobile call"}', '000000', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": true, "stem_words": true, "use_stopwords": false, "language": "en"}}}}', '{"Message": "A normal message"}', '000000', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": false, "stem_words": false, "use_stopwords": false, "language": "en"}}}}', '{"Message": "Mobile calls"}', '000000', 'spam'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": false, "stem_words": false, "use_stopwords": false, "language": "en"}}}}', '{"Message": "A normal message"}', '000000', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": false, "stem_words": true, "use_stopwords": true, "language": "en"}}}}', '{"Message": "Mobile call"}', '000000', 'spam'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": false, "stem_words": true, "use_stopwords": true, "language": "en"}}}}', '{"Message": "A normal message"}', '000000', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"token_mode": "full_terms_only", "language": "en"}}}}', '{"Message": "FREE for 1st week! No1 Nokia tone 4 ur mob every week just txt NOKIA to 87077 Get txting and tell ur mates. zed POBox 36504 W45WQ norm150p/tone 16+"}', '000000', 'spam'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"token_mode": "full_terms_only", "language": "en"}}}}', '{"Message": "Ok"}', '000000', 'ham'],
            ['data/movies.csv', '20', '20', '30', '{"fields": {"000007": {"optype": "items", "item_analysis": {"separator": "$"}}}}', '{"genres": "Adventure$Action", "timestamp": 993906291, "occupation": "K-12 student"}', '000009', '3.93064'],
            ['data/text_missing.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"token_mode": "all", "language": "en"}}, "000000": {"optype": "text", "term_analysis": {"token_mode": "all", "language": "en"}}}}', '{}', "000003", 'swap']]
        show_doc(self.test_scenario2, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            source_create.i_update_source_with(self, example[4])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_model(self)
            model_create.the_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_model(self)
            prediction_create.i_create_a_prediction(self, example[5])
            prediction_create.the_prediction_is(self, example[6], example[7])
            prediction_compare.i_create_a_local_prediction(self, example[5])
            prediction_compare.the_local_prediction_is(self, example[7])


    def test_scenario3(self):
        """
            Scenario: Successfully comparing predictions with proportional missing strategy:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a model
                And I wait until the model is ready less than <time_3> secs
                And I create a local model
                When I create a proportional missing strategy prediction for "<data_input>"
                Then the prediction for "<objective>" is "<prediction>"
                And the confidence for the prediction is "<confidence>"
                And I create a proportional missing strategy local prediction for "<data_input>"
                Then the local prediction is "<prediction>"
                And the local prediction's confidence is "<confidence>"

                Examples:
                | data               | time_1  | time_2 | time_3 | data_input           | objective | prediction     | confidence |

        """
        examples = [
            ['data/iris.csv', '10', '10', '10', '{}', '000004', 'Iris-setosa', '0.2629'],
            ['data/grades.csv', '10', '10', '10', '{}', '000005', '68.62224', '27.5358'],
            ['data/grades.csv', '10', '10', '10', '{"Midterm": 20}', '000005', '40.46667', '54.89713'],
            ['data/grades.csv', '10', '10', '10', '{"Midterm": 20, "Tutorial": 90, "TakeHome": 100}', '000005', '28.06', '25.65806']]
        show_doc(self.test_scenario3, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_model(self)
            model_create.the_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_model(self)
            prediction_create.i_create_a_proportional_prediction(self, example[4])
            prediction_create.the_prediction_is(self, example[5], example[6])
            prediction_create.the_confidence_is(self, example[7])
            prediction_compare.i_create_a_proportional_local_prediction(self, example[4])
            prediction_compare.the_local_prediction_is(self, example[6])
            prediction_compare.the_local_prediction_confidence_is(self, example[7])

    def test_scenario4(self):
        """
            Scenario: Successfully comparing predictions with proportional missing strategy for missing_splits models:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a model with missing splits
                And I wait until the model is ready less than <time_3> secs
                And I create a local model
                When I create a proportional missing strategy prediction for "<data_input>"
                Then the prediction for "<objective>" is "<prediction>"
                And the confidence for the prediction is "<confidence>"
                And I create a proportional missing strategy local prediction for "<data_input>"
                Then the local prediction is "<prediction>"
                And the local prediction's confidence is "<confidence>"

                Examples:
                | data               | time_1  | time_2 | time_3 | data_input           | objective | prediction     | confidence |
        """
        examples = [
            ['data/iris_missing2.csv', '10', '10', '10', '{"petal width": 1}', '000004', 'Iris-setosa', '0.8064'],
            ['data/iris_missing2.csv', '10', '10', '10', '{"petal width": 1, "petal length": 4}', '000004', 'Iris-versicolor', '0.7847']]
        show_doc(self.test_scenario4, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_model_with_missing_splits(self)
            model_create.the_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_model(self)
            prediction_create.i_create_a_proportional_prediction(self, example[4])
            prediction_create.the_prediction_is(self, example[5], example[6])
            prediction_create.the_confidence_is(self, example[7])
            prediction_compare.i_create_a_proportional_local_prediction(self, example[4])
            prediction_compare.the_local_prediction_is(self, example[6])
            prediction_compare.the_local_prediction_confidence_is(self, example[7])

    def test_scenario5(self):
        """
            Scenario: Successfully comparing logistic regression predictions:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a logistic regression model
                And I wait until the logistic regression model is ready less than <time_3> secs
                And I create a local logistic regression model
                When I create a logistic regression prediction for "<data_input>"
                Then the logistic regression prediction is "<prediction>"
                And I create a local logistic regression prediction for "<data_input>"
                Then the local logistic regression prediction is "<prediction>"

                Examples:
                | data             | time_1  | time_2 | time_3 | data_input                                                                                 | prediction  |
        """
        examples = [
            ['data/iris.csv', '10', '10', '50', '{"petal width": 0.5, "petal length": 0.5, "sepal width": 0.5, "sepal length": 0.5}', 'Iris-versicolor'],
            ['data/iris.csv', '10', '10', '50', '{"petal width": 2, "petal length": 6, "sepal width": 0.5, "sepal length": 0.5}', 'Iris-versicolor'],
            ['data/iris.csv', '10', '10', '50', '{"petal width": 1.5, "petal length": 4, "sepal width": 0.5, "sepal length": 0.5}', 'Iris-versicolor'],
            ['data/iris.csv', '10', '10', '50', '{"petal length": 1}', 'Iris-setosa'],
            ['data/iris_sp_chars.csv', '10', '10', '50', '{"pétal.length": 4, "pétal&width\u0000": 1.5, "sépal&width": 0.5, "sépal.length": 0.5}', 'Iris-versicolor'],
            ['data/price.csv', '10', '10', '50', '{"Price": 1200}', 'Product1']]
        show_doc(self.test_scenario5, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_logistic_model(self)
            model_create.the_logistic_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_logistic_model(self)
            prediction_create.i_create_a_logistic_prediction(self, example[4])
            prediction_create.the_logistic_prediction_is(self, example[5])
            prediction_compare.i_create_a_local_prediction(self, example[4])
            prediction_compare.the_local_prediction_is(self, example[5])


    def test_scenario6(self):
        """
            Scenario: Successfully comparing predictions with text options:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I update the source with params "<options>"
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a logistic regression model
                And I wait until the logistic regression model is ready less than <time_3> secs
                And I create a local logistic regression model
                When I create a logistic regression prediction for "<data_input>"
                Then the logistic regression prediction is "<prediction>"
                And I create a local logistic regression prediction for "<data_input>"
                Then the local logistic regression prediction is "<prediction>"

                Examples:
                | data             | time_1  | time_2 | time_3 | options | data_input                             | prediction  |

        """
        examples = [
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": true, "stem_words": true, "use_stopwords": false, "language": "en"}}}}', '{"Message": "Mobile call"}', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": true, "stem_words": true, "use_stopwords": false, "language": "en"}}}}', '{"Message": "A normal message"}', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": false, "stem_words": false, "use_stopwords": false, "language": "en"}}}}', '{"Message": "Mobile calls"}', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": false, "stem_words": false, "use_stopwords": false, "language": "en"}}}}', '{"Message": "A normal message"}', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": false, "stem_words": true, "use_stopwords": true, "language": "en"}}}}', '{"Message": "Mobile call"}', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"case_sensitive": false, "stem_words": true, "use_stopwords": true, "language": "en"}}}}', '{"Message": "A normal message"}', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"token_mode": "full_terms_only", "language": "en"}}}}', '{"Message": "FREE for 1st week! No1 Nokia tone 4 ur mob every week just txt NOKIA to 87077 Get txting and tell ur mates. zed POBox 36504 W45WQ norm150p/tone 16+"}', 'ham'],
            ['data/spam.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"token_mode": "full_terms_only", "language": "en"}}}}', '{"Message": "Ok"}', 'ham']]
        show_doc(self.test_scenario6, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            source_create.i_update_source_with(self, example[4])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_logistic_model(self)
            model_create.the_logistic_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_logistic_model(self)
            prediction_create.i_create_a_logistic_prediction(self, example[5])
            prediction_create.the_logistic_prediction_is(self, example[6])
            prediction_compare.i_create_a_local_prediction(self, example[5])
            prediction_compare.the_local_prediction_is(self, example[6])

    def test_scenario7(self):
        """
            Scenario: Successfully comparing predictions with text options:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I update the source with params "<options>"
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a logistic regression model with objective "<objective>"
                And I wait until the logistic regression model is ready less than <time_3> secs
                And I create a local logistic regression model
                When I create a logistic regression prediction for "<data_input>"
                Then the logistic regression prediction is "<prediction>"
                And the logistic regression probability for the prediction is "<probability>"
                And I create a local logistic regression prediction for "<data_input>"
                Then the local logistic regression prediction is "<prediction>"
                And the local logistic regression probability for the prediction is "<probability>"

                Examples:
                | data             | time_1  | time_2 | objective | time_3 | options | data_input                             | prediction  | probability

        """
        examples = [
            ['data/spam.csv', '20', '20', '180', '{"fields": {"000001": {"optype": "text", "term_analysis": {"token_mode": "full_terms_only", "language": "en"}}}}', '{"Message": "A normal message"}', 'ham', 0.9169, "000000"],
            ['data/spam.csv', '20', '20', '180', '{"fields": {"000001": {"optype": "text", "term_analysis": {"token_mode": "all", "language": "en"}}}}', '{"Message": "mobile"}', 'ham', 0.815, "000000"],
            ['data/movies.csv', '20', '20', '180', '{"fields": {"000007": {"optype": "items", "item_analysis": {"separator": "$"}}}}', '{"gender": "Female", "genres": "Adventure$Action", "timestamp": 993906291, "occupation": "K-12 student", "zipcode": 59583, "rating": 3}', 'Under 18', '0.8393', '000002']]
        show_doc(self.test_scenario7, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            source_create.i_update_source_with(self, example[4])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_logistic_model_with_objective_and_parms(self, example[8])
            model_create.the_logistic_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_logistic_model(self)
            prediction_create.i_create_a_logistic_prediction(self, example[5])
            prediction_create.the_logistic_prediction_is(self, example[6])
            prediction_create.the_logistic_probability_is(self, example[7])
            prediction_compare.i_create_a_local_prediction(self, example[5])
            prediction_compare.the_local_prediction_is(self, example[6])
            prediction_compare.the_local_probability_is(self, example[7])

    def test_scenario8(self):
        """
            Scenario: Successfully comparing predictions with text options and proportional missing strategy:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I update the source with params "<options>"
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a model
                And I wait until the model is ready less than <time_3> secs
                And I create a local model
                When I create a proportional missing strategy prediction for "<data_input>"
                Then the prediction for "<objective>" is "<prediction>"
                And I create a proportional missing strategy local prediction for "<data_input>"
                Then the local prediction is "<prediction>"

                Examples:

        """
        examples = [
            ['data/text_missing.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"token_mode": "all", "language": "en"}}, "000000": {"optype": "text", "term_analysis": {"token_mode": "all", "language": "en"}}}}', '{}', "000003",'swap'],
            ['data/text_missing.csv', '20', '20', '30', '{"fields": {"000001": {"optype": "text", "term_analysis": {"token_mode": "all", "language": "en"}}, "000000": {"optype": "text", "term_analysis": {"token_mode": "all", "language": "en"}}}}', '{"category1": "a"}', "000003",'paperwork']]
        show_doc(self.test_scenario8, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            source_create.i_update_source_with(self, example[4])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_model(self)
            model_create.the_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_model(self)
            prediction_create.i_create_a_proportional_prediction(self, example[5])
            prediction_create.the_prediction_is(self, example[6], example[7])
            prediction_compare.i_create_a_proportional_local_prediction(self, example[5])
            prediction_compare.the_local_prediction_is(self, example[7])


    def test_scenario9(self):
        """
            Scenario: Successfully comparing predictions with text options:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I update the source with params "<options>"
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a logistic regression model with objective "<objective>" and parms "<parms>"
                And I wait until the logistic regression model is ready less than <time_3> secs
                And I create a local logistic regression model
                When I create a logistic regression prediction for "<data_input>"
                Then the logistic regression prediction is "<prediction>"
                And the logistic regression probability for the prediction is "<probability>"
                And I create a local logistic regression prediction for "<data_input>"
                Then the local logistic regression prediction is "<prediction>"
                And the local logistic regression probability for the prediction is "<probability>"

        """
        examples = [
            ['data/iris.csv', '20', '20', '130', '{"fields": {"000000": {"optype": "categorical"}}}', '{"species": "Iris-setosa"}', '5.0', 0.0394, "000000", '{"field_codings": [{"field": "species", "coding": "dummy", "dummy_class": "Iris-setosa"}]}'],
            ['data/iris.csv', '20', '20', '130', '{"fields": {"000000": {"optype": "categorical"}}}', '{"species": "Iris-setosa"}', '5.0', 0.0511, "000000", '{"balance_fields": false, "field_codings": [{"field": "species", "coding": "contrast", "coefficients": [[1, 2, -1, -2]]}]}'],
            ['data/iris.csv', '20', '20', '130', '{"fields": {"000000": {"optype": "categorical"}}}', '{"species": "Iris-setosa"}', '5.0', 0.0511, "000000", '{"balance_fields": false, "field_codings": [{"field": "species", "coding": "other", "coefficients": [[1, 2, -1, -2]]}]}'],
            ['data/iris.csv', '20', '20', '130', '{"fields": {"000000": {"optype": "categorical"}}}', '{"species": "Iris-setosa"}', '5.0', 0.0417, "000000", '{"bias": false}']]
        show_doc(self.test_scenario9, examples)

        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            source_create.i_update_source_with(self, example[4])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_logistic_model_with_objective_and_parms(self, example[8], example[9])
            model_create.the_logistic_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_logistic_model(self)
            prediction_create.i_create_a_logistic_prediction(self, example[5])
            prediction_create.the_logistic_prediction_is(self, example[6])
            prediction_create.the_logistic_probability_is(self, example[7])
            prediction_compare.i_create_a_local_prediction(self, example[5])
            prediction_compare.the_local_prediction_is(self, example[6])
            prediction_compare.the_local_probability_is(self, example[7])

    def test_scenario10(self):
        """
            Scenario: Successfully comparing predictions with proportional missing strategy and balanced models:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a balanced model
                And I wait until the model is ready less than <time_3> secs
                And I create a local model
                When I create a proportional missing strategy prediction for "<data_input>"
                Then the prediction for "<objective>" is "<prediction>"
                And the confidence for the prediction is "<confidence>"
                And I create a proportional missing strategy local prediction for "<data_input>"
                Then the local prediction is "<prediction>"
                And the local prediction's confidence is "<confidence>"
                And I create local probabilities for "<data_input>"
                Then the local probabilities are "<probabilities>"

                Examples:
                | data               | time_1  | time_2 | time_3 | data_input           | objective | prediction     | confidence |

        """
        examples = [
            ['data/iris_unbalanced.csv', '10', '10', '10', '{}', '000004', 'Iris-setosa', '0.25284', '[0.33333, 0.33333, 0.33333]'],
            ['data/iris_unbalanced.csv', '10', '10', '10', '{"petal length":1, "sepal length":1, "petal width": 1, "sepal width": 1}', '000004', 'Iris-setosa', '0.7575', '[1.0, 0.0, 0.0]']]
        show_doc(self.test_scenario10, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_balanced_model(self)
            model_create.the_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_model(self)
            prediction_create.i_create_a_proportional_prediction(self, example[4])
            prediction_create.the_prediction_is(self, example[5], example[6])
            prediction_compare.i_create_a_proportional_local_prediction(self, example[4])
            prediction_compare.the_local_prediction_is(self, example[6])
            prediction_create.the_confidence_is(self, example[7])
            prediction_compare.the_local_prediction_confidence_is(self, example[7])
            prediction_compare.i_create_local_probabilities(self, example[4])
            prediction_compare.the_local_probabilities_are(self, example[8])

    def test_scenario11(self):
        """
            Scenario: Successfully comparing predictions for logistic regression with balance_fields:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I update the source with params "<options>"
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I create a logistic regression model with objective "<objective>" and flags
                And I wait until the logistic regression model is ready less than <time_3> secs
                And I create a local logistic regression model
                When I create a logistic regression prediction for "<data_input>"
                Then the logistic regression prediction is "<prediction>"
                And the logistic regression probability for the prediction is "<probability>"
                And I create a local logistic regression prediction for "<data_input>"
                Then the local logistic regression prediction is "<prediction>"
                And the local logistic regression probability for the prediction is "<probability>"

                Examples:
                | data               | time_1  | time_2 | objective | time_3 | options | data_input                             | prediction  | probability

        """
        examples = [
            ['data/movies.csv', '20', '20', '180', '{"fields": {"000000": {"name": "user_id", "optype": "numeric"},'
                                                  ' "000001": {"name": "gender", "optype": "categorical"},'
                                                  ' "000002": {"name": "age_range", "optype": "categorical"},'
                                                  ' "000003": {"name": "occupation", "optype": "categorical"},'
                                                  ' "000004": {"name": "zipcode", "optype": "numeric"},'
                                                  ' "000005": {"name": "movie_id", "optype": "numeric"},'
                                                  ' "000006": {"name": "title", "optype": "text"},'
                                                  ' "000007": {"name": "genres", "optype": "items",'
                                                  '"item_analysis": {"separator": "$"}},'
                                                  '"000008": {"name": "timestamp", "optype": "numeric"},'
                                                  '"000009": {"name": "rating", "optype": "categorical"}},'
                                                  '"source_parser": {"separator": ";"}}', '{"timestamp": "999999999"}', '4', 0.3231, "000009", '{"balance_fields": false}'],
            ['data/movies.csv', '20', '20', '180', '{"fields": {"000000": {"name": "user_id", "optype": "numeric"},'
                                                  ' "000001": {"name": "gender", "optype": "categorical"},'
                                                  ' "000002": {"name": "age_range", "optype": "categorical"},'
                                                  ' "000003": {"name": "occupation", "optype": "categorical"},'
                                                  ' "000004": {"name": "zipcode", "optype": "numeric"},'
                                                  ' "000005": {"name": "movie_id", "optype": "numeric"},'
                                                  ' "000006": {"name": "title", "optype": "text"},'
                                                  ' "000007": {"name": "genres", "optype": "items",'
                                                  '"item_analysis": {"separator": "$"}},'
                                                  '"000008": {"name": "timestamp", "optype": "numeric"},'
                                                  '"000009": {"name": "rating", "optype": "categorical"}},'
                                                  '"source_parser": {"separator": ";"}}', '{"timestamp": "999999999"}', '4', 0.2622, "000009", '{"normalize": true}'],
            ['data/movies.csv', '20', '20', '180', '{"fields": {"000000": {"name": "user_id", "optype": "numeric"},'
                                                  ' "000001": {"name": "gender", "optype": "categorical"},'
                                                  ' "000002": {"name": "age_range", "optype": "categorical"},'
                                                  ' "000003": {"name": "occupation", "optype": "categorical"},'
                                                  ' "000004": {"name": "zipcode", "optype": "numeric"},'
                                                  ' "000005": {"name": "movie_id", "optype": "numeric"},'
                                                  ' "000006": {"name": "title", "optype": "text"},'
                                                  ' "000007": {"name": "genres", "optype": "items",'
                                                  '"item_analysis": {"separator": "$"}},'
                                                  '"000008": {"name": "timestamp", "optype": "numeric"},'
                                                  '"000009": {"name": "rating", "optype": "categorical"}},'
                                                  '"source_parser": {"separator": ";"}}', '{"timestamp": "999999999"}', '4', 0.2622, "000009", '{"balance_fields": true, "normalize": true}']]
        show_doc(self.test_scenario11, examples)
        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            source_create.i_update_source_with(self, example[4])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            model_create.i_create_a_logistic_model_with_objective_and_parms(self, example[8], example[9])
            model_create.the_logistic_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_logistic_model(self)
            prediction_create.i_create_a_logistic_prediction(self, example[5])
            prediction_create.the_logistic_prediction_is(self, example[6])
            prediction_create.the_logistic_probability_is(self, example[7])
            prediction_compare.i_create_a_local_prediction(self, example[5])
            prediction_compare.the_local_prediction_is(self, example[6])
            prediction_compare.the_local_probability_is(self, example[7])

    def test_scenario12(self):
        """
            Scenario: Successfully comparing logistic regression predictions with constant fields:

                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I create a dataset
                And I wait until the dataset is ready less than <time_2> secs
                And I update the dataset with "<params>"
                And I wait until the dataset is ready less than <time_4> secs
                And I create a logistic regression model
                And I wait until the logistic regression model is ready less than <time_3> secs
                And I create a local logistic regression model
                When I create a logistic regression prediction for "<data_input>"
                Then the logistic regression prediction is "<prediction>"
                And I create a local logistic regression prediction for "<data_input>"
                Then the local logistic regression prediction is "<prediction>"

                Examples:
                | data             | time_1  | time_2 | time_3 |time_4| data_input                                 | prediction  | field_id

        """
        examples = [
            ['data/constant_field.csv', '10', '10', '50', '10','{"a": 1, "b": 1, "c": 1}', 'a', '{"fields": {"000000": {"preferred": true}}}']]
        show_doc(self.test_scenario12, examples)

        for example in examples:
            print "\nTesting with:\n", example
            source_create.i_upload_a_file(self, example[0])
            source_create.the_source_is_finished(self, example[1])
            dataset_create.i_create_a_dataset(self)
            dataset_create.the_dataset_is_finished_in_less_than(self, example[2])
            dataset_create.i_update_dataset_with(self, example[7])
            dataset_create.the_dataset_is_finished_in_less_than(self, example[4])
            model_create.i_create_a_logistic_model(self)
            model_create.the_logistic_model_is_finished_in_less_than(self, example[3])
            prediction_compare.i_create_a_local_logistic_model(self)
            prediction_create.i_create_a_logistic_prediction(self, example[5])
            prediction_create.the_logistic_prediction_is(self, example[6])
            prediction_compare.i_create_a_local_prediction(self, example[5])
            prediction_compare.the_local_prediction_is(self, example[6])
