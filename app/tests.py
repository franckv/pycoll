class Test:
    """
    >>> from app.models import Item, ItemType, Performer, PerformerType, Role, RoleType
    >>> from app.forms import ItemForm
    >>> import datetime

    >>> cd = ItemType.objects.get(name="CD")
    >>> cd.name
    u'CD'
    >>> form = ItemForm.get_form(cd)
    >>> form
    <class 'app.forms.CDForm'>

    >>> item = Item.new(cd)
    >>> item.name = 'couin'
    >>> item
    <CD: ? - couin>
    >>> item.type
    <ItemType: CD>

    >>> item.creation_date = datetime.datetime.now()
    >>> item.update_date = datetime.datetime.now()
    >>> item.save()
    >>> item.name
    'couin'
    >>> item.type
    <ItemType: CD>
    >>> item.type.pk
    1
    >>> item.get_absolute_url()
    '/manager/items/1/'

    >>> Item.objects.get(name='couin')
    <Item: ? - couin>

    >>> PerformerType.objects.all()
    [<PerformerType: Person>, <PerformerType: Group>]

    >>> performer = Performer.new(PerformerType.objects.get(name='Person'))
    >>> performer.name='toto'
    >>> performer.save()
    >>> performer.name
    'toto'
    >>> performer.type
    <PerformerType: Person>

    >>> roletype = RoleType.objects.get(name='Artist')
    >>> roletype.name
    u'Artist'

    >>> role = Role()
    >>> role.item = item
    >>> role.performer = performer
    >>> role.type = roletype
    >>> role.save()

    >>> item
    <CD: toto - couin>

    >>> from django.test.client import Client
    >>> c=Client()

    >>> response=c.get('/manager/')
    >>> response.status_code
    302

    >>> c.login()
    False

    >>> c.login(username='test', password='test')
    True

    >>> response=c.get('/manager/items/')
    >>> response.status_code
    200

    >>> response.template[0].name
    'app/items.html'

    >>> response.context['items_list']
    [<Item: toto - couin>]



    """

    def __init__(self):
	pass
