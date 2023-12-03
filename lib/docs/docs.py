from datastack import datastack
import inspect, types

# import stoutput
from docutils.core import publish_parts
from docutils.parsers.rst import directives
import pandas as pd

ds = datastack(main=True)


prefix = "ds"
obj = ds


def generate_doc():
    membername = ds.state["selected_menu"]
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
    ds.html(short_description, id="s_d")
    ds.html(long_description, id="l_d")

    ds.subheader("Function signature", id="fn_sig")
    # sing_container = ds.container()
    signature = f"{prefix}.{membername}({arguments})"
    ds.list([signature], id="sig")
    if len(details["args"]) > 0:
        ds.subheader("Parameters", id="param")

        # for arg in details['args']:
        #     ds.write(arg['name'], id='params_name')
        #     ds.write(arg['description'], id='desc')
        ds.table(
            pd.DataFrame.from_dict(details["args"]),
            column_definition={"description": "html"},
            id="arg_table",
        )
    else:
        ds.table(pd.DataFrame.from_dict({}), id="arg_table")
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
                # collapsed = "\n".join(line.lstrip() for line in numpydoc_obj["Examples"])
                print(numpydoc_obj["Examples"])
                print(collapsed)
                import html

                details["examples"] = strip_code_prompts(parse_rst(collapsed))
                ds.subheader("Example")
                ds.html(details["examples"])
                from pathlib import Path

                code = collapsed  # .replace(">>> ",'')
                # sourcefile = "v1.py"
                # Path(sourcefile).write_text(code)
                # compiled = compile(code, sourcefile, mode="exec")
                # exec(compiled)
        except Exception as e:
            print(e)


def strip_code_prompts(rst_string):
    """Removes >>> and ... prompts from code blocks in examples."""
    return (
        rst_string.replace("&gt;&gt;&gt; ", "")
        .replace("&gt;&gt;&gt;\n", "\n")
        .replace("\n... ", "\n")
        .replace("\n...", "\n")
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

selected_menu = ds.sidebar().menu(
    [m for m in dir(obj) if not m.startswith("_")],
    value="write",
    on_change=generate_doc,
)
ds.header(selected_menu)
# for membername in dir(obj):
#     member = getattr(obj, membername)
#     print('member', membername)
# print(getattr(obj, "__doc__", ""))
# print(getattr(member, "__doc__", ""))
