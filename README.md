Kleinberg-network-learning
==========================

Exploring the use of options in creating small worlds for faster learning in Reinforcement Learning Domains
Exploring the Small World Effect in Reinforcement Learning
----------------------------------------------------------

In large domains, RL agents generally require a large number of samples to
learn a good policy. The options framework proposed by Sutton, Precup and Singh
provides extended actions for which a policy is already learnt, reducing the
complexity of the learning task, and generally making the learning task faster.
An open question in the options framework is discovering the options
themselves.  There has been substantial work to learn options, mainly focussed
around identifying ``bottleneck'' states, either empirically, or
more recently, using graph theoretic methods like betweeness or
graph partitions.

We would like to test an alternative hypothesis; we memorise many actions,
not necessarily bottleneck ones, and put them together; based on their
necessity in solving problems these actions are either reinforced, or gradually
forgotten.  The actions could be of varying complexity, and it is intuitive to
expect that we probably learn a great deal more _simple_ actions than
complex ones. In context of the options framework, the ``complex actions''
correspond to options.

Our proposed approach is to use randomly constructed options that create a
'short-cut' between states, forming a sort of 'small-world' in the domain. This
approach can be viewed as an extension of Kleinberg's popular model in the
Social Network Analysis field, and we would like to note that RL domains are
very grid-like as well. The analogy is further motivated by observing that the
policy followed by an agent in the MDP framework is like distributed search; we
are interested in moving from our source state to the destination (goal) state
using only information available locally, i.e. the value function. We leave
addressing the dynamics of such random options, i.e.  when options are added or
removed, as future work.
