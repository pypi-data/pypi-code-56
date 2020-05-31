from fanstatic import Library, Resource

library = Library('js.ace', 'resources')

ace = Resource(library, 'ace.js')

# All resources from ace-build subdir "src-min-noconflict" are copied into
# this packge, but only top-level resources are defined as Resource objects.
# Load the extra mode/keybindings/themes/workers in javascript using
# ace.require().
