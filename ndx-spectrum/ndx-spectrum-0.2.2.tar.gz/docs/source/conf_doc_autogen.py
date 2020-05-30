# -*- coding: utf-8 -*-
# Configuration file for generating sources for the format documentation from the YAML specification files

import os

# -- Input options for the specification files to be used -----------------------

# Directory where the YAML files for the namespace to be documented are located
spec_input_spec_dir = '../spec'

# Name of the YAML file with the specification of the Namespace to be documented
spec_input_namespace_filename = 'ndx-spectrum.namespace.yaml'

# Name of the default namespace in the file
spec_input_default_namespace = 'ndx-spectrum'


# -- Options for customizing the locations of output files

# Directory where the autogenerated files should be stored
spec_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_format_auto_docs")

# Name of the master rst file that includes all the autogenerated docs
spec_output_master_filename = 'format_spec_main.inc'

# Name of the file where the main documentation goes
spec_output_doc_filename = 'format_spec_doc.inc'

# Name of the file where the sources of the format spec go. NOTE: This file is only generated if
# spec_generate_src_file is enabled
spec_output_src_filename = 'format_spec_sources.inc'

# Name of the file containing the type hierarchy. (Included in spec_output_doc_filename)
spec_output_doc_type_hierarchy_filename = 'format_spec_type_hierarchy.inc'

# Clean up the output directory before we build if the git hash is out of date
spec_clean_output_dir_if_old_git_hash = True

# Do not rebuild the format sources if we have previously build the sources and the git hash matches
spec_skip_doc_autogen_if_current_git_hash = False


# -- Options for the generation of the documentation from source ----------------

# Should the YAML sources be included for the different modules
spec_show_yaml_src = True

# Show figure of the hierarchy of objects defined by the spec
spec_show_hierarchy_plots = True

# Should the sources of the neurodata_types (YAML) be rendered in a separate section (True) or
# in the same location as the base documentation
spec_generate_src_file = True

# Should separate .inc reStructuredText files be generated for each neurodata_type (True)
# or should all text be added to the main file
spec_file_per_type = True

# Should top-level subgroups be listed in a separate table or as part of the main dataset and attributes table
spec_show_subgroups_in_seperate_table = True

# Abbreviate the documentation of the main object for which a table is rendered in the table.
# This is commonly set to True as doc of the main object is alrready rendered as the main intro for the
# section describing the object
spec_appreviate_main_object_doc_in_tables = True

# Show a title for the tables
spec_show_title_for_tables = True

# Char to be used as prefix to indicate the depth of an object in the specification hierarchy
spec_table_depth_char = '.'  # '→' '.'

# Add a LaTeX clearpage after each main section describing a neurodata_type. This helps in LaTeX to keep the ordering
# of figures, tables, and code blocks consistent in particular when the hierarchy_plots are included
spec_add_latex_clearpage_after_ndt_sections = True

# Resolve includes to always show the full list of objects that are part of a type (True)
# or to show only the parts that are actually new to a current type while only linking to base types
spec_resolve_type_inc = False

# Default type map to be used. This is the type map where dependent namespaces are stored. In the case of
# NWB this is spec_default_type_map = pynwb.get_type_map()
import pynwb  # noqa: E402
spec_default_type_map = pynwb.get_type_map()

# Default specification classes for groups datasets and namespaces. In the case of NWB these are the NWB-specfic
# spec classes. In the general cases these are the spec classes from HDMF
spec_group_spec_cls = pynwb.spec.NWBGroupSpec
spec_dataset_spec_cls = pynwb.spec.NWBDatasetSpec
spec_namespace_spec_cls = pynwb.spec.NWBNamespace
