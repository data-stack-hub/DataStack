from datastack import datastack
import inspect, types

# import stoutput
from docutils.core import publish_parts
from docutils.parsers.rst import directives
import pandas as pd
import re, textwrap

ds = datastack(main=True)


prefix = "ds"
obj = ds


def generate_doc():
    details_container.dump_app()

    membername = ds.state["selected_menu"]
    details_container.header(membername)
    member = getattr(obj, membername)
    # print('member', member)
    import docstring_parser

    docstring = getattr(member, "__doc__", "")
    docstring_obj = docstring_parser.parse(docstring)
    # print(docstring_obj)
    details = {}

    details["args"] = []
    for param in docstring_obj.params:
        arg_obj = {}
        arg_obj["name"] = param.arg_name  ## Store the argument name
        arg_obj["type_name"] = param.type_name  # Store the argument type
        arg_obj["is_optional"] = param.is_optional  # Store the optional flag
        arg_obj["description"] = parse_rst(param.description)
        arg_obj["default"] = param.default
        details["args"].append(arg_obj)

    details["returns"] = []
    if type(docstring_obj.returns) is not None:
        for returns in docstring_obj.many_returns:
            return_obj = {}
            return_obj["type_name"] = returns.type_name
            return_obj["is_generator"] = returns.is_generator
            return_obj["description"] = returns.description
            return_obj["return_name"] = returns.return_name
            details["returns"].append(return_obj)
    # print('args:', details["args"])
    arguments = get_sig_string_without_annots(member)

    # ds.header('ds.write')
    short_description = parse_rst(
        ""
        if docstring_obj.short_description is None
        else docstring_obj.short_description
    )
    long_description = parse_rst(
        "" if docstring_obj.long_description is None else docstring_obj.long_description
    )
    details_container.html(short_description, id="s_d")
    details_container.html(long_description, id="l_d")

    details_container.subheader("Function signature", id="fn_sig")
    # sing_container = ds.container()
    signature = f"{prefix}.{membername}({arguments})"
    sig_container = details_container.container()
    sig_container.list([signature], id="sig")
    if len(details["args"]) > 0:
        details_container.subheader("Parameters", id="param")

        # for arg in details['args']:
        #     ds.write(arg['name'], id='params_name')
        #     ds.write(arg['description'], id='desc')
        details_container.table(
            pd.DataFrame.from_dict(details["args"]),
            column_definition={"description": "html"},
            id="arg_table",
        )
    else:
        details_container.table(pd.DataFrame.from_dict({}), id="arg_table")
    # example_container = details_container.container()
    # example_container.write("thi is eampale container")
    if docstring:
        try:
            from numpydoc.docscrape import NumpyDocString

            # Explicitly create the 'Example' section which Streamlit seems to use a lot of.
            NumpyDocString.sections.update({"Example": []})
            numpydoc_obj = NumpyDocString(docstring)

            if "Notes" in numpydoc_obj and len(numpydoc_obj["Notes"]) > 0:
                collapsed = "\n".join(numpydoc_obj["Notes"])
                details["notes"] = parse_rst(collapsed)

            if "Warning" in numpydoc_obj and len(numpydoc_obj["Warning"]) > 0:
                collapsed = "\n".join(numpydoc_obj["Warning"])
                details["warnings"] = parse_rst(collapsed)

            if "Example" in numpydoc_obj and len(numpydoc_obj["Example"]) > 0:
                collapsed = "\n".join(numpydoc_obj["Example"])
                details["example"] = strip_code_prompts(parse_rst(collapsed))

            if "Examples" in numpydoc_obj and len(numpydoc_obj["Examples"]) > 0:
                collapsed = "\n".join(numpydoc_obj["Examples"])
                details["examples"] = strip_code_prompts(parse_rst(collapsed))
                details_container.subheader("Example")
                examples = extract_multiline_examples_from_docstring(docstring)
                for i, example in enumerate(examples, 1):
                    ex1 = (
                        textwrap.dedent(example)
                        .replace("ds", "res")
                        .replace("...", "\n")
                    )
                    details_container.code(textwrap.dedent(example.replace("...", "")))
                    res = details_container.container()
                    import tempfile

                    with tempfile.NamedTemporaryFile(
                        mode="w", suffix=".py", delete=False
                    ) as f:
                        f.write(ex1)
                        sourcefile = f.name
                    globals().update({"res": res})

                    exec(compile(ex1, sourcefile, "exec"), globals())
            # else:
            #     example_container.dump_app()
        except Exception as e:
            print(e)


def extract_multiline_examples_from_docstring(docstring):
    """
    Extract multiline examples from the docstring of a function.

    Args:
        func (function): The function from which to extract examples.

    Returns:
        list: List of multiline example strings.
    """
    # docstring = inspect.getdoc(func)

    if not docstring:
        return []

    examples = []
    current_example = []

    # Use a simple regex to identify lines starting with '>>>'
    example_pattern = re.compile(r"^\s*>>>( .+)?$")
    ellipsis_pattern = re.compile(r"^\s*\.\.\. (.+)$")

    in_example = False

    for line in docstring.splitlines():
        match = example_pattern.match(line)
        if match:
            # Start of a new example
            in_example = True
            if match.group(1) is not None:
                current_example.append(match.group(1))
        elif in_example and line.strip() == "":
            # End of the current example
            examples.append("\n".join(current_example))
            current_example = []
            in_example = False
        elif in_example:
            # Check for lines starting with '...'
            ellipsis_match = ellipsis_pattern.match(line)
            if ellipsis_match:
                current_example.append(ellipsis_match.group(1))
            else:
                # Continue building the current example
                current_example.append(line)

    # Add the last example if there is one
    import textwrap

    if current_example:
        examples.append(textwrap.dedent("\n".join(current_example)).strip())

    return examples


