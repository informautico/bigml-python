# -*- coding: utf-8 -*-
#
# Copyright 2015-2022 BigML
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


""" Uploading source with structured args

"""
import sys

from .world import world, setup_module, teardown_module, show_doc, \
    show_method, delete_local
from . import create_source_steps as source_create
from bigml.api_handlers.resourcehandler import get_id

class TestUploadSource(object):

    def setup(self):
        """
            Debug information
        """
        print("\n-------------------\nTests in: %s\n" % __name__)

    def teardown(self):
        """
            Debug information
        """
        delete_local()
        print("\nEnd of tests in: %s\n-------------------\n" % __name__)

    def test_scenario1(self):
        """

            Scenario: Successfully uploading source:
                Given I create a data source uploading a "<data>" file with args "<source_conf>"
                And I wait until the source is ready less than <source_wait> secs
                Then the source exists and has args "<source_conf>"
        """
        show_doc(self.test_scenario1)
        headers = ["data", "source_wait", "source_conf"]
        examples = [
            ['data/iris.csv', '30', '{"tags": ["my tag", "my second tag"]}'],
            ['data/iris.csv', '30', '{"name": "Testing unicode names: áé"}']]
        for example in examples:
            example = dict(zip(headers, example))
            show_method(self, sys._getframe().f_code.co_name, example)
            source_create.i_upload_a_file_with_args(
                self, example["data"], example["source_conf"])
            source_create.the_source_is_finished(self, example["source_wait"])
            source_create.source_has_args(self, example["source_conf"])

    def test_scenario2(self):
        """

            Scenario: Successfully creating composite source:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <source_wait> secs
                And I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <source_wait> secs
                Then I create a composite from the last two sources
                And I wait until the source is ready less than <source_wait> secs
                Then the composite exists and has the previous two sources
        """
        show_doc(self.test_scenario2)
        headers = ["data", "source_wait"]
        examples = [
            ['data/iris.csv', '30']]
        for example in examples:
            example = dict(zip(headers, example))
            show_method(self, sys._getframe().f_code.co_name, example)
            sources = []
            source_create.i_upload_a_file(
                self, example["data"])
            source_create.the_source_is_finished(
                self, example["source_wait"])
            sources.append(get_id(world.source["resource"]))
            source_create.i_upload_a_file(
                self, example["data"])
            source_create.the_source_is_finished(
                self, example["source_wait"])
            sources.append(get_id(world.source["resource"]))
            source_create.i_create_composite(self, sources)
            source_create.the_source_is_finished(self, example["source_wait"])
            for source in sources:
                world.sources.remove("source/%s" % source)
            source_create.the_composite_contains(self, sources)

    def test_scenario3(self):
        """

            Scenario: Successfully cloning source:
                Given I create a data source uploading a "<data>" file
                And I wait until the source is ready less than <time_1> secs
                And I clone the last source
                And I wait until the source is ready less than <time_1> secs
                Then the new source the first one as origin

                Examples:
                | data             | time_1  |
                | ../data/iris.csv | 30      |

        """
        show_doc(self.test_scenario3)
        headers = ["data", "source_wait"]
        examples = [
            ['data/iris.csv', '30']]
        for example in examples:
            example = dict(zip(headers, example))
            show_method(self, sys._getframe().f_code.co_name, example)
            source_create.i_upload_a_file(
                self, example["data"], shared=example["data"])
            source_create.the_source_is_finished(
                self, example["source_wait"], shared=example["data"])
            source = world.source["resource"]
            source_create.clone_source(self, source)
            source_create.the_source_is_finished(
                self, example["source_wait"])
            source_create.the_cloned_source_origin_is(self, source)
