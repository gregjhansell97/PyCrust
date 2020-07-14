# -*- coding: utf-8 -*-

"""
Monitors function invocations and notifies interested subscribers

Pynoculars uses the observable decorator to create a ObservableFunction wrapper.
Callbacks can subscribe to this wrapper. A subscribed callback is notified when
the function is successfully invoked.

Example:
    ```
        from pynoculars import observable

        # wraps hello_world function (creating an ObservableFunction instance)
        @observable
        def hello_world():
            return "hello world"

        # create callback that counts the number of times hello_world is called
        def hello_world_counter():
            hello_world_counter.count += 1
        hello_world_counter.count = 0

        # subscribe callback to hello_world function
        hello_world.subscribe(hello_world_counter)

        assert hello_world() == "hello world"
        assert hello_world() == "hello world"
        assert hello_world_counter.count == 2
    ```
"""

from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

from pynoculars.observable_function import observable

__all__ = ["observable"]
