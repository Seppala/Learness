import datetime
from haystack import indexes
from haystack import site
from learness3.flow.models import Project, Question, Answer, Comment, Link


class QuestionIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='owner')
    pub_date = indexes.DateField(model_attr='datecreated')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Question.objects.filter(pub_date__lte=datetime.datetime.now())


site.register(Question, QuestionIndex)