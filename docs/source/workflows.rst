Workflows
=========

Typical datacenter operations and processes involve taking multiple actions across various
systems. To capture and automate these operations, |st2| uses workflows. A workflow strings atomic
actions into a higher level automation, and orchestrates their executions by calling the right
action, at the right time, with the right input. It keeps state, passes data between actions, and
provides reliability and transparency to the execution.

Just like any actions, workflows are exposed in the automation library, and can be called
manually, or triggered by rules. Workflows can even be called from other workflows.

To create a workflow action, choose a workflow runner (Mistral or ActionChain), connect the
actions in a workflow definition, and provide the usual action meta data.

|st2| supports two types of workflows - :doc:`ActionChain <actionchain>` and 
:doc:`Mistral <mistral>`.

* :doc:`ActionChain <actionchain>` is |st2|'s internal no-frills workflow runner. It provides a
  simple syntax to define a chain of actions, runs them one after another, passing data from one
  action to another until it succeeds or fails. 

  **Use ActionChain when you want speed and simplicity.**

* :doc:`Mistral <mistral>` is a dedicated workflow service, originated in OpenStack, integrated
  and bundled with |st2|. With Mistral, you can define complex workflow logic with nested
  workflows, forks, joins, and policies for error handling, retries, and delays.

  **Use Mistral when you need power and resilience.**

* :doc:`Orchestra <orchestra/index>` is a new workflow engine, designed specifically for |st2|. It
  is currently in public beta. In future this will replace both Action Chain and Mistral. With
  Orchestra, you can define simple sequential workflows or complex workflows with forks, joins,
  and sophisticated data transformation and queries.

  **Use Orchestra to test-drive the future of workflows.** 

In addition, |st2| offers experimental support for :doc:`CloudSlang <cloudslang>` workflows.

* `CloudSlang <http://www.cloudslang.io/>`_ is a language for defining workflows run by the
  CloudSlang Orchestration Engine. With the CloudSlang runner, you can define your own complex
  workflows or leverage the power of the ready-made CloudSlang `content repository
  <https://github.com/CloudSlang/cloud-slang-content>`_.

Learn how to define and run workflows:

.. toctree::
    :maxdepth: 1

    actionchain
    mistral
    Orchestra <orchestra/index>
    cloudslang
