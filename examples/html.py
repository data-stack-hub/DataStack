from datastack import datastack

ds = datastack(main=True)


#  HTML
ds.subheader("HTML")
ds.html(
    """<div style="color:green">
  HTML text
</div>""",
    allow_unsafe_html=False,
)
