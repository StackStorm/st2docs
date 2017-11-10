Troubleshooting Webhooks
========================

You may run into some issues with getting |st2| to respond to :doc:`Webhooks </webhooks>` the way you want. A common problem
that community members run into is that |st2| doesn't seem to recognize or respond to incoming webhooks,
even if a manual test using ``curl`` results in a successful HTTP status.

The first thing to do is confirm that the webhook request is indeed getting to |st2|. When webhooks successfully
hit the |st2| API, you will see messages similar to below in the ``st2api`` log (``/var/log/st2/st2api.log``):

.. sourcecode:: text

    2017-11-09 21:21:00,563 140040790988752 INFO logging [-] 651897d7-2aed-4a11-9c14-4c56152230cc - POST /v1/webhooks/st2 with query={} (remote_addr='127.0.0.1',method='POST',request_id='651897d7-2aed-4a11-9c14-4c56152230cc',query={},path='/v1/webhooks/st2')
    2017-11-09 21:21:00,566 140040790988752 AUDIT auth [-] Token with id "5a04be6bc4da5f0d1fe22ca1" is validated.
    2017-11-09 21:21:00,572 140040790988752 INFO logging [-] 651897d7-2aed-4a11-9c14-4c56152230cc - 202 94 8.623ms (content_length=94,request_id='651897d7-2aed-4a11-9c14-4c56152230cc',runtime=8.623,remote_addr='127.0.0.1',status=202,method='POST',path='/v1/webhooks/st2')

If you don't see these, the actual request isn't even making it to |st2| at all. You should look at anything
along the path between the requester and |st2| and ensure that nothing is blocking that communication. Don't
forget to look at the NGINX logs as well, as this front-ends all API communication, including webhooks, in a
normal setup.

You may also be running |st2| with a self-signed certificate. Be sure that the webhook sender isn't rejecting
the connection because of this, as that will prevent the webhook from ever being sent. In this case, you won't
even see a successful connection in the nginx logs.

However, if you **are** seeing successful ``POST`` requests showing up in the ``st2api`` log but you still aren't
seeing the resulting trigger instances in the output of ``st2 trigger-instance list``, there's likely a problem
with the webhook payload. The best place to look for more information on this is the ``st2rulesengine``
log (``/var/log/st2/st2rulesengine.log``). For instance, if you're using the built-in ``st2`` webhook, this
log message will show if the specified trigger doesn't exist:

.. sourcecode:: text

    2017-11-09 20:45:52,006 140146899259632 ERROR consumers [-] StagedQueueConsumer failed to process message: {'trace_context': <st2common.models.api.trace.TraceContext object at 0x7f767ded7290>, 'trigger': u'default.badtrigger', 'payl
    oad': {u'attribute1': u'value1'}}
    Traceback (most recent call last):
      File "/opt/stackstorm/st2/local/lib/python2.7/site-packages/st2common/transport/consumers.py", line 85, in process
        response = self._handler.pre_ack_process(body)
      File "/opt/stackstorm/st2/local/lib/python2.7/site-packages/st2reactor/rules/worker.py", line 54, in pre_ack_process
        raise_on_no_trigger=True)
      File "/opt/stackstorm/st2/local/lib/python2.7/site-packages/st2reactor/container/utils.py", line 70, in create_trigger_instance
        raise StackStormDBObjectNotFoundError('Trigger not found for %s', trigger)
    StackStormDBObjectNotFoundError: ('Trigger not found for %s', u'default.badtrigger')

The vast majority of webhook issues fall into one of these two buckets, and these log files should help point
you in the right direction.
