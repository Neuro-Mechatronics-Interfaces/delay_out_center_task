""" An interface to a behavioral task environment.

This module defines an interface to an environmental context in which a 
behavioral task operates. A behavioral goal is typically defined in terms of 
the state of the environment, and the objective of a task is to manipulate 
the environment in order to achieve that goal state.

This class is intended as an example and a testing mechanism, but also as a 
means for declaring the expectations of the task model. Any implementation of 
the environment should be a derivative of this class.

The environment is expected to provide a clock, and a mechanism for setting 
timers. For this purpose, this example / interface uses the [Timer] class from 
the [threading] standard package. This should be replaced with whatever clock 
is implementation-appropriate.

[threading]: https://docs.python.org/3/library/threading.html

[Timer]: https://docs.python.org/3/library/threading.html#timer-objects

"""

# Copyright 2022 Carnegie Mellon University Neuromechatronics Lab (a.whit)
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Contact: a.whit (nml@whit.contact)


# Imports.
from threading import Timer


# Environment class.
class Environment:
    """ A simple environment interface for tasks involving interaction between 
        a spherical cursor and targets in a 3-dimensional space.
        
    This environment class is primarily intended for (a) defining the interface 
    for spherical cursor tasks, and (b) acting as a simple stand-in for testing 
    purposes.
    
    In addition to object attribute accessor functions, this class provides 
    functionality for testing interaction between spherical objects.
    
    Attributes
    ----------
    radius : dict of floats
        A mapping between object keys and radius values.
    position : dict of 3-tuples of floats
        A mapping between object keys and tuples of 3D spatial coordinates.
    
    Examples
    --------
    
    Initialize a new environment.
    
    >>> environment = Environment()
    
    Verify that a `cursor` object has been initialized in the environment, that 
    the object is a unit sphere, and that it is positioned at the origin.
    
    >>> environment.objects
    {'cursor': {'radius': 1.0, 'position': (0.0, 0.0, 0.0)}}
    
    Initialize a target sphere, and verify that the two spheres overlap.
    
    >>> environment.initialize_sphere(key='target')
    >>> environment.is_engaged('target')
    True
    
    Set the position away from the origin, and verify that the two spheres 
    still overlap.
    
    >>> environment.set_position(x=1.0, key='target')
    >>> environment.get_position('target')
    (1.0, 0.0, 0.0)
    >>> environment.is_engaged('target')
    True
    
    Shrink the radii of the `cursor` and `target` spheres, and verify that the 
    spheres are still (barely) touching.
    
    >>> environment.set_radius(0.5, key='cursor')
    >>> environment.set_radius(0.5, key='target')
    >>> environment.is_engaged('target')
    True
    
    Further shrink the radius of the `cursor` sphere, and verify that it no 
    longer touches the `target`.
    
    >>> environment.set_radius(0.1, key='cursor')
    >>> environment.is_engaged('target')
    False
    
    Restore the radii to the default, and move the target. Verify that the 
    spheres once again overlap.
    
    >>> environment.set_radius(key='cursor')
    >>> environment.set_radius(key='target')
    >>> environment.set_position(1.0, 1.0, 0.0, key='target')
    >>> environment.is_engaged('target')
    True
    
    Reduce the radii, and verify that the spheres no longer touch.
    
    >>> environment.set_radius(0.707, key='cursor')
    >>> environment.set_radius(0.707, key='target')
    >>> environment.is_engaged('target')
    False
    
    """
    
    def __init__(self):
        
        # Initialize the spherical object attributes.
        self.objects = {}
        
        # Initialize a timer callable.
        self.timer = Timer
        
        # Initialize a cursor object.
        self.initialize_sphere()
        
    def exists(self, key):
        """ Test whether or not an object exists in the environment. """
        return key in self.objects
        
    def initialize_sphere(self, key='cursor'):
        """ Initialize a sphere object.
        
        Parameters
        ----------
        key : string
            Key or label used to identify the sphere object.
        """
        assert key not in self.objects
        self.objects[key] = {}
        self.set_radius(key=key)
        self.set_position(key=key)
    
    def destroy_sphere(self, key='cursor'):
        """ Destroy a sphere object.
        
        Parameters
        ----------
        key : string
            Key or label used to identify the sphere object.
        """
        if key in self.objects: del self.objects[key]
    
    def get_radius(self, key='cursor'):
        """ Get the current size of a sphere object.
        
        Parameters
        ----------
        key : string
            Key or label used to identify the object.
        """
        return self.objects[key]['radius']
        
    def set_radius(self, radius=1.0, key='cursor'):
        """ Set the current size of a sphere object.
        
        Parameters
        ----------
        radius : float
            Size of the target sphere.
        key : string
            Key or label used to identify a sphere object.
        """
        assert key in self.objects
        self.objects[key]['radius'] = radius
        
    def get_position(self, key='cursor'):
        """ Get the current position in space of the center of a sphere object.
        
        Parameters
        ----------
        key : string
            Key or label used to identify the object.
        """
        return self.objects[key]['position']
        
    def set_position(self, x=0.0, y=0.0, z=0.0, key='cursor'):
        """ Set the current position of an object in space.
        
        Parameters
        ----------
        x : float
            First position coordinate.
        y : float
            Second position coordinate.
        z : float
            Third position coordinate.
        key : string
            Key or label used to identify the object.
        """
        assert key in self.objects
        self.objects[key]['position'] = (x, y, z)
        
        
        
    # The remaining functions should be removed or replaced, when possible.
        
        
        
    def set_target_radius(self, radius=0.0, key='target'):
        """ Set the current size of the target sphere.
        
        Parameters
        ----------
        radius : float
            Size of the target sphere.
        key : string
            Key or label used to identify a target.
        """
        self.radius[key] = radius
        
    def set_target_position(self, *args, key='target', **kwargs):
        """ Set the current position of the target in behavioral space.
        
        Parameters
        ----------
        x : float
            First position coordinate.
        y : float
            Second position coordinate.
        z : float
            Third position coordinate.
        key : string
            Key or label used to identify a target.
        """
        self.set_position(*args, key=key, **kwargs)

    def set_cursor_position(self, x=0.0, y=0.0, z=0.0):
        """ Set the current position of the cursor in behavioral space.
        
        Parameters
        ----------
        x : float
            First position coordinate.
        y : float
            Second position coordinate.
        z : float
            Third position coordinate.
        """
        self.set_position(*args, key='cursor', **kwargs)
        
    def is_engaged(self, key='target'):
        """ Tests whether or not the cursor overlaps with, or touches, a target 
            sphere.
        
        Parameters
        ----------
        key : string
            Key or label used to identify a target.
        """
        p_t = self.objects[key]['position']
        p_c = self.objects['cursor']['position']
        d = sum([(t-c)**2 for (t, c) in zip(p_t, p_c)])
        r_t = self.objects[key]['radius']
        r_c = self.objects['cursor']['radius']
        
        return d <= (r_t + r_c)**2
    
  

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
  

