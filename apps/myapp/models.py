from django.db import models
import bcrypt
from datetime import datetime

now = str(datetime.now())
# print(type(now))

class UserManager(models.Manager):

    def regValidator(self, form):

        errors = []

        if len(form['name']) < 3:
            errors.append("Name must have at least 3 characters.")
        if len(form['username']) < 2:
            errors.append("Username must have at least 3 characters.")
        elif User.objects.filter(username=form['username']):
             errors.append("Account already exists.")
        if len(form['password']) < 5:
            errors.append("Password must have at least 5 characters.")
        elif form['password'] != form['confirm_pw']:
            errors.append("Password and confirm password must match.")


        if not errors:
            hash1 = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=form['name'], username=form['username'], password=hash1)
            return (True, user)
        else:
            return (False, errors)


    def loginValidator(self, form):

        errors = []

        if not form['username']:
            errors.append("Username required.")
        elif len(form['username']) < 3:
            errors.append("Username must have at least 3 characters.")
        # must use filter() instead of get() in case nothing comes back:
        elif not User.objects.filter(username=form['username']):
             errors.append("Please register first.")

        if len(form['password']) < 3:
            errors.append("Password must have at least 8 characters.")
        else:
            user = User.objects.filter(username=form['username'])
            if not bcrypt.checkpw(form['password'].encode(), user[0].password.encode()):
                errors.append("Password does not match password in database.")

        if not errors:
            return (True, user[0])
        else:
            return (False, errors)

class TripValidator(models.Manager):

    def tripValidator(self, form, user_id):
        errors = []

        if not form['dest']:
            errors.append('Destination is required')
        if not form['desc']:
            errors.append('Description is required')

        if not form['start_date']:
            errors.append('Start date is required')
        # else:
        #     start_date = datetime.strptime(form['start_date'], '%Y-%m-%d')
        #     if start_date < now:
        #         errors.append('Start date must be in the future')
        elif form['start_date'] < now:
            errors.append('Start date must be in the future')

        if not form['end_date']:
            errors.append('End date is required')
        elif form['end_date'] < now:
            errors.append('End date must be in the future')

        if form['end_date'] < form['start_date']:
            errors.append('End date must be after start date')

        if not errors:
            planner = User.objects.get(id=user_id)
            trip = Trip.objects.create(dest=form['dest'], desc=form['desc'], start_date=form['start_date'], end_date=form['end_date'], planner=planner)

            # adding this trip and user to Join table
            planner.joins.add(trip)

            return (True, trip)
        else:
            return (False, errors)



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
    # joins (to Join table)
    # trips (to Trip table)
    def __repr__(self):
        return "<User {} | {} | {}>".format(self.id, self.name, self.username)

class Trip(models.Model):
    dest = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    planner = models.ForeignKey(User, related_name="trips")
    joiners = models.ManyToManyField(User, related_name="joins")

    objects = TripValidator()
    def __repr__(self):
        return "<Trip {} | {} | {}>".format(self.id, self.dest, self.desc)
