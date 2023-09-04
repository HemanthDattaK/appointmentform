from django.db import models

class Contact(models.Model):
    TIMESLOT_LIST = (
        ('09:00 – 09:30', '09:00 – 09:30'),
        ('10:00 – 10:30', '10:00 – 10:30'),
        ('11:00 – 11:30', '11:00 – 11:30'),
        ('12:00 – 12:30', '12:00 – 12:30'),
        ('13:00 – 13:30', '13:00 – 13:30'),
        ('14:00 – 14:30', '14:00 – 14:30'),
        ('15:00 – 15:30', '15:00 – 15:30'),
        ('16:00 – 16:30', '16:00 – 16:30'),
        ('17:00 – 17:30', '17:00 – 17:30'),
    )

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    date = models.DateField()
    time_slot_choice = models.CharField(max_length=13, choices=TIMESLOT_LIST)

    @property
    def default_time_slot(self):
        return self.date.strftime('%H:%M')  # This generates "HH:MM" from the date

    def save(self, *args, **kwargs):
        if not self.time_slot_choice:
            base_time_slot = self.default_time_slot
            suffix = 0

            while True:
                if suffix == 0:
                    new_time_slot_choice = base_time_slot
                else:
                    new_time_slot_choice = f"{base_time_slot}_{suffix}"

                if not Contact.objects.filter(time_slot_choice=new_time_slot_choice).exists():
                    self.time_slot_choice = new_time_slot_choice
                    break
                suffix += 1

        super().save(*args, **kwargs)

    def time_slot(self):
        return self.time_slot_choice

    def __str__(self):
        return self.name

class AppointmentLimit(models.Model):
    limit = models.PositiveIntegerField(default=5)  # Default appointment limit correct if any error

