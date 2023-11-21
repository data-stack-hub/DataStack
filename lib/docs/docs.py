
from datastack import datastack
import inspect, types
# import stoutput
from docutils.core import publish_parts
from docutils.parsers.rst import directives

ds = datastack(main=True)

opt = ds.radio_button(['a','b'])
ds.write(opt)



prefix = 'ds'
obj = ds
membername = 'write'
member = getattr(obj, membername)
import docstring_parser
docstring = getattr(member, "__doc__","")
docstring_obj = docstring_parser.parse(docstring)
details ={}

details["args"] = []
for param in docstring_obj.params:
    arg_obj = {}
    arg_obj["name"] = param.arg_name  ## Store the argument name
    arg_obj["type_name"] = param.type_name  # Store the argument type
    arg_obj["is_optional"] = param.is_optional  # Store the optional flag
    arg_obj["description"] = param.description
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
print('args:', details["args"])


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

arguments = get_sig_string_without_annots(ds.write)

ds.header('ds.write')
ds.html(parse_rst(docstring_obj.short_description))
ds.html(parse_rst(docstring_obj.long_description))

ds.subheader('Function signature')
ds.write(f'{prefix}.{membername}({arguments})')
ds.subheader('Parameters')
for arg in details['args']:
     ds.write(arg['name'])
     ds.write(arg['description'])





# for membername in dir(obj):
#     member = getattr(obj, membername)
#     print(getattr(obj, "__doc__", ""))
#     print(getattr(member, "__doc__", ""))