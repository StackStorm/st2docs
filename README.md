[![StackStorm](https://github.com/stackstorm/st2/raw/master/stackstorm_logo.png)](http://www.stackstorm.com)

**StackStorm** is a platform for integration and automation across services and tools, taking
actions in response to events. Learn more at [www.stackstorm.com](http://www.stackstorm.com/product).

[![Build Status](https://circleci.com/gh/StackStorm/st2docs.png?style=shield)](https://circleci.com/gh/StackStorm/st2docs)

# Writing the Docs

Product documentation for StackStorm is maintained in this repository. These docs are built using
[Sphinx](http://www.sphinx-doc.org/en/stable/).

## Contributing

* Fork this repo on GitHub (https://help.github.com/articles/fork-a-repo/).
* Make changes to the docs using your favorite editor.
* To update docs for the latest - i.e. unstable - release of StackStorm, base your changes off the `master` branch.
* To update docs for a released version of StackStorm pick the appropriate version branch (v1.2 etc) and make changes.
* Push changes to your fork.
* Create a pull request (https://help.github.com/articles/creating-a-pull-request/) against StackStorm/st2docs repository
  to upstream the changes.
* Wait for Travis to complete and one of the StackStorm team shall merge the change.

## Build and Run the Docs.

#### Build locally on Linux
Follows these steps to build the docs locally:

Install the dependencies:

For Debian/Ubuntu: ``sudo apt-get install python-dev libssl-dev libldap2-dev libsasl2-dev ldap-utils``

For RHEL/CentOS: `` sudo dnf install python2-devel python3-devel openldap-devel``

```bash
git clone https://github.com/StackStorm/st2docs.git
cd st2docs
make docs
```

Keep in mind that the initial ``make docs`` run will take a while because it needs to install
all the Python dependencies which are needed to build the docs.

`make livedocs` builds the docs and runs the doc site live at [http://localhost:8000](http://localhost:8000) to
validate changes locally prior to committing any code.

#### Run with Docker
```bash
make docker-build
make docker-run
```
This will build a docker image and run it in a container, serving docs live at [http://localhost:8000](http://localhost:8000).
Edit the sources and enjoy live updates.

Before pushing the PR, it's good idea to run a full build and catch any warnings which will fail the official build. Here is how:
```
run --rm -it -v "$PWD"/docs/source:/st2docs/docs/source st2/st2docs /bin/bash -c "make .cleandocs ; make .docs"
```
#### Running docs only

To make docs changes, without installing full development environment (e.g., on Mac or Windows):

```bash
git clone git@github.com:StackStorm/st2docs.git
cd st2docs
make docs
# make docs will fail; ignore the failure:
# it will get st2 and set up virtualenv with sphinx/shinx-autobuild
. virtualenv/bin/activate
sphinx-autobuild -H 0.0.0.0 -b html ./docs/source/ ./docs/build/html
```

Edit, enjoy live updates.

### For Windows users:

1. Install Docker

2. Run Docker QuickStart Terminal.This way these instructions work as-is (otherwise you will need
   to convert these instructions to work with a Windows command prompt)

3. cd to docs directory, e.g.:
   ```bash
   cd /c/Users/stanley/st2docs
   ```
4. activate virtualenv:
   ```bash
   . virtualenv/scripts/activate
   ```
5. Run
   ```bash
   sphinx-autobuild -H 127.0.0.1 -b html ./docs/source/ ./docs/build/html
   ```
6. Connect to http://localhost:8000 Edit files. Watch live updates. Enjoy.

## Sphinx Tricks

* TODO (Use [http://localhost:8000/todo.html](http://localhost:8000/todo.html) for full TODO list (must be empty when we ship):

  ```rst
  .. todo:: Here is a TODO
  ```

* Code fragment:

  ```rst
  .. code-block:: bash

      # List all available triggers
      st2 trigger list
  ```

* Reference the document

  ```rst
  :doc:`/start`
  :doc:`in the Rules doc </rules>`
  ```
* Referencing an arbitrary section: for instance, there's examples section in `sensors.rst`. Define a reference on `examples` section in `sensors.rst`:

  ```rst
  .. _sensors-examples:
  ```

  and point to it as from this, or from other documents as:

  ```rst
  :ref:`sensors-examples`
  :ref:`My examples <sensors-examples>`
  ```

  Note that the leading `_` underscore is gone, and the reference is quoted.

  Name convention for references is `_filename-refname` (because they are unique across the docs).  Note that there is no way to reference just a point in the docs. See http://sphinx-doc.org/markup/inline.html#cross-referencing-syntax

* External links:

  ```rst
  `External link <http://webchat.freenode.net/?channels=stackstorm>`_
  ```

* Inlcude a document, full body:

  ```rst
  .. include:: /engage.rst
  ```

* Link to GitHub st2 repo

  ```rst
  :github_st2:`st2/st2common/st2common/operators.py </st2common/st2common/operators.py>`
  ```

* Link to Github StackStorm-Exchange org:

  ```rst
  :github_exchange:`Link to a sensu pack repo inside Exchange<stackstorm-sensu>`
  ```

* Link to StackStorm Exchange website with a filter query:

  ```rst
  :web_exchange:`Sensu<sensu>`
  ```

* Link to the Exchange website on Github (using a global we set up in source/conf.py)

  ```rst
  `exchange`_
  ```

* The pattern to include an example from `/st2/contrib/examples`: make example file name a reference on github. May say that it is deployed to `/usr/share/doc/st2/examples/`, and auto-include the file:

  ```rst
  Sample rule: :github_st2:`sample-rule-with-webhook.yaml
  </contrib/examples/rules/sample-rule-with-webhook.yaml>` :

  .. literalinclude:: /../../st2/contrib/examples/rules/sample_rule_with_webhook.yaml
      :language: json
  ```

## Pandoc - convert md <-> rst and more

pandoc - a super-tool to convert between formats. Sample for markdown conversion:

```bash
sudo apt-get install pandoc
pandoc --from=markdown --to=rst --output=README.rst README.md
```

## Misc

It's ironic that I use Markdown to write about rST tricks.
