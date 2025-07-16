from typing import Union, Any

class Abstract:
	
	class Property:

		def __init__(self, name: str, value: Any=None, allowed: list[Any]=None):
			self.name = name
			self.value = value
			self.allowed = allowed
			
		def set(self, value):
			if self.allowed is not None:
				if value not in self.allowed:
					raise ValueError
			self.value = value
		
	class Type:
		
		def __init__(self, name: str, *properties):
			self.name = name
			self.properties = properties
			self.relations = []
			
	class Relation:

		def __init__(self, name: str, *ts, bidirectional: bool=False, **kwargs):
			self.name = name
			self.initial = ts[0]
			self.types = ts
			self.bidirectional = bidirectional
			self.args = kwargs
			for t in self.types:
				t.relations.append(self)

class Referent:

	class Entity:

		def __init__(self, t: Type, **props: dict[str]):
			self.type = t
			self.properties = t.properties
			for name in props.keys():
				self.property(name).set(props[name])
			self.relations = []
				
		def property(self, name):
			for p in self.properties:
				if p.name == name:
					return p
			raise NameError
			
	class Relation:
		
		def __init__(self, name: str, *es, bidirectional: bool=False, **kwargs):
			self.name = name
			self.entities = es
			self.initial = es[0]
			self.bidirectional = bidirectional
			self.args = kwargs
			for e in self.entities:
				e.relations.append(self)

class OntologicalNetwork:

	class Query:

		def __init__(self, **kwargs):
			self.is_type = None
			self.is_not_type = None
			self.has_type_relation = None
			self.has_not_type_relation = None
			self.is_type_related_to = None
			self.is_not_type_related_to = None
			self.has_referent_relation = None
			self.has_not_referent_relation = None
			self.is_referent_related_to = None
			self.is_not_referent_related_to = None
			self.has_property = None
			self.has_not_property = None
			self.property_unknown = None
			self.property_is = None
			self.property_is_not = None
			
