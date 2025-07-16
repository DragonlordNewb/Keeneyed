from typing import Union, Any

class Abstract:
	
	class Property:

		def __init__(self, name: str, value: Any=None, allowed: list[Any]=None, not_allowed=None):
			self.name = name
			self.value = value
			self.allowed = allowed
			self.not_allowed = not_allowed
			
		def set(self, value):
			if self.allowed is not None:
				if value not in self.allowed:
					raise ValueError
			if self.not_allowed is not None:
				if value in self.not_allowed:
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
			self.request_type = None
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
			
	def __init__(self):
		self.types = []
		self.abstract_relations = []
		self.entities = []
		self.referent_relations = []

	def __contains__(self, x):
		hx = hash(x)
		for a in self.types:
			if hash(a) == hx:
				return True
		for b in self.abstract_relations:
			if hash(b) == hx:
				return True
		for c in self.entities:
			if hash(c) == hx:
				return True
		for d in self.entities:
			if hash(d) == hx:
				return True
		return False
		
	def load_type(self, t):
		self.types.append(t)
		for r in t.relations:
			if r not in self:
				self.load_abstract_relation(r)
				
	def load_abstract_relation(self, ar):
		self.abstract_relations.append(ar)
		for t in [ar.initial, *ar.types]:
			if t not in self:
				self.load_type(t)
				
	def load_entity(self, e):
		self.entities.append(e)
		for r in e.relations:
			if r not in self:
				self.load_referent_relation(r)
				
	def load_referent_relation(self, rr):
		self.referent_relations.append(rr)
		for e in [rr.initial, *rr.entities]:
			if e not in self:
				self.load_entity(e)
				
	def query(self, q: Query):
		target = None
		if q.request_type == Abstract.Type:
			target = self.types
		elif q.request_type == Abstract.Relation:
			target = self.abstract_relations
		elif q.request_type == Referent.Entity:
			target = self.entities
		elif q.request_type == Referent.Relation:
			target = self.referent_relations
		else:
			raise KeyError
		for x in target:
			if q.check(x):
				yield x
		
	def run_query(self, q: Query):
		return [x for x in self.query(q)]
