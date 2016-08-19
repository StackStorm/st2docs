Tuning action runner dispatcher pool size
=========================================

When action runner executes actions it uses two internal green thread pools -
one for regular actions and one for workflows. Both of those pools have a hard
limit on the maximum size (by default that is ``40`` green threads for
workflows and ``60`` green threads for non-workflow actions).

This hard limit is there to prevent resource exhaustion and to allow for a fair
distribution across multiple action runner processes.

In some situations, such as if you have a lot of action-chain workflows with a
delay policy this limit being hit can cause a deadlock to occur (this deadlock
can be reset by restarting action runner process which has dead locked).

To prevent such issues from occurring and to allow for a good server and action
runner process resource utilization you should adjust those pool sizes bases on
your configuration and workload.

As mentioned above, those settings are very hardware and workload specific (
how many action runner processes do you run and on how many servers, what kind
of actions are being executed - long running vs short running, CPU intensive
vs non-CPU intensive. etc.).

To be able to to effectively tune those limits you should monitor the following
parameters:

* Sizes of the RabbitMQ queues relating to the action executions
* Action runner process resource usage (CPU and memory)

Once you have established baselines and have a good idea of your resource
utilization and workloads you can increase resource utilization and prevent
deadlocks by tuning pool sizes and / or increasing / decreasing the number of
action runner processes.

You can tune pool sizes by changing settings in ``st2.conf`` as shown below.

.. sourcecode:: ini

    [actionrunner]
    # Internal pool size for dispatcher used by workflow actions.
    workflows_pool_size = 40

    # Internal pool size for dispatcher used by regular actions.
    actions_pool_size = 60
