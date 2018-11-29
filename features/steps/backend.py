import csv
import os
from pathlib import Path
from behave import *
from features.constants import *


@given(u'I have backend file')
def step_impl(context):
    current_folder = os.path.dirname(__file__)
    backend_file_name = os.path.join(current_folder, BACKEND_FILE)
    backend_file = Path(backend_file_name)
    assert backend_file.is_file(), "Backend file '{}' not found".format(backend_file_name)
    context.backend_file = backend_file


@when(u'I run the backend')
def step_impl(context):
    current_folder = os.path.dirname(__file__)
    input_file = os.path.join(current_folder, INPUT_FILE)
    output_folder = os.path.join(current_folder, OUTPUT_FOLDER)
    os.system('java -jar {} "{}" "{}"'.format(context.backend_file, input_file, output_folder))


@then(u'csv file should be generated')
def step_impl(context):
    current_folder = os.path.dirname(__file__)
    output_file_name = os.path.join(current_folder, OUTPUT_FILE)
    output_file = Path(output_file_name)
    assert output_file.is_file(), "UI file '{}' not found".format(output_file_name)


def count_characters(file):
    result = {}
    with open(file) as source_file:
        data = source_file.read().replace('\n', '')
        for char in data:
            keys = result.keys()
#            if char == ' ':
#                char = ''
            if char in keys:
                result[char] += 1
            else:
                result[char] = 1
    return result


def csv_to_dict(file_name):
    result = {}
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                result[row[0]] = int(row[1])
            line_count += 1
    return result


@then(u'generated csv file should have correct data')
def step_impl(context):
    current_folder = os.path.dirname(__file__)
    input_counts = count_characters(os.path.join(current_folder, INPUT_FILE))
    csv_counts = csv_to_dict(os.path.join(current_folder, OUTPUT_FILE))
    assert input_counts == csv_counts, "Character counts are not correct in backend output file - expected '{}', actual '{}'".format(input_counts, csv_counts)
    context.csv_counts = csv_counts

