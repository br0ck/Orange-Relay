"""Basic Indexes and simple forward facing views"""

# django imports
from django.shortcuts import render
# local imports
from OR_web_GUI.models import Rule, Input, Output
from .hidden import check_output_state
# import for GPIO in real vs. test env
try:
    import OPi.GPIO as GPIO
    fake = False
except ImportError:
    from OR_web_GUI.packages import extendGPIO as GPIO
    fake = True
    print('The linux_interaction() function was not executed')


def index(request):
    # Basic Index
    inputs = Input.objects.order_by('date_added')
    rules = Rule.objects.order_by('date_added')
    for rule in rules:
        rule.output.state = check_output_state(rule.output.pk)
    outputs = Output.objects.order_by('date_added')
    for output in outputs:
        output.state = check_output_state(output.pk)
    context = {'inputs': inputs, 'outputs': outputs, 'rules': rules, 'fake': fake}
    return render(request, 'OR_web_GUI/index.html', context)


def rules(request):
    """Shows the rules"""
    rules = Rule.objects.order_by('date_added')
    for rule in rules:
        rule.output.state = check_output_state(rule.output.pk)
    context = {'rules': rules, 'fake': fake}
    return render(request, 'OR_web_GUI/rules.html', context)


def inputs(request):
    # Inputs index page
    inputs = Input.objects.order_by('date_added')
    rules = Rule.objects.order_by('date_added')
    for rule in rules:
        rule.output.state = check_output_state(rule.output.pk)
    context = {'rules': rules, 'inputs': inputs, 'fake': fake}
    return render(request, 'OR_web_GUI/inputs.html', context)


def outputs(request):
    # Outputs index page
    outputs = Output.objects.order_by('date_added')
    for output in outputs:
        output.state = GPIO.input(output.channel)
    context = {'outputs': outputs, 'fake': fake}
    return render(request, 'OR_web_GUI/outputs.html', context)