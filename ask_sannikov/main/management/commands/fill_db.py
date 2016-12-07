import datetime
from django.core.management.base import BaseCommand, CommandError
from main.models import Question, Answer, Hashtag

class Command(BaseCommand):
    help = 'Fills the DB'

    def do(self):
        h = Hashtag(tag="test")
        h.save()
        for i in xrange(1,10000):
            q = Question(id = i,
                title="Question no. " + str(i),
                text="This is a test. The no. is " + str(i),
                timeStamp=datetime.datetime.now())
            q.save()
            h2 = Hashtag(tag=str(i))
            h2.save()
            q.hashtags.add(h, h2)
            for t in xrange(1,10):
                a = Answer(text = "no. " + str(i) + " being answered here for the "
                    + str(t) + "th time",
                    question_id = i,
                    timeStamp=datetime.datetime.now())
                Question.objects.get(id=i).answerCount += 1
                a.save()

    
    def handle(self, *args, **options):
        self.do()
        self.stdout.write('Success')
