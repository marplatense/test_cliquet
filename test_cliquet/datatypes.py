from colander import SchemaType, Invalid, null


class Password(SchemaType):

    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null

    def serialize(self, node, appstruct):
        if appstruct is null:
            return null


