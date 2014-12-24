"""
RL Framework
Authors: Praful Konduru
Environment Base Class; Represented by an MDP
"""

import random
import numpy as np
import networkx as nx
import util
import sys
import pdb

from ProgressBar import ProgressBar

class Environment:
    """Environment represented as an MDP"""
    domain = None
    S = 0
    A = 0
    P = []
    R = {}
    R_bias = 0
    Q = []

    state = 0

    def __init__( self, domain, S, A, P, R, R_bias, start_set, end_set ):
        self.domain = domain
        self.S = S 
        self.A = A 
        self.P = P
        self.R = R
        self.R_bias = R_bias
        self.start_set = start_set
        self.end_set = end_set

        # State action set for MDP
        Q = []
        for s in xrange(self.S):
            Q.append( tuple( ( a for a in xrange( self.A ) if len( self.P[ a ][ s ] ) > 0 ) ) )
        self.Q = Q

    def start( self ):
        """Calls _start - this is to support Options later"""
        return self._start()

    def _start(self):
        """Initialise the Environment
        @returns initial state and valid actions
        """
        if self.start_set:
            state = random.choice( self.start_set )
        else:
            state = np.random.randint( self.S )
            while len( self.Q[ state ] ) == 0:
                state = np.random.randint( self.S )
        self.state = state

        return state

    def react(self, action):
        return self._react( action )

    def _react(self, action):
        state = util.choose( self.P[ action ][ self.state ] )
        reward = self.R.get( (self.state, state), 0 ) + self.R_bias

        # If there is no way to get out of this state, the episode has ended
        if self.end_set is not None:
            episode_ended = state in self.end_set 
        else:
            episode_ended = len( self.Q[ state ] ) == 0

        if episode_ended:
            state = self._start()
        self.state = state

        return state, reward, episode_ended

    def to_graph( self ):
        """Create a graph from the MDP environment"""

        graph = nx.MultiDiGraph()
        # Add all states as nodes
        for i in xrange( self.S ):
            graph.add_node( i )
        for a in xrange( self.A ):
            # Add pr-edges for each action
            for i in xrange( self.S ):
                for (j,pr) in self.P[ a ][ i ]:
                    graph.add_edge( i, j, pr = pr, action = a )

        return graph

    def to_dot( self ):
        """Create a graph from the MDP environment"""

        s = ""
        s += "# Autogenerated rl-domain graph\n"
        s += "digraph{ \n"

        # Add a node for all states
        for i in xrange( self.S ):
            s += '%d [label=""];\n'%( i )
        # Add pr-edges
        for a in xrange( self.A ):
            # Add pr-edges for each action
            for i in xrange( self.S ):
                for (j,pr) in self.P[ a ][ i ]:
                    s += "%d -> %d;\n"%( i, j )
        s += "}\n"
        return s

class Option:
    r"""Encapsulates an option: I, \pi, \beta"""
    I = set([])
    pi = {}
    B_ = {}

    def __init__( self, I, pi, B ):
        self.I = I
        self.pi = pi
        self.B_ = B

    def __repr__(self):
        return "[Option: %s]"%( id( self ) )

    def can_start( self, state ):
        return state in self.I

    def act( self, state ):
        action = util.choose( self.pi[ state ] )
        return action

    def B( self, state ):
        if state in self.B_:
            return self.B_[ state ]
        elif state in self.pi and len( self.pi[ state ] ) > 0:
            return 0.0
        else:
            return 1.0

    def should_stop( self, state ):
        b = self.B( state )
        if b == 1.0:
            return True
        elif b == 0.0:
            return False
        elif np.random.random() < b:
            return True
        else:
            return False

class OptionEnvironment( Environment ):
    """
    Environment that also supports options defines a graph structure
    Note: We don't save actions as options from an efficiency standpoint.
    """
    O = []

    def __init__( self, domain, S, A, P, R, R_bias, start_set, end_set, O ):
        Environment.__init__( self, domain, S, A, P, R, R_bias, start_set, end_set )
        self.O = O

        # Update the Q function based on the options we now have
        Q = []
        for s in xrange(self.S):
            actions = tuple( ( a for a in xrange( self.A ) if len( self.P[ a ][ s ] ) > 0 ) )
            options = tuple( ( o for o in O if s in o.I ) )
            Q.append( actions + options )
        self.Q = Q

    def react( self, action ):
        """
        React to action
        @returns new state and valid actions, and reward, and if episode has
        ended
        """

        if isinstance( action, Option ):
            option = action
            history = []
            rewards = []

            # Act according to the option
            action = option.act( self.state )
            history.append( ( self.state, action ) )

            state, reward, episode_ended = self._react( action )
            rewards.append( reward )

            while not episode_ended and not option.should_stop( state ):
                # Use the option policy 
                action = option.act( state )
                history.append( ( state, action ) )

                state, reward, episode_ended = self._react( action )
                rewards.append( reward )

            history.append( (state, None) )

            return history, tuple(rewards), episode_ended
                
        else:
            return self._react( action )
