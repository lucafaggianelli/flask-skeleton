#!/usr/bin/env python
import sys
import os
import re
import glob
import logging
from argparse import ArgumentParser
try:
    import jinja2 as jj
except:
    sys.exit('Please install jinja2')

__version__ = '0.1'

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_BLACKLIST = ('static')
RE_APP_NAME = re.compile('^[a-zA-Z][a-zA-Z0-9_]*$')

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('command', nargs='+',
            help='Possible values: createapp')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return args

def render_python_src(app_name, context=dict(), out_dir='.'):
    logging.debug('THIS_DIR = ' + THIS_DIR)

    out_dir = os.path.abspath(out_dir)
    logging.info('Output directory ' + out_dir)

    app_dir = os.path.join(out_dir, app_name)
    if os.path.exists(app_dir):
        if len(os.listdir(app_dir)) > 0:
            sys.exit('App directory not empty ' + app_dir)
    else:
        os.mkdir(app_dir, 0755)
        logging.info('Created directory ' + app_dir)

    # Init Jinja2 environment with different tokens otherwise is impossible
    # to generate HTML files with {{ }} strings
    template_dir = os.path.join(THIS_DIR,'app_template')
    jinja_env = jj.Environment(loader=jj.FileSystemLoader(template_dir),
            block_start_string = '{$',
            block_end_string = '$}',
            variable_start_string = '{[',
            variable_end_string = ']}',
        )

    """
    Search files to render with Jinja2

    Copy from A=<template_dir>/ to B=<app_dir>/
    Need relative path in A and in B
    """
    for curr_dir, dirs, files in os.walk(template_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in TEMPLATE_BLACKLIST]

        # relative current path of the walked template dir, something like:
        # runserver.py, app_name/templates/index.html
        template_curr_dir = os.path.relpath(curr_dir, start=template_dir) # curr_dir_rel
        out_curr_dir = os.path.join(app_dir, re.sub('^app_name', app_name, template_curr_dir))
        print 'template_curr_dir.repl()', re.sub('^app_name', app_name, template_curr_dir)
        print 'template_curr_dir', template_curr_dir
        print 'out_curr_dir', out_curr_dir

        # Walked into a new directory, should create the same dir in the
        # out dir
        if not os.path.exists(out_curr_dir):
            os.mkdir(out_curr_dir)
            logging.debug('Created directory ' + out_curr_dir)

        for source in files:
            #src = os.path.join(out_curr_dir, source)

            # Read the template with a relative path from template_dir
            template = jinja_env.get_template(os.path.join(template_curr_dir, source))
            compiled = template.render(context)
            #logging.warning('Can\'t render template: ' + src)

            # Write the rendered file to the out_dir, the path will be the
            # same as the template but the app_name folder is renamed
            out_file = os.path.join(out_curr_dir, source)
            with open(out_file, 'w') as f:
                f.write(compiled)

            # Set correct mode of the compiled files
            os.chmod(out_file, os.stat(os.path.join(template_dir, template_curr_dir, source)).st_mode)
            logging.debug('Rendered %s -> %s' % (os.path.join(template_curr_dir, source), out_file))

if __name__ == '__main__':
    args = parse_args()

    cmd = args.command[0]
    if cmd == 'createapp':
        if len(args.command) < 3:
            sys.exit('Need a directory and a name for the app')

        if not os.path.isdir(args.command[1]):
            sys.exit('Output path is not a directory ' + out_dir)

        if re.match(RE_APP_NAME, args.command[2]) is None:
            sys.exit('App name can only contain letters, numbers and ' +
                    'underscore. The first char can only be a letter')

        out_dir = os.path.abspath(args.command[1])
        app_name = args.command[2]

        app_name_pretty = None
        if len(args.command) >= 4:
            app_name_pretty = args.command[3]

        print 'Creating app', app_name

        context = {
            'name': app_name,
            'name_pretty': app_name_pretty if app_name_pretty else app_name
        }
        render_python_src(app_name, out_dir=out_dir, context=context)
