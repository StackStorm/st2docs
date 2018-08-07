Orquesta
========

.. warning::
   Orquesta is currently in beta and features are subject to change.

Orquesta is a workflow engine designed specifically to run natively in |st2|. The goal is to
replace ActionChain and Mistral in the future. Orquesta's workflow definition is described in
YAML and contains a number of changes and improvements over its predecessors. The workflow
definition supports simple sequential workflows to complex workflows with forks, joins, and
sophisticated data queries and transformation. Since Orquesta runs as a subcomponent of |st2|,
it does not require a separate authentication system and database like Mistral.

.. toctree::
   :maxdepth: 2

   Overview <overview>
   Getting Started <start>
   Workflow Definition <languages/orquesta>
   Expressions and Context <expressions>
   Workflow Operations <operations>
   Upcoming Features <upcoming>
