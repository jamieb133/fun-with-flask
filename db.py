#run to create or delete local dev database (used for development)

from app import app
from flask_sqlalchemy import SQLAlchemy
from app.views import db 
import argparse

p = argparse.ArgumentParser(description='script to control the postgres database')
p.add_argument('--create', action='store_true', help='create the account table')
p.add_argument('--delete', action='store_true', help='drop the account table')
p.add_argument('--reset', action='store_true', help='drop the account table and recreate it')
args = p.parse_args()

if args.delete:
    sure = input('WARNING THIS WILL DELETE ALL ACCOUNT INFO, ARE YOU SURE? [y/n]')
    if sure == 'y':
        db.drop_all()
elif args.create:
    db.create_all()
elif args.reset:
    db.drop_all()
    db.create_all()
else:
    p.print_help()
