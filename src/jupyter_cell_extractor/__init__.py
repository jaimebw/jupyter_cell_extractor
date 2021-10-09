import os
this_dir, _ = os.path.split(__file__)
os.environ["TEMPLATE_TPLX"] = os.path.join(this_dir, "data", "classic.tplx")