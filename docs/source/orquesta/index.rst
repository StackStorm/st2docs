Orquesta
========

Orquesta is a workflow engine designed specifically to run natively in |st2|. It has replaced
the Mistral workflow engine, and the goal is to replace ActionChain in the future. Orquesta's
workflow definition is described in YAML and contains a number of changes and improvements over
its predecessors. The workflow definition supports simple sequential workflows to complex
workflows with forks, joins, and sophisticated data queries and transformation. Orquesta
does not require a separate authentication system and database like Mistral did.

.. toctree::
   :maxdepth: 2

   Overview <overview>
   Getting Started <start>
   Workflow Definition <languages/orquesta>
   Expressions and Context <expressions>
   StackStorm Runtime <stackstorm>
   Workflow Operations <operations>
   Upcoming Features <upcoming>
   Development <development/index>
