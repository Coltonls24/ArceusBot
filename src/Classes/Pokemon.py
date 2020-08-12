class Pokemon:
    def __init__(self, pokemon):
        self._name = pokemon['name']
        self._id = pokemon['id']
        self._sprite = pokemon['sprites']['front_default']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite