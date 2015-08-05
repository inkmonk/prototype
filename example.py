from schemalite import Schema, Field, validator, schema_validator, SchemaError
from schemalite.validators import type_validator


class PersonSchema(Schema):

    name = Field(required=True)
    gender = Field(required=True)
    age = Field(validator=type_validator(int), required=False)

    @classmethod
    @validator('age')
    def validate_age(cls, val):
        if val < 0 or val > 120:
            raise SchemaError('Invalid Value For Age')

    @classmethod
    @schema_validator
    def check_males_age(cls, data):
        if data['gender'] == 'M':
            if 'age' in data and data['age'] > 70:
                raise SchemaError('Male age cannot be greater than 70')


class OrganizationSchema(Schema):

    name = Field(required=True)
    head = Field(validator=PersonSchema.validate, required=False)
    members = Field(validator=PersonSchema.validate_list)


if __name__ == '__main__':
    ricky = {'gender': 'M', 'age': 80}

    try:
        PersonSchema.validate(ricky)
    except SchemaError as e:
        print e.value
    else:
        print "No error"

    adam = {'name': 'Adam', 'gender': 'M', 'age': -1.4}

    try:
        PersonSchema.validate(adam)
    except SchemaError as e:
        print e.value
    else:
        print "No error"

    john = {'name': 'John', 'gender': 'M', 'age': 200}

    try:
        PersonSchema.validate(john)
    except SchemaError as e:
        print e.value
    else:
        print "No error"

    maya = {'name': 'Maya', 'gender': 'M', 'age': 20}

    try:
        PersonSchema.validate(maya)
    except SchemaError as e:
        print e.value
    else:
        print "No error"

    org = {
        'name': 'Startup',
        'ceo': maya,
        'members': [
            adam, john,
            {'name': 'Peter', 'gender': 'M'},
            {'name': 'Martin', 'gender': 'X'}
        ]
    }
    try:
        OrganizationSchema.validate(org)
    except SchemaError as e:
        print e.value
    else:
        print "No error"

    ricky = {'name': 'Ricky', 'gender': 'M', 'age': 80}

    try:
        PersonSchema.validate(ricky)
    except SchemaError as e:
        print e.value
    else:
        print "No error"
