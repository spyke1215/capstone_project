from django_tables2 import tables, TemplateColumn
from cmis.models import Deceased

class DeceasedTable(tables.Table):
    class Meta:
         model = Deceased
         attrs = {'class': 'table table-sm'}
         fields = ['date', 'description', 'tags', 'points', 'edit']
