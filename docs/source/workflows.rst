Workflows
=========

Typical datacenter operations and processes involve taking multiple actions across various
systems. To capture and automate these operations, |st2| uses workflows. A workflow strings atomic
actions into a higher level automation, and orchestrates their executions by calling the right
action, at the right time, with the right input. It keeps state, passes data between actions, and
provides reliability and transparency to the execution.

Just like any actions, workflows are exposed in the automation library, and can be called
manually, or triggered by rules. Workflows can even be called from other workflows.

To create a workflow action, choose a workflow runner, connect the actions in a workflow definition,
and provide the usual action meta data.

|st2| supports two types of workflows - :doc:`Orquesta <orquesta/index>` and :doc:`ActionChain <actionchain>`.

* :doc:`Orquesta <orquesta/index>` is a new workflow engine, designed specifically for |st2|, released
  in 2019. With Orquesta, you can define simple sequential workflows or complex workflows with forks, joins,
  and sophisticated data transformation and queries. It has replaced the Mistral workflow engine, and will
  also replace ActionChains. We recommend you write all new workflows in Orquesta.

  **Use Orquesta for all new workflows.** 

* :doc:`ActionChain <actionchain>` is |st2|'s legacy internal no-frills workflow runner. It provides a
  simple syntax to define a chain of actions, runs them one after another, passing data from one
  action to another until it succeeds or fails. It does not provide any complex workflow handling.

  **Use ActionChain for simple legacy workflows.**

Mistral workflows are no longer supported. See https://github.com/StackStorm/orquestaconvert for a tool to
convert Mistral workflows to Orquesta.

Learn how to define and run workflows:

.. toctree::
    :maxdepth: 1

    Orquesta <orquesta/index>
    actionchain
