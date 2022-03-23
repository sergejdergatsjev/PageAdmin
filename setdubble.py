>>> from permanentjob.models import *
>>> dir()
['Category', 'DubbeleContent', 'Img', 'JobApplication', 'JobKeyword', 'NOW', 'PermanentJob', '__builtins__', 'choices', 'datetime', 'models', 'now', 'settings']
>>> all_jobs = PermanentJob.objects.all()
>>> all_jobs.update(status=0)
2982
>>> 
>>> dubbles = DubbeleContent.objects.all()
for dubble in dubbles:
...  dubble.same_with.status = 4
...  dubble.same_with.save()