def strip_code_prompts(rst_string):
    """Removes >>> and ... prompts from code blocks in examples."""
    print(rst_string)
    print("------")
    print(
        rst_string.replace("&gt;&gt;&gt; ", "")
        .replace("&gt;&gt;&gt;\n", "\n")
        .replace("\n... ", "\n")
        .replace("\n...", "\n")
        .replace("...", "\n")
    )
    return (
        rst_string.replace("&gt;&gt;&gt; ", "")
        .replace("&gt;&gt;&gt;\n", "\n")
        .replace("\n... ", "\n")
        .replace("\n...", "\n")
        .replace("...", "\n")
    )


def get_sig_string_without_annots(func):
    """Returns a string representation of the function signature without annotations."""
    if not callable(func):
        return ""
    # Check if the function is a bound method
    if isinstance(func, types.MethodType):
        # Get the signature of the function object being bound
        sig = inspect.signature(func.__func__)
    else:
        # Get the signature of the function
        sig = inspect.signature(func)
    # Initialize an empty list to store the arguments
    args = []
    # Initialize a variable to store the previous parameter
    prev = None

    # Iterate through the parameters of the function
    for name, param in sig.parameters.items():
        # Skip the "self" parameter for class methods
        if name == "self":
            prev = param
            continue

        # If there was a previous parameter, check for certain conditions
        if prev:
            # Insert "/" if going from positional_only to anything else
            if (
                prev.kind is prev.POSITIONAL_ONLY
                and param.kind is not param.POSITIONAL_ONLY
            ):
                args.append("/")
                prev_was_positional_only = False

            # Insert "*" if going from something that's not *foo to keyword-only
            if (
                prev.kind not in (prev.VAR_POSITIONAL, prev.KEYWORD_ONLY)
                and param.kind is param.KEYWORD_ONLY
            ):
                args.append("*")

        # If the parameter has a default value, format it accordingly
        if param.default != inspect._empty:
            if type(param.default) is str:
                def_value = f'"{param.default}"'
            elif type(param.default) is type or callable(param.default):
                def_value = f"special_internal_function"
            else:
                def_value = param.default

            args.append(f"{name}={def_value}")

        # If the parameter is a variable positional argument, format it with '*' in front
        elif param.kind is param.VAR_POSITIONAL:
            args.append(f"*{name}")

        # If the parameter is a variable keyword argument, format it with '**' in front
        elif param.kind is param.VAR_KEYWORD:
            args.append(f"**{name}")

        # Otherwise, just append the parameter name
        else:
            args.append(name)

        # Set the current parameter as the previous one for the next iteration
        prev = param

    # Return the formatted argument string
    return ", ".join(args)


def parse_rst(rst_string):
    """Parses RST string to HTML using docutils."""
    docutil_settings = {"embed_stylesheet": 0}
    # Register the custom RST directive for output
    # directives.register_directive("output", stoutput.StOutput)
    # Convert RST string to HTML using docutils
    document = publish_parts(
        rst_string, writer_name="html", settings_overrides=docutil_settings
    )
    return str(document["body"])


# ds.sidebar().list(dir(obj))
# sb = ds.sidebar()
ignor_list = [
    "app",
    "append_block",
    "blocks",
    "build_app",
    "build_element_from_blocks",
    "dump_app",
    "dynamic_widget_id",
    "get_all_blocks",
    "get_all_dfs",
    "get_app_block_by_id",
    "get_block_by_id",
    "main",
    "replace_block",
    "rerun",
    "session_id",
    "type",
    "update_app_state",
    "chart_builder",
    "editable_html",
    "query",
    "page_link",
    "clear_notifications",
    "notification",
    "gat_all_blocks",
    "path",
    "sql_connection",
    "state",
    "update_state",
    "title",
]

menu = [
    {"title": "Input elements", "children": ["button", "radio_button", "date_input"]},
    {"title": "cache_data"},
    {"title": "Chart elements", "children": ["chart", "pyplot"]},
    {
        "title": "Layouts",
        "children": [
            "columns",
            "container",
            "divider",
            "expander",
            "sidebar",
            "topbar",
            "tabs",
        ],
    },
    {"title": "Data elements", "children": ["dataframe", "table", "list"]},
    {"title": "Status elements", "children": ["error", "info", "warning", "success"]},
    {
        "title": "Text elements",
        "children": ["header", "subheader", "html", "markdown", "write"],
    },
    {"title": "Input elements", "children": ["input", "select", "slider", "tag"]},
    {"title": "iframe"},
    {"title": "menu"},
    {"title": "Media elements", "children": ["image"]},
    {"title": "Page", "children": ["page", "set_page"]},
]
selected_menu = ds.sidebar().menu(
    menu,  # [m for m in dir(obj) if not m.startswith("_") and m not in ignor_list],
    value="button",
    on_change=generate_doc,
    mode="inline",
)

details_container = ds.container()
details_container.header("Welcome to DataStack")
details_container.divider()
details_container.subheader("The Fastest way to build apps in python")
details_container.write(
    "Datastack is an open-source framework that enables you to easily build real-time web apps, internal tools, dashboards, weekend projects, data entry forms, or prototypes using just Python no frontend experience required."
)
page1 = ds.page("page1")
page1.header("Page 1")
