from django.db import models


# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=256)
    additions = models.ManyToManyField('Addition', related_name='additions+', symmetrical=False, blank=True, null=True,
                                       verbose_name='additions')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Method(models.Model):
    ord = models.IntegerField()
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Word(models.Model):
    s = models.CharField(max_length=256)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    method = models.ForeignKey('Method', on_delete=models.CASCADE)

    # synonyms = models.ManyToManyField('self', related_name = 'synonyms+', symmetrical=False, blank = True, null = True, verbose_name = "synonyms")
    # additions = models.ManyToManyField('Addition', related_name = 'additions+', symmetrical=False, blank = True, null = True, verbose_name = "additions")

    def __unicode__(self):
        return "{0}".format(self.s)

    def __str__(self):
        return self.s + ' (' + str(self.type) + ')'

    class Meta:
        ordering = ['s']


class AdditionType(models.Model):
    name = models.CharField(max_length=256)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Synonym(models.Model):
    choices = []
    for i in range(11):
        choices.append((i / 10, i / 10))
    w1 = models.ForeignKey('Word', on_delete=models.CASCADE, related_name='%(class)s_from')
    w2 = models.ForeignKey('Word', on_delete=models.CASCADE, related_name='%(class)s_to')
    similar = models.FloatField(choices=choices, default=0.1)

    class Meta:
        ordering = ['-id']


class Addition(models.Model):
    type = models.ForeignKey('AdditionType', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    add = models.CharField(max_length=256)
    exeption = models.CharField(max_length=256)
    additions = models.ManyToManyField('self', related_name='additions+', symmetrical=False, blank=True, null=True,
                                       verbose_name='additions')

    def __str__(self):
        return self.add + ' (' + self.name + ')'


class BuildWord(models.Model):
    word = models.CharField(max_length=1024)
    root = models.ForeignKey('Word', on_delete=models.CASCADE)
    additions = models.CharField(max_length=1024)

    def __str__(self):
        return self.word
