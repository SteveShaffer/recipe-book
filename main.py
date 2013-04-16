#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json

import models
    
class MainPageRedirectHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect('/app/')

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect(models.Account.get_login_url())

class LogoutHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect(models.Account.get_logout_url())
    
#----API----#

class ApiHandler(webapp2.RequestHandler):

  def write_json(self, value, convert=False):
    self.response.headers['Content-Type'] = 'application/json'
    if convert:
      message = json.dumps(value)
    else:
      message = value
    self.response.out.write(message)

class AccountHandler(ApiHandler):

  model = models.Account

  def get(self):
    self.write_json(self.model.get_for_current_user().api_message())

  def post(self):
    message = json.loads(self.request.body)
    obj = self.model.get_for_current_user().update_from_api_message(message)
    self.write_json(obj.api_message())
    
class RecipeListHandler(ApiHandler):
  
  model = models.Recipe
  
  #LIST Recipes
  def get(self): self.write_json(self.model.api_list_message())
  
  #NEW Recipe
  def post(self):
    message = json.loads(self.request.body)
    obj = self.model.create_from_api_message(message)
    self.write_json(obj.api_message()) #TODO: Add Location header?
                                       #      perform redirect?

class RecipeHandler(ApiHandler):
  
  model = models.Recipe
  
  #READ Recipe
  def get(self, recipe_id):
    self.write_json(self.model.get_by_id(int(recipe_id)).api_message())
  
  #UPDATE Recipe
  def post(self, recipe_id):
    message = json.loads(self.request.body)
    obj = self.model.get_by_id(int(recipe_id))
    obj.update_from_api_message(message)
    self.write_json(obj.api_message())
    
  #DELETE Recipe
  def delete(self, recipe_id):
    models.Recipe.delete(int(recipe_id))
    self.response.set_status(204)

app = webapp2.WSGIApplication([
  ('/', MainPageRedirectHandler),
  ('/app', MainPageRedirectHandler),
  ('/login', LoginHandler),
  ('/logout', LogoutHandler),
  ('/user', AccountHandler),
  ('/recipes/?', RecipeListHandler),
  ('/recipes/(.*)/?', RecipeHandler)
], debug=True)
