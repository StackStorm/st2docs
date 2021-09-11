Database Models and Abstractions
================================

In |st2| interaction with the database (MongoDB) is handled via the database models. Those
models expose an ORM like interface and are built on top of the the ``mongoengine`` library.

Most of the code for handling the database interactions and persistence is located in the
following locations:

* https://github.com/StackStorm/st2/tree/master/st2common/st2common/models/db - database models
* https://github.com/StackStorm/st2/tree/master/st2common/st2common/persistence - code for
  storing models in the database, retrieving them, querying the database, etc.

Database Field Types
--------------------

For the most part we utilize native MongoDB field types such as strings and objects (dictionaries
/ nested documents).

|st2| v3.5.0 introduced some changes to the database models where we now store execution result
(``ActionExecutionDB.result``) field and various other fields which can can contain a lot data
in a binary field as a serialized JSON string.

This format is much more efficient (in terms of retrieving and storing the field value in the
database and also in terms of disk space) than the field type we used previously. Per benchmarking
results and end to end load testing, storing those models with the new field types can be up to
15x faster.

The change is fully opaque to the end user since it's handled transparently by our ORM layer
/ database models code.

If for some reason you want or need to view the raw binary field value, you can use the following
code inside MongoDB shell:

.. sourcecode:: bash

    # Let's assume execution you are interested in has ID 604bdf055779c52cbe31a476

    > use st2;
    switched to db st2

    > function hex2a(hex) {
    ...     var str = '';
    ...     for (var i = 0; i < hex.length; i += 2)
    ...         str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    ...     return str;
    ... }

    > document = db.action_execution_d_b.find({"_id": ObjectId("604bdf055779c52cbe31a476")}, {status:1, start_timestamp: 1, end_timestamp: 1, result: 1})[0];
    {
        "_id" : ObjectId("604bdf055779c52cbe31a476"),
        "result" : BinData(0,"eyJmYWlsZWQiOmZhbHNlLCJzdWNjZWVkZWQiOnRydWUsInJldHVybl9jb2RlIjowLCJzdGRvdXQiOiJoZWxsbyB3b3JsZCIsInN0ZGVyciI6IiJ9"),
        "start_timestamp" : NumberLong("1615585029623199"),
        "status" : "succeeded",
        "end_timestamp" : NumberLong("1615585029987208")
    }

    > hex2a(document.result.hex())
    {"failed":false,"succeeded":true,"return_code":0,"stdout":"hello world","stderr":""}

Keep in mind that this code is here only for illustrative purposes. Only official way for
interacting with the database is using ORM layer so if you start manually changing data using
mongo shell there is no guarantee things will work and you are doing it at your own risk.
