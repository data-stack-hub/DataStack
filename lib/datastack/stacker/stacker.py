import hashlib
import inspect
from contextlib import contextmanager
from datastack.runtime import runtime
from datastack.logger import logger
from datastack.server import caching
from datastack.connections.sql_connection import SQLConnection
import uuid, os, json
import numpy as np
import time, threading
from pathlib import Path
from varname import argname
from varname import varname
from typing import Iterable, Optional, Callable, Tuple

# from datastack.server.server import seesion_mgr


class datastack:
    """
    Datastack class for holding all widgets

    Parameters
    ----------
    type: str main_page | sidebar | container | column | tab | None

    path: str
        Path for pages

    title: str
        Title of container or tabs

    main: bool
        True value idenfify the class instance as main class where as false value identify as subclass
    """

    def __init__(self, type="main_page", path="", title="", main=False):
        """Inserts or updates elements in the datstack apps."""

        self.type = type
        self.title = title
        self.path = path
        self.main = main

        self.app = {
            "current_page": "main_page",
            "sidebar": [],
            "main_page": [],
            "pages": [],
            "appstate": {
                # "session_id": getattr(threading.current_thread(), "session_id"),
                "notifications": [],
            },
        }

        self.blocks = {"sidebar": [], "main_page": [], "pages": []}
        self.state = {}

        if main:
            self.session_id = getattr(threading.current_thread(), "session_id")
            self.app["appstate"]["session_id"] = getattr(
                threading.current_thread(), "session_id"
            )
            setattr(threading.current_thread(), "STACKER_CLASS", self)
        # to be checked if this is required
        # if main:
        #     runtime.set_main_class(self)
        #     runtime.collect_cls(self)

    def dynamic_widget_id(self):
        # return str(time.time_ns())
        return str(uuid.uuid4())

    def button(
        self,
        name: str,
        on_click: Optional[callable] = None,
        args: Optional[Tuple] = None,
        id: Optional[str] = None,
    ):
        """Button widget.

        Parameters
        ----------
        name : str
            A name of button, clerly explain the purpouse of button to user.

        on_click : callable
            callable function to invoke when button is clicked

        args : tuple
            An optional tuple of args to pass to the callback.

        Examples
        --------
        Simple button

        >>> ds.button('Click')

        Button on_click

        >>> count = 0
        >>>
        >>> def click():
        ...     global count
        ...     count += 1
        >>>
        >>> ds.button('Click', on_click=click)
        >>> ds.write('Count = {}'.format(count), id='count')
        """

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "button",
            "prop": {
                "title": name,
                # "on_change_source": click_fn,
                "title_var": argname("name", func=self.button),
                "args": args,
            },
        }
        try:
            block["prop"]["on_change"] = argname(
                "on_click", vars_only=False, func=self.button
            )
        except:
            pass

        if not self.replace_block(id, block):
            self.append_block(block)

    def input(
        self,
        label: str = None,
        value: str | None = "",
        id: Optional[str] = None,
        on_change: Optional[callable] = "",
        args: Optional[Tuple] = None,
    ):
        """Display a single-line text input widget

        Parameters
        ----------

        label : str
            A short label explaining to the user what this input is for.

        value : str or None
            The text value of this element when it first renders.

        id : str
            An optional string or integer to use as the unique key for the element.

        on_change : callable
            An option callback invoked when this text input's value chnages.

        args : dict
            An optional tuple of args to pass to the callback

        Examples
        --------

        >>> name = ds.input('Name')
        >>> ds.write('your name: ' + name)

        """
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "input",
            "prop": {
                "label": label,
                "value": value,
                "args": args,
            },
        }
        try:
            block["prop"]["on_change"] = argname(
                "on_click", vars_only=False, func=self.input
            )
        except:
            pass

        try:
            block["prop"]["value_var"] = varname()
        except:
            pass

        if not self.replace_block(id, block):
            self.append_block(block)
        return value

    def divider(self):
        """A divider line separates different content.

        Examples
        --------
        >>> ds.divider()
        """

        block = {"id": self.dynamic_widget_id(), "type": "divider", "prop": {}}
        self.append_block(block)

    def header(self, data, id: Optional[str] = None):
        """Display text in header formatting.

        Parameters
        ----------

        data : str
            The text to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.header('This is header')

        """

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "header",
            "prop": {"data": data, "data_var": str(argname("data", vars_only=False))},
        }

        try:
            block["prop"]["data_var"] = argname("data")
        except:
            pass

        if not self.replace_block(id, block):
            self.append_block(block)

    def subheader(self, data, id: Optional[str] = None):
        """Display text in subheader formatting.

        Parameters
        ----------

        data : str
            The text to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.subheader('This is subheader')

        """

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "subheader",
            "prop": {"data": data, "data_var": str(argname("data", vars_only=False))},
        }
        if not self.replace_block(id, block):
            self.append_block(block)

    def select(
        self,
        label: str,
        options: Iterable = [],
        value: str | None = "",
        id: Optional[str] = None,
        on_change: Optional[callable] = "",
        args: Optional[Tuple] = None,
    ):
        """Select component to select value from options

        Parameters
        ----------
        label : str
            A short label explaining to the user what this input is for.

        options : Itrerable
            Options for select element.

        value : str or None
            The text value of this element when it first renders.

        id : str
            An optional string or integer to use as the unique key for the element.

        on_change : callable
            An option callback invoked when this text input's value chnages.

        args : dict
            An optional tuple of args to pass to the callback

        Examples
        --------

        >>> operating_system = ds.select('Select operating system', ['ios', 'android', 'windows'])
        >>> ds.write('You selected: ' + operating_system)
        """

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "select",
            "prop": {
                "options": [opt for opt in options],
                "label": label,
                "value": value,
                "value_var": varname(),
                "args": args,
            },
        }

        try:
            block["prop"]["on_change"] = argname(
                "on_change", vars_only=False, func=self.select
            )
        except:
            print("error on change function")

        try:
            block["prop"]["options_var"] = str(argname("options", vars_only=False))
        except Exception as e:
            print(e)

        if not self.replace_block(id, block):
            self.append_block(block)
        return value

    def radio_button(
        self,
        label: str = "",
        options: Iterable = [],
        value: str | None = "",
        id: Optional[str] = None,
        on_change: Optional[callable] = "",
        args: Optional[Tuple] = None,
    ):
        """Display a radio button element

        Parameters
        ----------

        label : str
            A short label explaining to the user what this input is for.

        options : Itrerable
            Options for select element.

        value : str or None
            The text value of this element when it first renders.

        id : str
            An optional string or integer to use as the unique key for the element.

        on_change : callable
            An option callback invoked when this text input's value chnages.

        args : dict
            An optional tuple of args to pass to the callback

        Examples
        --------

        >>> operating_system = ds.radio_button('Select operating system', ['ios', 'android', 'windows'])
        >>> ds.write('You selected: ' + operating_system)
        """
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "radio_button",
            "prop": {
                "options": [opt for opt in options],
                "label": label,
                "value": value,
                "on_change": "" if on_change == "" else argname("on_change"),
            },
        }
        try:
            block["prop"]["value_var"] = varname()
        except:
            pass

        try:
            block["prop"]["options_var"] = str(
                argname("options", vars_only=True, func=self.radio_button)
            )
        except:
            print()

        if not self.replace_block(id, block):
            self.append_block(block)
        return value

    def list(
        self,
        data: Iterable = [],
        on_click: Optional[Callable] = None,
        id: Optional[str] = None,
    ):
        """Display list element

        Parameters
        ----------

        data : Iterable
            Iterable list to display

        on_click : Callable
            An option callback invoked when this list is clicked.

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> selected_lan = ds.list(['python', 'javascript', 'java', 'c++', 'pascal'])
        >>> ds.write('your favourite language: ' + selected_lan)

        """
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "list",
            "prop": {
                "data": data,
                "value": "",
            },
        }
        try:
            block["prop"]["on_change"] = argname(
                "on_change", vars_only=False, func=self.list
            )
        except:
            pass

        try:
            block["prop"]["value_var"] = varname()
        except:
            pass

        if not self.replace_block(id, block):
            self.append_block(block)

        return "none"

    def menu(
        self,
        data: Iterable,
        mode: str = "horizontal",
        value: Optional[str] = None,
        id: Optional[str] = None,
        on_change: Optional[callable] = None,
    ):
        """Display menu

        Parameters
        ----------

        data : Iterable
            data to be displayed in the menu.

        mode : vertical | horizontal | inline
            Mode of menu display

        value : str or None
            The text value of this element when it first renders.

        id : str
            An optional string or integer to use as the unique key for the element.

        on_change : callable
            An option callback invoked when this text input's value chnages.

        Examples
        --------

        >>> page = ds.menu(['Page1', 'Page2', 'Page3'])
        >>> ds.header(page)
        """

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "menu",
            "prop": {"data": data, "value": value, "mode": mode},
        }
        try:
            block["prop"]["value_var"] = varname()
        except:
            pass

        try:
            block["prop"]["on_change"] = argname(
                "on_change", vars_only=False, func=self.menu
            )

        except Exception as e:
            print(e)

        if not self.replace_block(id, block):
            self.append_block(block)
        return value

    def notification(self, data: str):
        """Diaplay a short message

        Parameters
        ----------

        data : str
            The string to display
        """
        data["notification_id"] = self.dynamic_widget_id()
        self.app["appstate"]["notifications"].append(data)

    def clear_notifications(self):
        """Clear all notifications"""
        self.app["appstate"]["notifications"] = []

    # def get_value_assign_var(self, f):
    #     import dis

    #     """
    #     # method 1
    #     frame = inspect.currentframe()
    #     frame = inspect.getouterframes(frame)[1]
    #     s = inspect.getframeinfo(frame[0])
    #     code = inspect.currentframe().f_back.f_code
    #     print('code', dis.code_info(code))

    #     it = iter(dis.get_instructions(code))
    #     for instr in it:
    #         if instr.offset == inspect.currentframe().f_back.f_lasti:
    #             print('inspect',instr)
    #             break
    #     assert instr.opname.startswith('CALL_')
    #     print(next(it).argval)
    #     """

    #     # method 2
    #     import sys

    #     # f = inspect.currentframe().f_back # get stack frame of caller (depth=1)
    #     # next op should be STORE_NAME (current op calls the constructor)
    #     opname = dis.opname[f.f_code.co_code[f.f_lasti + 2]]
    #     # print('opname',opname)
    #     if (
    #         opname == "STORE_NAME" or opname == "STORE_GLOBAL"
    #     ):  # not all objects will be assigned a name
    #         # STORE_NAME argument is the name index
    #         namei = f.f_code.co_code[f.f_lasti + 3]
    #         name = f.f_code.co_names[namei]
    #         # print('is this?', name)
    #         return name
    #     else:
    #         return None

    def table(self, data, column_definition: dict = {}, id: Optional[str] = None):
        """Display a dataframe as an interactive table.

        Parameters
        ----------

        data : pandas.DataFrame
            The data to display.

        column_defination : dict
            define columns

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> import pandas as pd
        >>> data = [
        ...         {'name':'Ikigai', 'author':'Francesc Miralles and Hector Garcia', 'rating':4.3 },
        ...         {'name':'psychology of money', 'author':'Morgan Housel', 'rating':4.5},
        ...         {'name':'Atomic Habits', 'author':'James Clear', 'rating':4.4},
        ...         {'name':'Rework', 'author':"David Heinemeier Hansson and Jason Fried", 'rating':4.5}
                    ]
        >>> df = pd.json_normalize(data)
        >>> ds.table(df)
        """
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "table",
            "prop": {
                "data": json.loads(data.to_json(orient="records")),
                "columns": list(data.columns),
                "column_defination": column_definition,
            },
        }

        print("table data type", type(block["prop"]["data"]))
        if not self.replace_block(id, block):
            self.append_block(block)

    def dataframe(self, data, id: Optional[str] = None):
        """Display dataframe

        Parameters
        ----------

        data : pandas.DataFrame
            The data to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> import pandas as pd
        >>> import numpy as np
        ...
        >>> df = pd.DataFrame(np.random.randn(25,10), columns=("col_%d" % i for i in range(10)))
        ...
        >>> ds.dataframe(df.round(decimals=3))
        """
        if "id" not in data.columns:
            data["id"] = np.arange(data.shape[0])
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "dataframe",
            "prop": {
                "data": json.loads(data.to_json(orient="records")),
                "columns": [
                    {
                        "name": c,
                        "id": c,
                        "field": c,
                        "sortable": True,
                        "minWidth": max(len(c) * 9, 100),
                        "maxWidth": 400,
                        "filterable": True,
                    }
                    for c in list(data.columns)
                ],
                "grid_id": "a" + self.dynamic_widget_id(),
            },
        }
        if not self.replace_block(id, block):
            self.append_block(block)

    def write(self, data, id: Optional[str] = None):
        """
        Write text to the app.

        Parameters
        ----------
        data : str
            text to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        Basic use case

        >>> ds.write('Hello, World!')

        """
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "text",
            "prop": {
                "data": data,
                "data_var": argname("data", vars_only=False, func=self.write),
            },
        }
        if not self.replace_block(id, block):
            self.append_block(block)

    def html(
        self, html: str, allow_unsafe_html: bool = False, id: Optional[str] = None
    ):
        """Diapy html element

        Parameters
        ----------
        html : str
            html string

        allow_unsafe_html : bool
            By default, any HTML tags found in the body will be escaped and therefore treated as pure text. This behavior may be turned off by setting this argument to True.

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.html("<h1>Header</h1>")

        """

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "html",
            "prop": {
                "data": html,
                "data_var": argname("html", vars_only=False, func=self.html),
                "allow_unsafe_html": allow_unsafe_html,
            },
        }
        if not self.replace_block(id, block):
            self.append_block(block)

    def markdown(self, data: str, id: Optional[str] = None):
        """Display markdown text

        Parameters
        ----------

        data : str
            data to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.markdown("**bold text** *itlic text*")
        >>> ds.markdown("# A first-level heading")
        >>> ds.markdown("## A second-level heading")
        >>> ds.markdown("### A third-level heading")

        """
        block = {
            "id": self.dynamic_widget_id(),
            "type": "markdown",
            "prop": {"data": data},
        }
        if not self.replace_block(id, block):
            self.append_block(block)

    def tag(self, data: str):
        """Display tag element

        Parameters
        ----------

        data : str
            text to display inside tag element

        Examples
        --------

        >>> ds.tag('tag1')
        >>> ds.tag('tag2')
        >>> ds.tag('tag3')
        >>> ds.tag('tag4')
        """
        block = {"id": self.dynamic_widget_id(), "type": "tag", "prop": {"data": data}}
        if not self.replace_block(id, block):
            self.append_block(block)

    def cache_data(self, func: callable):
        """Decorator to cache functions that return data

        Parameters
        ----------

        func :  callable
            the function to cache

        Examples
        --------

        >>> @ds.cache_data
        >>> def get_data():
        ...     # fetch data from db
        ...     return 'some_data'
        ...
        >>> get_data()
        """

        def inner1(*args, **kwargs):
            arg_pairs = []
            for arg_idx in range(len(args)):
                arg_name = self._get_positional_arg_name(func, arg_idx)
                arg_pairs.append((arg_name, args[arg_idx]))
            for kw_name, kw_val in kwargs.items():
                arg_pairs.append((kw_name, kw_val))
            args_hasher = hashlib.new("md5")
            for s1, s2 in arg_pairs:
                args_hasher.update(s1.encode())
                args_hasher.update(s2.encode())
            args_hash = args_hasher.hexdigest()

            func_hasher = hashlib.new("md5")
            source_code = inspect.getsource(func)
            func_hasher.update(func.__module__.encode())
            func_hasher.update(func.__qualname__.encode())
            func_hasher.update(source_code.encode())
            func_hash = func_hasher.hexdigest()

            try:
                cache_class = caching.cache_storage[func_hash]

                return_value = cache_class.mem_cache_get(args_hash)

            except:
                return_value = func(*args, **kwargs)
                cache_class = caching.Cache_data(func_hash)
                cache_class.mem_cache_set(args_hash, return_value)
            return return_value

        return inner1

    def _get_positional_arg_name(self, func, arg_index: int) -> str | None:
        """Return the name of a function's positional argument.

        If arg_index is out of range, or refers to a parameter that is not a
        named positional argument (e.g. an *args, **kwargs, or keyword-only param),
        return None instead.
        """
        if arg_index < 0:
            return None

        params: list[inspect.Parameter] = list(
            inspect.signature(func).parameters.values()
        )
        if arg_index >= len(params):
            return None

        if params[arg_index].kind in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.POSITIONAL_ONLY,
        ):
            return params[arg_index].name

        return None

    def editable_html(self, key, id=""):
        default_html = [
            {
                "_id": "5f54d75b114c6d176d7e9765",
                "html": "Heading",
                "tag": "h1",
                "imageUrl": "",
            }
        ]
        file_path = os.path.join(
            Path(os.path.dirname(__file__)).parent.absolute(), "static/app.json"
        )

        try:
            import json

            with open(file_path, "r") as f:
                html = json.loads(f.read())[key]["block"]["prop"]["html"]
        except Exception as e:
            logger.error(e)
            html = default_html
        # if not html:
        #     html = default_html
        logger.info(html)
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "wid": key,
            "type": "editable_html",
            "is_root": True,
            "prop": {"html": html},
        }
        self.append_block(block)

    def sidebar(self):
        """Sidebar"""
        cls = datastack(type="sidebar")
        self.append_block(cls, "sidebar")
        return cls

    def expander(self, name: str):
        """A content area which can be collapsed and expanded.

        Parameters
        ----------

        name : str
            name of the expander

        Examples
        --------

        >>> expander = ds.expander('Expand to view content')
        >>> expander.write('This content will show inside the expander')
        """
        cls = datastack(type="expander", title=name)
        self.append_block(cls)
        return cls

    def columns(self, col_number: int, id: Optional[str] = None):
        """Insert containers laid out as side-by-side columns

        Parameters
        ----------

        col_number : int
            number of columns required

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> col1, col2, col3 = ds.columns(3)
        >>> col1.write('this is col1')
        >>> col2.write('this is col2')
        >>> col3.write('this is col3')
        """
        cols = [datastack(type="column") for x in range(0, col_number)]
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "column",
            "data": cols,
            "prop": {},
        }
        self.append_block(block)
        return cols

    def tabs(self, tab_list: Iterable, id: Optional[str] = None):
        """Insert containers separated into tabs.

        Parameters
        ----------

        tab_list :  iterable
            list of tabs to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> tab1, tab2, tab3 = ds.tabs(["tab1","tab2", "tab3"])
        >>> tab1.header('Tab1')
        >>> tab1.write('this is tab1')
        >>> tab2.header('Tab2')
        >>> tab2.write('this is tab2')
        >>> tab3.header('Tab3')
        >>> tab3.write('this is tab3')
        """
        tab = [
            datastack(type="tab", title=tab_list[x]) for x in range(0, len(tab_list))
        ]
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "tabs",
            "data": tab,
            "prop": {"tabs": tab_list},
        }
        self.append_block(block)
        return tab

    def slider(
        self,
        min: int,
        max: int,
        value: int = None,
        id: Optional[str] = None,
        on_change: Optional[callable] = None,
    ):
        """Display a slider element.

        Parameters
        ----------

        min : int
            minimum value of slider

        max : int
            maximum value of slider

        value : str or None
            The text value of this element when it first renders.

        id : str
            An optional string or integer to use as the unique key for the element.

        on_change : callable
            An option callback invoked when this text input's value chnages.

        Examples
        --------

        >>> ds.slider(min=10, max=100, value=50)
        """
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "slider",
            "prop": {
                "min": min,
                "max": max,
                "value": value,
            },
        }

        try:
            block["prop"]["on_change"] = argname(
                "on_change", vars_only=False, func=self.select
            )
        except:
            print("error on change function")

        try:
            block["prop"]["value_var"] = str(argname("value", vars_only=False))
        except Exception as e:
            print(e)

        if not self.replace_block(id, block):
            self.append_block(block)

    def date_input(
        self,
        label: str = None,
        value: str = None,
        min: str = "1970-01-01",
        max: str = "2500-01-01",
        date_format: str = "yyyy-MM-dd",
        use_container_width: bool = False,
        disabled: bool = False,
        id: Optional[str] = None,
        on_change: Optional[callable] = None,
    ):
        """Display a date input element.

        Parameters
        ----------
        label : str
            A short label explaining to the user what this date input is for.

        value : str
            The value of this widget when it first renders (ex.: 2023-01-01).

        min : str
            The minimum selectable date (ex.: 2023-01-01).

        max : str
            The maximum selectable date (ex.: 2023-01-01).

        date_format : str
            To set the date format (ex.: dd-MMM-yyyy).

        use_container_width : bool
            An optional boolean, which makes the date picker stretch its width to match the parent container.

        disabled : bool
            An optional boolean, which disables the date input if set to True. The default is False.

        id : str
            An optional string or integer to use as the unique key for the element.

        on_change : callable
            An option callback invoked when this text input's value chnages.

        Examples
        --------

        >>> ds.date_input()

        """
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "date_input",
            "prop": {
                "label": label,
                "value": value,
                "date_format": date_format,
                "min": min,
                "max": max,
                "use_container_width": use_container_width,
                "disabled": disabled,
            },
        }

        try:
            block["prop"]["on_change"] = argname(
                "on_change", vars_only=False, func=self.select
            )
        except:
            print("error on change function")

        try:
            block["prop"]["value_var"] = str(argname("value", vars_only=False))
        except Exception as e:
            print(e)

        if not self.replace_block(id, block):
            self.append_block(block)

    def success(self, text: str = None, id: Optional[str] = None):
        """Display an informational message.

        Parameters
        ----------

        text : str
            The success text to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.success('Data saved')
        """

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "success",
            "prop": {
                "value": text,
            },
        }
        self.append_block(block)

    def info(self, text: str = None, id: Optional[str] = None):
        """Display an informational message.

        Parameters
        ----------

        text : str
            The info text to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.info('Data saved')

        """
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "info",
            "prop": {
                "value": text,
            },
        }
        self.append_block(block)

    def warning(self, text: str = None, id: Optional[str] = None):
        """Display an warning message.

        Parameters
        ----------

        text : str
            The info text to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.warning('This is a warning!')

        """

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "warning",
            "prop": {
                "value": text,
            },
        }
        self.append_block(block)

    def error(self, text: str = None, id: Optional[str] = None):
        """Display an error message.

        Parameters
        ----------

        text : str
            The info text to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.error('This is an error!')


        """

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "error",
            "prop": {
                "value": text,
            },
        }
        self.append_block(block)

    def container(self):
        """Insert a multi-element container.

        Examples
        --------

        >>> container = ds.container()
        >>> ds.write('This is outside container')
        ...
        >>> container.write('this is inside container' )
        """
        cls = datastack(type="container")
        self.append_block(cls)
        return cls

    def page(self, path: str):
        """create a new page

        Parameters
        ----------

        path : str
            Path of page

        Examples
        --------

        >>> page1 = ds.page('page1')


        """
        cls = datastack(type="page", path=path)
        self.append_block(cls, "pages")
        return cls

    def code(self, data: str, id: Optional[str] = None):
        """Display code element

        Parameters
        ----------
        data : str
            Code as string to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.code('''def my_function():
        ...     print('my function')''')
        """
        id = id if id else self.dynamic_widget_id()
        block = {
            "id": id,
            "wid": id,
            "type": "code",
            "prop": {"code": data},
        }

        with open(
            os.path.join(
                Path(os.path.dirname(__file__)).parent.absolute(), "static/app.json"
            ),
            "r",
        ) as f:
            import json

            try:
                b = json.loads(f.read())
            except:
                b = {}
        if id in b:
            block["prop"]["code"] = b[id]["block"]["prop"]["code"]
            block["prop"]["last_run_result"] = b[id]["block"]["prop"]["last_run_result"]
        self.append_block(block)
        return ""

    def query(self, data, id=""):
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "query",
            "prop": {"query": data},
        }
        self.append_block(block)
        return ""

    def image(self, data, id: Optional[str] = None):
        """Diaplay an image

        Parameters
        ----------

        data : ImageFile
            image data to display

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> import os
        >>> from PIL import Image
        >>> image = Image.open(os.path.join('images', 'image-3.png'))
        >>> ds.image(image)

        """
        import io
        import base64

        if not isinstance(data, io.BytesIO):
            buffered = io.BytesIO()
            data.save(buffered, format=data.format)
        else:
            buffered = data
        img_str = base64.b64encode(buffered.getvalue())
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "image",
            "prop": {"data": "data:image/png;base64, " + img_str.decode("utf-8")},
        }
        if not self.replace_block(id, block):
            self.append_block(block)

    def pyplot(self, fig):
        """Display a matplotlib.pyplot figure.

        Parameters
        ----------
        fig : Matplotlib Figure
            The figure to plot.

        Examples
        --------
        >>> import numpy as np
        >>> ds.subheader('PyPlot')
        >>> arr = np.random.normal(1, 1, size=100)
        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> ax.hist(arr, bins=20)
        >>> ds.pyplot(fig)
        """
        import io

        image = io.BytesIO()
        fig.savefig(image)
        self.image(image)

    def iframe(self, url: str, id: Optional[str] = None):
        """Display iframe element

        Parameters
        ----------

        url : str
            url for iframe

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> ds.subheader('Iframe')
        ...
        >>> url = 'https://www.wikipedia.org/'
        >>> ds.iframe(url)

        """
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "iframe",
            "prop": {
                "url": url,
                "url_var": argname("url", vars_only=False, func=self.iframe),
            },
        }
        if not self.replace_block(id, block):
            self.append_block(block)

    def chart(
        self, data, on_click: Optional[callable] = None, id: Optional[str] = None
    ):
        """Display plotly chart

        Parameters
        ----------

        data : plotly data
            plotly fig object to display chart

        id : str
            An optional string or integer to use as the unique key for the element.

        Examples
        --------

        >>> import plotly.express as px
        ...
        >>> data_canada = px.data.gapminder().query("country == 'Canada'")
        >>> fig = px.bar(data_canada, x='year', y='pop')
        ...
        >>> ds.subheader('Charts')
        >>> ds.chart(fig)

        >>> import plotly.express as px
        ...
        >>> df = px.data.tips()
        ...
        >>> fig = px.box(df, x="day", y="total_bill", facet_row="smoker")
        >>> fig.update_traces(quartilemethod="exclusive", alignmentgroup='df', offsetgroup='offset')
        >>> fig.update_layout(boxmode='group')
        ...
        >>> ds.chart(fig)
        """
        import json
        import plotly.tools

        fig = plotly.tools.return_figure_from_figure_or_data(data, validate_figure=True)
        # fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "chart",
            "prop": {
                "data": fig,
                "data_var": argname("data", vars_only=False, func=self.chart),
            },
        }

        try:
            block["prop"]["on_change"] = argname("on_click")
        except:
            pass

        if not self.replace_block(id, block):
            self.append_block(block)

    def chart_builder(self, id=""):
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "chart_builder",
            "prop": {},
        }
        self.append_block(block)

    def get_all_dfs(self):
        import pandas as pd
        import itertools

        self.app["appstate"]["dfs"] = [
            attr[0]
            for attr in inspect.getmembers(runtime.get_module())
            if isinstance(attr[1], pd.DataFrame)
        ]
        self.app["appstate"]["columns"] = list(
            itertools.chain(
                *[
                    [attr[0] + "." + str(col) for col in attr[1].columns.tolist()]
                    for attr in inspect.getmembers(runtime.get_module())
                    if isinstance(attr[1], pd.DataFrame)
                ]
            )
        )

    def update_app_state(self, key, value):
        self.state[key] = value

    def page_link(self, page_name, id=""):
        block = {
            "id": id if id else self.dynamic_widget_id(),
            "type": "page_link",
            "prop": {"data": page_name, "on_change": "load_page"},
        }
        self.append_block(block)

    def set_page(self, page_name: str):
        """Set which page to display

        Parameters
        ----------
        page_name : str
            page name

        Examples
        --------

        >>> ds.set_page('page1')
        """
        self.app["current_page"] = page_name

    def sql_connection(self, params):
        return SQLConnection(params)

    def append_block(self, block, location="main_page"):
        self.blocks[location].append(block)

    def get_app_block_by_id(self, id):
        all_app_blocks = [
            block
            for page in ["main_page", "sidebar"] + self.app["pages"]
            for block in self.app[page]
        ]
        return_block = ""

        def check_block_id(blocks, id):
            nonlocal return_block
            for block in blocks:
                if block["type"] == "container" or block["type"] == "expander":
                    check_block_id(block["data"], id)
                elif block["type"] == "column":
                    for col in block["data"]:
                        check_block_id(col, id)
                elif block["type"] == "tabs":
                    for tab in block["data"]:
                        check_block_id(tab["data"], id)
                elif block["id"] == id:
                    return_block = block

        check_block_id(all_app_blocks, id)
        return return_block

        # def check_block_id(blocks, id):
        #     f_blocks = list(filter(lambda p: p["id"] == id, blocks))
        #     if f_blocks:
        #         return f_blocks

        # if blocks:
        #     return blocks

        # else:
        #     print('not found in common')
        #     for b in all_app_blocks:
        #         print('checking for loop')
        #         if b["type"] == "column" or b["type"] == "container" or b["type"] == 'expander':
        #             for b1 in b['data']:
        #                 blocks = list(filter(lambda p: p["id"] == id, b1))
        #                 if blocks:
        #                     return blocks
        #         if b["type"] == "tabs":
        #             print('checking tabs')
        #             for b1 in b['data']:
        #                 blocks = list(filter(lambda p: p["id"] == id, b1['data']))
        #                 if blocks:
        #                     return blocks
        return []

    def gat_all_blocks(self):
        # print(self.blocks)
        # for page in  self.blocks['pages']:
        #     print(self.blocks[page])
        #     for block in self.blocks[page]:
        #         print('bbb---', block)
        return [
            block
            for page in ["main_page"]
            for block in self.blocks[page]
            if isinstance(block, dict)
        ]

    def get_block_by_id(self, id):
        # self.gat_all_blocks()
        try:
            return list(filter(lambda p: p["id"] == id, self.gat_all_blocks()))
        except Exception as e:
            print("error get block by id", e)
            logger.error(e)

    def replace_block(self, id, new_block):
        block = self.get_block_by_id(id)
        # if id == "title":
        #     print("title block", block)
        if block:
            block[0].update(new_block)
            return True
        else:
            return False

    def dump_app(self):
        self.app = {
            "current_page": "main_page",
            "sidebar": [],
            "main_page": [],
            "pages": [],
            "appstate": {"session_id": "default", "notifications": []},
        }
        self.blocks = {"sidebar": [], "main_page": [], "pages": [], "notifications": []}

    def build_element_from_blocks(self, blocks):
        # with parent
        # return [ dict(each_one, **{'parent':x.type}) for each_one in x.blocks['main_page']]

        _app = [
            {"id": "", "type": x.type, "title": x.title, "data": x.blocks["main_page"]}
            if isinstance(x, object)
            and x.__class__.__name__ == "datastack"
            and x.type != "sidebar"
            else x
            for x in blocks
        ]
        # for columns and tabs
        _app = [
            {
                "id": "",
                "type": x["type"],
                "prop": x["prop"],
                "data": [
                    self.build_element_from_blocks(c.blocks["main_page"])
                    for c in x["data"]
                ],
            }
            if x["type"] == "column"
            else x
            for x in _app
        ]
        _app = [
            {
                "id": "",
                "type": x["type"],
                "prop": x["prop"],
                "data": [
                    {
                        "id": "",
                        "type": "tab",
                        "title": c.title,
                        "data": self.build_element_from_blocks(c.blocks["main_page"]),
                    }
                    for c in x["data"]
                ],
            }
            if x["type"] == "tabs"
            else x
            for x in _app
        ]
        _app = [
            {
                "id": "",
                "type": x["type"],
                "data": [
                    {
                        "type": c.__dict__["type"],
                        "data": self.build_element_from_blocks(c.blocks["main_page"]),
                    }
                    if isinstance(c, object) and c.__class__.__name__ == "datastack"
                    else c
                    for c in x["data"]
                ],
            }
            if x["type"] == "container"
            else x
            for x in _app
        ]

        _app = [x if x["type"] == "list" else x for x in _app]
        return _app

    def update_state(self):
        def _update_state(location):
            for c in location:
                try:
                    if (
                        c["type"] == "text"
                        or c["type"] == "html"
                        or c["type"] == "header"
                        or c["type"] == "subheader"
                    ):
                        c["prop"]["data"] = eval(c["prop"]["data_var"])
                    if c["type"] == "date_input" or c["type"] == "input":
                        c["prop"]["value"] = eval(c["prop"]["value_var"])
                    if c["type"] == "button":
                        c["prop"]["title"] = eval(c["prop"]["title_var"])
                    if c["type"] == "select" or c["type"] == "radio_button":
                        c["prop"]["value"] = eval(c["prop"]["value_var"])
                        if "options_var" in c["prop"]:
                            c["prop"]["options"] = [
                                opt for opt in eval(c["prop"]["options_var"])
                            ]
                    if c["type"] == "iframe":
                        c["prop"]["url"] = eval(c["prop"]["url_var"])
                    if c["type"] == "list" or c["type"] == "menu":
                        c["prop"]["value"] = eval(c["prop"]["value_var"])
                    if c["type"] == "chart":
                        # c['prop']['data'] = eval(c['prop']['data_var'])
                        pass
                    if c["type"] == "expander" or c["type"] == "container":
                        _update_state(c["data"])
                    if c["type"] == "column":
                        for col in c["data"]:
                            _update_state(col)
                    if c["type"] == "tabs":
                        for col in c["data"]:
                            _update_state(col["data"])
                    if c["type"] == "editable_html":
                        default_html = [
                            {
                                "_id": "5f54d75b114c6d176d7e9765",
                                "html": "Heading",
                                "tag": "h1",
                                "imageUrl": "",
                            }
                        ]
                        try:
                            import json

                            with open(
                                os.path.join(
                                    Path(os.path.dirname(__file__)).parent.absolute(),
                                    "static/app.json",
                                ),
                                "r",
                            ) as f:
                                html = json.loads(f.read())[c["wid"]]["block"]["prop"][
                                    "html"
                                ]
                        except Exception as e:
                            logger.error("update state:" + str(e))
                            html = default_html
                        c["prop"]["html"] = html
                except Exception as e:
                    logger.error("update state:" + str(e))
                    print(c)

        for location in ["main_page", "sidebar"] + self.app["pages"]:
            _update_state(self.app[location])

    def build_app(self):
        # Transfer blocks to app
        # main page
        # _app =  [ self.build_element_from_cls(x) if isinstance(x, object) and x.__class__.__name__ =='datastack' else [x] for x in self.blocks['main_page']]
        # self.app['main_page'] = [item for sublist in _app for item in sublist]
        self.app["main_page"] = self.build_element_from_blocks(self.blocks["main_page"])

        # all pages
        for page in self.blocks["pages"]:
            self.app["pages"].append(page.path)
            # _page = [ x.blocks['main_page'] if isinstance(x, object) and x.__class__.__name__ =='datastack' else [x] for x in page.blocks['main_page']]
            # self.app[page.__dict__['path']] = [item for sublist in _page for item in sublist]
            self.app[page.__dict__["path"]] = self.build_element_from_blocks(
                page.blocks["main_page"]
            )

        #  sidebar
        _app = [
            x.blocks["main_page"]
            if isinstance(x, object) and x.__class__.__name__ == "datastack"
            else [x]
            for x in self.blocks["sidebar"]
        ]
        # # if any class in sidebar
        # # _app = [a[0] for a in _app]
        # _app =  self.build_element_from_blocks(_app)
        # print(_app)
        # self.app['sidebar'] = [ item for sublist in _app for item in sublist]
        t = self.build_element_from_blocks([a[0] for a in _app])
        self.app["sidebar"] = t
        self.app["pages"] = np.unique(np.array(self.app["pages"])).tolist()
        return self.app

    def rerun(self, my_vars={}, old_app=""):

        for k, v in my_vars.items():
            globals()[k] = v
        # print({k: v for k, v in globals().items() if not k.startswith("__")})
        self.build_app()
        self.update_state()
        # old_app = self.app.copy()

        # diff = [x for x in self.app if x not in old_app else x]
        # diff = [x.update(is_change=True) if x not in old_app else x for x in self.app]
        # diff = [{**x, 'is_change':True} if x  not in old_app else {**x, 'is_change':False}  for x in self.app ]
        # print(self.app)
        return self.app
