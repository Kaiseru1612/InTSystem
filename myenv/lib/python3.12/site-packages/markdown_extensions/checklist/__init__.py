"""
    import markdown
    from markdowns.extensions.checklist.extension import ChecklistExtension
    html = markdown.markdown(source, extensions=[ChecklistExtension()])
"""

from .extension import makeExtension

