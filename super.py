#!/usr/bin/python
class Padre(object):
  def unicode(self):
    return 'Padre'

class Hijo(Padre):
  def unicode(self):
    return super(Hijo,self).unicode() + '-Hijo'

h=Hijo()
print h.unicode()
