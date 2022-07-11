'''Testing Worldstates

We're gonna going to have to test a lot of things!

First off:
- Location Dependent World State
- Multiple actions in one timestep
- Actually, we also need to bring back timesteps

Timestep
- Each timestep contains multiple story parts and its own World State

StoryGraph
- Rewrite it to support adding multiple nodes

StoryNode
- Add a "Timestep" property to it, to prevent events from different timesteps from being used together
'''