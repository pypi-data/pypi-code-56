import os

__version__ = "0.0.3"

class Package:
  def __init__(self):
    self.mods = []

class Mod:
  pass

def package():
  pkg = Package()
  pkg.path = os.path.dirname(__file__)
  pkg.name = os.path.basename(pkg.path)
  pkg.astro_version = "0.1.0"
  pkg.glia_version = "0.1.1"

  #-Generated by Astrocyte v0.1.0
  #-mod_glia__glia_test_mods__cdp5__CR
  mod_glia__glia_test_mods__cdp5__CR = Mod()
  mod_glia__glia_test_mods__cdp5__CR.pkg_name = 'glia_test_mods'
  mod_glia__glia_test_mods__cdp5__CR.asset_name = 'cdp5'
  mod_glia__glia_test_mods__cdp5__CR.variant = 'CR'
  mod_glia__glia_test_mods__cdp5__CR.namespace = 'glia__glia_test_mods'
  mod_glia__glia_test_mods__cdp5__CR._is_point_process = False
  mod_glia__glia_test_mods__cdp5__CR.pkg = pkg
  pkg.mods.append(mod_glia__glia_test_mods__cdp5__CR)
  #-##
  #-Generated by Astrocyte v0.1.0
  #-mod_glia__glia_test_mods__Kir2_3__0
  mod_glia__glia_test_mods__Kir2_3__0 = Mod()
  mod_glia__glia_test_mods__Kir2_3__0.pkg_name = 'glia_test_mods'
  mod_glia__glia_test_mods__Kir2_3__0.asset_name = 'Kir2_3'
  mod_glia__glia_test_mods__Kir2_3__0.variant = '0'
  mod_glia__glia_test_mods__Kir2_3__0.namespace = 'glia__glia_test_mods'
  mod_glia__glia_test_mods__Kir2_3__0._is_point_process = False
  mod_glia__glia_test_mods__Kir2_3__0.pkg = pkg
  pkg.mods.append(mod_glia__glia_test_mods__Kir2_3__0)
  #-##
  return pkg
