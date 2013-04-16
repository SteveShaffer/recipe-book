#!/usr/bin/env python

import json
import logging

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
    obj = cls() #NOTE: Assumes no required attributes
    obj.process_api_message(message)
    return obj
    
  def update_from_api_message(self, message):
    try:
      self.process_api_message(message)
      return self
    except:
      return None

class Account(AppModel):
  #Key: User ID

  name = ndb.StringProperty()
  user = ndb.UserProperty(auto_current_user_add=True)
  
  @classmethod
  def get_for_current_user(cls):
    """Returns the current user's account (and creates it if it doesn't exist)


    :return: The current user's account model from the datastore
    """
    return cls.get_or_insert(users.get_current_user().user_id())

  @classmethod
  def get_login_url(cls, destination='/'):
    """Returns a URL that will send the user to a login page

    :param destination: URL the user should be redirected to after logging in
    :return: URL to redirect the user's browser to in order to log the user in
    """
    return users.create_login_url(destination)

  @classmethod
  def get_logout_url(cls, destination='/'):
    """Returns a URL that will log the current user out

    :param destination: URL the user should be redirected to after logging out
    :return: URL to redirect the user's browser to in order to log the user out
    """
    return users.create_logout_url(destination)

  def api_response_data(self):
    name = self.name if self.name else self.user.nickname()
    return {
      'name': name,
      'email': self.user.email()
    }

  def process_api_message(self, message):
    if 'name' in message: self.name = message['name']
    self.put()
  #TODO: Continue implementing?

class Measure(AppModel):
  quantity = ndb.FloatProperty(verbose_name='Quantity')
  unit = ndb.StringProperty(verbose_name='Unit')
  
  def api_response_data(self):
    return {
      'quantity': self.quantity,
      'unit': self.unit,
      'text': ' '.join([str(self.quantity), str(self.unit)])
    }
  
  def process_api_message(self, message):
    if 'quantity' in message: self.quantity = message['quantity']
    if 'unit' in message: self.unit = message['unit']
  
class Tag(AppModel):
  description = ndb.StringProperty(verbose_name='Description')
  
  def api_response_data(self):
    return { 'description': self.description }
  
  def process_api_message(self, message):
    #TODO: Implement (and then use below)
    pass

class Ingredient(Measure):
  description = ndb.StringProperty(verbose_name='Description')
  
  def api_response_data(self):
    return {
      'quantity': self.quantity,
      'unit': self.unit,
      'description': self.description,
      'text': ' '.join([ x for x in [ self.quantity,
                                      self.unit,
                                      self.description] if x ])
    }
  
  def process_api_message(self, message):
    #TODO: Implement (and then use below)
    pass
  
class Instruction(AppModel):
  description = ndb.StringProperty(verbose_name='Description')
  
  def api_response_data(self):
    return { 'description': self.description }
  
  def process_api_message(self, message):
    #TODO: Implement (and then use below)
    pass

class Recipe(AppModel):
  name = ndb.StringProperty(default='New Recipe', verbose_name='Name')
  description = ndb.StringProperty(verbose_name='Description')
  makes = ndb.StructuredProperty(Measure)
  serves = ndb.StructuredProperty(Measure) #unit='People' #TODO: Implement somehow
  cooking_time = ndb.StructuredProperty(Measure) #unit='Minutes' #TODO: Implement somehow
  rating = ndb.FloatProperty(verbose_name='Rating')
  tags = ndb.StructuredProperty(Tag, repeated=True, verbose_name='Tags')
  ingredients = ndb.StructuredProperty(Ingredient, repeated=True,
                                       verbose_name='Ingredients')
  instructions = ndb.StructuredProperty(Instruction, repeated=True,
                                        verbose_name='Instructions')
  
  def api_response_data(self):
    return {
      'id': self.key.id() if self.key else None,
      'name': self.name,
      'description': self.description,
      'makes': self.makes.api_message(as_dict=True) if self.makes else {},
      'serves': self.serves.api_message(as_dict=True) if self.serves else {},
      'cooking_time': self.cooking_time.api_message(as_dict=True)
        if self.cooking_time else {},
      'rating': self.rating,
      'tags': [ x.api_message(as_dict=True) for x in self.tags ],
      'ingredients': [ x.api_message(as_dict=True) for x in self.ingredients ]
        if 'ingredients' in self._properties else [],
      'instructions': [ x.api_message(as_dict=True)
                        for x in self.instructions ]
        if 'instructions' in self._properties else []
    }
  
  def process_api_message(self, message):
    if 'name' in message: self.name = message['name']
    if 'description' in message: self.description = message['description']
    if 'makes' in message:
      self.makes = Measure.create_from_api_message(message['makes'])
    if 'serves' in message:
      self.serves = Measure.create_from_api_message(message['serves'])
    if 'cooking_time' in message:
      self.cooking_time = Measure.create_from_api_message(message['cooking_time'])
    if 'rating' in message: self.rating = message['rating']
    #if 'tags' in message: self.tags = message['tags'] #TODO: Reimplement
    if 'ingredients' in message:
      self.ingredients = [ Ingredient.create_from_api_message(x)
                           for x in message['ingredients'] ]
    if 'instructions' in message:
      self.instructions = [ Instruction.create_from_api_message(x)
                            for x in message['instructions'] ]
    logging.info('****recipe: ' + str(self))
    self.put()
    
  @classmethod
  def delete(cls, recipe_id):
    ndb.Key('Recipe', recipe_id).delete()
  
class ShoppingList(AppModel):
  name = ndb.StringProperty(default='My Shopping List', verbose_name='Name')
  items = ndb.StructuredProperty(Ingredient, repeated=True,
                                 verbose_name='Items')
  
  def api_response_data(self):
    return {
      'name': self.name,
      'items': [ x.api_message(as_dict=True) for x in self.items ]
    }