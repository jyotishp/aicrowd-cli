import json
import os

import click

from aicrowd.context import pass_info, Info
from helpers.evaluations import Evaluations, Utils
from aicrowd.config import Config



@click.group(name="grader", short_help="Grader related commands for the evaluations API")
@pass_info
def grader_command(info: Info):
    try:
        info.evalapi_auth_token
    except AttributeError:
        click.echo(f"Login to continue")
        evaluations = Evaluations()
        while True:
            email = click.prompt('Email', type=str)
            password = click.prompt('Password', type=str)
            if evaluations.login(email, password):
                break
            click.echo("Please try again!")            
        click.echo(f"Logged in successfully!")
        config = Config()
        vars(info).update(config.settings)
        
        

@click.command(help="Create Grader")
@click.option('--validate', '-v', is_flag = True)
@pass_info
def create(info: Info, validate):
    grader_url = click.prompt('Enter Grader URL', type=str)
    evaluations = Evaluations(info.evalapi_auth_token)
    if Utils().helm_validate(grader_url):
        click.echo("Validated!")

    if not validate:
        grader = evaluations.grader_create(grader_url)
        if grader:
            click.echo(f"Grader queued successfully with ID: {grader.id}")
        else:
            click.echo("Please try again!")

@click.command(help="Download grader template")
@pass_info
def templates(info: Info):
    templates = Utils().list_templates()

    for idx, template in enumerate(templates):
        click.echo(f'[{idx + 1}] {template}')

    template_idx = click.prompt('Select the grader template you wish to download')
    Utils().get_template(templates[int(template_idx) - 1])

@click.command(help="Download grader example")
@pass_info
def examples(info: Info):
    examples = Utils().list_examples()

    for idx, example in enumerate(examples):
        click.echo(f'[{idx + 1}] {example}')

    example_idx = click.prompt('Select the grader example you wish to download')
    Utils().get_example(examples[int(example_idx) - 1])

grader_command.add_command(create)
grader_command.add_command(templates)
grader_command.add_command(examples)

