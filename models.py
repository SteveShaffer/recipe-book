#!/usr/bin/env python

import json

from google.appengine.ext import ndb
from google.appengine.api import users

class AppModel(ndb.Model):
  """This is the base model for this application.
  
  Basic Sub-Classing Usage:
  - Define model properties per usual GAE.
  - Override api_response_data() to specify how the model should report itself
    to the API in a message format (should return a dictionary)
  - If your model will be handling update requests from the API, override
    process_api_message() to specify how messages from the API should be
    interpreted (should accept the raw message format (e.g. JSON)). YOU ARE
    RESPONSIBLE FOR CALLING .put() (or not) IN THIS METHOD!
  """
  def api_response_data(self):
    """Override this function to return a dict to provide to the API response"""
    return {}
  
  def api_message(self, as_dict=False):
    message = self.api_response_data()
    if as_dict:
      return message
    else:
      return json.dumps(message)
    
  @classmethod
  def api_list_response_data(cls):
    """Override this function to return a different list to provide to the API
    response than the default of all the model's objects.
    """
    query = cls.query()
    return [ x.api_message(as_dict=True) for x in query ]
  
  @classmethod
  def api_list_message(cls, as_dict=False):
    message = cls.api_list_response_data()
    if as_dict:
      return message
    else:
      return json.dumps(message)
  
  def process_api_message(self, message):
    """Override this method to define custom API message-processing behavior for
    both creation and update requests.
    
    If you want to handle creation and update requests differently, override the
    create_from_api_message() and update_from_api_message() methods below
    instead of this one.
    """
    pass
  
  @classmethod
  def create_from_api_message(cls, message):
    try:
      obj = cls()
      obj.process_api_message(message)
      return obj
    except:
      return None
    
  def update_from_api_message(self, message):
    try:
      self.process_api_message(message)
      return self
    except:
      return None

class Account(AppModel):
  #Key: User ID
  
  @classmethod
  def get_for_current_user(cls):
    return ndb.Model.get_or_insert(users.get_current_user().user_id())
  
  #TODO: Continue implementing?

class Measure(AppModel):
  quantity = ndb.FloatProperty(verbose_name='Quantity')
  unit = ndb.StringProperty(verbose_name='Unit')
  
  def api_response_data(self):
    return {
      'quantity': self.quantity,
      'unit': self.unit,
      'text': ' '.join([self.quantity, self.unit])
    }

class Ingredient(Measure):
  description = ndb.StringProperty(verbose_name='Description')
  
  def api_response_data(self):
    return {
      'quantity': self.quantity,
      'unit': self.unit,
      'description': self.description,
      'text': ' '.join([ x for x in [self.quantity,
                                     self.unit,
                                     self.description] if x ])
    }

class Recipe(AppModel):
  name = ndb.StringProperty(default='New Recipe', verbose_name='Name')
  description = ndb.StringProperty(verbose_name='Description')
  makes = ndb.StructuredProperty(Measure)
  serves = ndb.StructuredProperty(Measure) #unit='People' #TODO: Implement somehow
  cooking_time = ndb.StructuredProperty(Measure) #unit='Minutes' #TODO: Implement somehow
  rating = ndb.FloatProperty(verbose_name='Rating')
  tags = ndb.StringProperty(repeated=True, verbose_name='Tags')
  ingridients = ndb.StructuredProperty(Ingredient, repeated=True,
                                       verbose_name='Ingredients')
  instructions = ndb.StringProperty(repeated=True, verbose_name='Instructions')
  
  def api_response_data(self):
    return {
      'id': self.key.id() if self.key else None,
      'name': self.name,
      'description': self.description,
      'makes': self.makes.api_message(as_dict=True) if self.makes else {},
      'serves': self.serves.api_message(as_dict=True) if self.serves else {},
      'cooking_time': self.cooking_time.api_message(as_dict=True) if
        self.cooking_time else {},
      'rating': self.rating,
      'tags': self.tags, #TODO: Does this work?
      'ingredients': [ x.api_message(as_dict=True) for x in self.ingredients ]
        if 'ingredients' in self._properties else [],
      'instructions': self.instructions #TODO: Does this work?
    }
  
  def process_api_message(self, message):
    message = json.loads(message)
    if 'name' in message: self.name = message['name']
    if 'description' in mesage: self.description = message['description']
    if 'makes' in message: self.makes = Measure(
      quantity=message['makes']['quantity'], unit=message['makes']['unit']
    ) #TODO: Use Measure.process_api_message()? (and for other ones below)
    if 'serves' in message: self.serves = Measure(
      quantity=message['serves']['quantity']
    )
    if 'cooking_time' in message: self.cooking_time = Measure(
      quantity=message['cooking_time']['quantity']
    )
    if 'rating' in message: self.rating = message['rating']
    if 'tags' in message: self.tags = message['tags']
    if 'ingredients' in message:
      self.ingredients = [
        Ingredient(quantity=x.quantity,
                   unit=x.unit,
                   description = x.description)
        for x in message['ingredients']
      ]
    if 'instructions' in message: self.instructions = message['instructions']
    self.put()
  
class ShoppingList(AppModel):
  name = ndb.StringProperty(default='My Shopping List', verbose_name='Name')
  items = ndb.StructuredProperty(Ingredient, repeated=True,
                                 verbose_name='Items')
  
  def api_response_data(self):
    return {
      'name': self.name,
      'items': [ x.api_message(as_dict=True) for x in self.items ]
    }