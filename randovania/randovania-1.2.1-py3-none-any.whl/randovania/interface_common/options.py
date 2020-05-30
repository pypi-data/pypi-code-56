import dataclasses
import json
from distutils.version import StrictVersion
from pathlib import Path
from typing import Optional, TypeVar, Callable, Any

from randovania.interface_common import persistence, update_checker
from randovania.interface_common.cosmetic_patches import CosmeticPatches
from randovania.interface_common.echoes_user_preferences import EchoesUserPreferences
from randovania.interface_common.persisted_options import get_persisted_options_from_data, serialized_data_for_options

T = TypeVar("T")


def identity(v: T) -> T:
    return v


@dataclasses.dataclass(frozen=True)
class Serializer:
    encode: Callable[[Any], Any]
    decode: Callable[[Any], Any]


_SERIALIZER_FOR_FIELD = {
    "last_changelog_displayed": Serializer(identity, str),
    "advanced_validate_seed_after": Serializer(identity, bool),
    "advanced_timeout_during_generation": Serializer(identity, bool),
    "auto_save_spoiler": Serializer(identity, bool),
    "output_directory": Serializer(str, Path),
    "selected_preset_name": Serializer(identity, str),
    "cosmetic_patches": Serializer(lambda p: p.as_json, CosmeticPatches.from_json_dict),
}


def _return_with_default(value: Optional[T], default_factory: Callable[[], T]) -> T:
    """
    Returns the given value is if it's not None, otherwise call default_factory
    :param value:
    :param default_factory:
    :return:
    """
    if value is None:
        return default_factory()
    else:
        return value


class DecodeFailedException(ValueError):
    pass


class Options:
    _data_dir: Path
    _on_options_changed: Optional[Callable[[], None]] = None
    _nested_autosave_level: int = 0
    _is_dirty: bool = False

    _last_changelog_displayed: str
    _advanced_validate_seed_after: Optional[bool] = None
    _advanced_timeout_during_generation: Optional[bool] = None
    _auto_save_spoiler: Optional[bool] = None
    _output_directory: Optional[Path] = None
    _selected_preset_name: Optional[str] = None
    _cosmetic_patches: Optional[CosmeticPatches] = None

    def __init__(self, data_dir: Path):
        self._data_dir = data_dir
        self._last_changelog_displayed = str(update_checker.strict_current_version())

    @classmethod
    def with_default_data_dir(cls) -> "Options":
        return cls(persistence.user_data_dir())

    def _read_persisted_options(self) -> Optional[dict]:
        try:
            with self._data_dir.joinpath("config.json").open() as options_file:
                return json.load(options_file)
        except FileNotFoundError:
            return None

    def _set_field(self, field_name: str, value):
        setattr(self, "_" + field_name, value)

    def load_from_disk(self, ignore_decode_errors: bool = False) -> bool:
        """
        Loads the file created with `_save_to_disk`.
        :param ignore_decode_errors: If True, errors in the config file are ignored.
        :return: True, if a valid file exists.
        """
        try:
            persisted_data = self._read_persisted_options()

        except json.decoder.JSONDecodeError as e:
            if ignore_decode_errors:
                persisted_data = None
            else:
                raise DecodeFailedException(f"Unable to decode JSON: {e}")

        if persisted_data is None:
            return False

        persisted_options = get_persisted_options_from_data(persisted_data)
        self.load_from_persisted(persisted_options, ignore_decode_errors)
        return True

    def load_from_persisted(self,
                            persisted: dict,
                            ignore_decode_errors: bool,
                            ):
        """
        Loads fields from the given persisted options.
        :param persisted:
        :param ignore_decode_errors:
        :return:
        """
        for field_name, serializer in _SERIALIZER_FOR_FIELD.items():
            value = persisted.get(field_name, None)
            if value is not None:
                try:
                    decoded = serializer.decode(value)
                except Exception as err:
                    if ignore_decode_errors:
                        decoded = None
                    else:
                        raise DecodeFailedException(
                            f"Unable to decode field {field_name}: {err}"
                        )

                if decoded is not None:
                    self._set_field(field_name, decoded)

    def _serialize_fields(self) -> dict:
        data_to_persist = {}
        for field_name, serializer in _SERIALIZER_FOR_FIELD.items():
            value = getattr(self, "_" + field_name, None)
            if value is not None:
                data_to_persist[field_name] = serializer.encode(value)

        return serialized_data_for_options(data_to_persist)

    def _save_to_disk(self):
        """Serializes the fields of this Option and writes then to a file."""
        self._is_dirty = False
        data_to_persist = self._serialize_fields()

        self._data_dir.mkdir(parents=True, exist_ok=True)

        # Write to a separate file, so we don't corrupt the existing one in case we unexpectedly
        # are unable to finish writing the file
        new_config_path = self._data_dir.joinpath("config_new.json")
        with new_config_path.open("w") as options_file:
            json.dump(data_to_persist, options_file,
                      indent=4, separators=(',', ': '))

        # Place the new, complete, config to the desired path
        config_path = self._data_dir.joinpath("config.json")
        new_config_path.replace(config_path)

    def __enter__(self):
        self._nested_autosave_level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._nested_autosave_level == 1:
            if self._is_dirty:
                # TODO: maybe it should be an error to change options to different values in on_options_changed?
                # previous = self._serialize_fields()
                if self._on_options_changed is not None:
                    self._on_options_changed()
                # assert previous == self._serialize_fields()
                self._save_to_disk()
        self._nested_autosave_level -= 1

    # Events
    def _set_on_options_changed(self, value):
        self._on_options_changed = value

    on_options_changed = property(fset=_set_on_options_changed)

    # Reset

    def reset_to_defaults(self):
        self._check_editable_and_mark_dirty()
        self._advanced_validate_seed_after = None
        self._advanced_timeout_during_generation = None
        self._auto_save_spoiler = None
        self._cosmetic_patches = None

    # Files paths
    @property
    def backup_files_path(self) -> Path:
        return self._data_dir.joinpath("backup")

    @property
    def game_files_path(self) -> Path:
        return self._data_dir.joinpath("extracted_game")

    @property
    def tracker_files_path(self) -> Path:
        return self._data_dir.joinpath("tracker")

    @property
    def data_dir(self) -> Path:
        return self._data_dir

    # Access to Direct fields
    @property
    def last_changelog_displayed(self) -> StrictVersion:
        return StrictVersion(self._last_changelog_displayed)

    @last_changelog_displayed.setter
    def last_changelog_displayed(self, value: StrictVersion):
        if value != self.last_changelog_displayed:
            self._check_editable_and_mark_dirty()
            self._last_changelog_displayed = str(value)

    @property
    def output_directory(self) -> Optional[Path]:
        return self._output_directory

    @output_directory.setter
    def output_directory(self, value: Optional[Path]):
        self._edit_field("output_directory", value)
        
    @property
    def auto_save_spoiler(self) -> bool:
        return _return_with_default(self._auto_save_spoiler, lambda: False)
    
    @auto_save_spoiler.setter
    def auto_save_spoiler(self, value: bool):
        self._edit_field("auto_save_spoiler", value)

    @property
    def selected_preset_name(self) -> Optional[str]:
        return self._selected_preset_name

    @selected_preset_name.setter
    def selected_preset_name(self, value: str):
        self._edit_field("selected_preset_name", value)

    @property
    def cosmetic_patches(self) -> CosmeticPatches:
        return _return_with_default(self._cosmetic_patches, CosmeticPatches.default)

    # Advanced

    @property
    def advanced_validate_seed_after(self) -> bool:
        return _return_with_default(self._advanced_validate_seed_after, lambda: True)

    @advanced_validate_seed_after.setter
    def advanced_validate_seed_after(self, value: bool):
        self._check_editable_and_mark_dirty()
        self._advanced_validate_seed_after = value

    @property
    def advanced_timeout_during_generation(self) -> bool:
        return _return_with_default(self._advanced_timeout_during_generation, lambda: True)

    @advanced_timeout_during_generation.setter
    def advanced_timeout_during_generation(self, value: bool):
        self._check_editable_and_mark_dirty()
        self._advanced_timeout_during_generation = value

    # Access to fields inside CosmeticPatches
    @property
    def hud_memo_popup_removal(self) -> bool:
        return self.cosmetic_patches.disable_hud_popup

    @hud_memo_popup_removal.setter
    def hud_memo_popup_removal(self, value: bool):
        self._edit_field("cosmetic_patches",
                         dataclasses.replace(self.cosmetic_patches, disable_hud_popup=value))

    @property
    def speed_up_credits(self) -> bool:
        return self.cosmetic_patches.speed_up_credits

    @speed_up_credits.setter
    def speed_up_credits(self, value: bool):
        self._edit_field("cosmetic_patches",
                         dataclasses.replace(self.cosmetic_patches, speed_up_credits=value))

    @property
    def open_map(self) -> bool:
        return self.cosmetic_patches.open_map

    @open_map.setter
    def open_map(self, value: bool):
        self._edit_field("cosmetic_patches",
                         dataclasses.replace(self.cosmetic_patches, open_map=value))

    @property
    def pickup_markers(self) -> bool:
        return self.cosmetic_patches.pickup_markers

    @pickup_markers.setter
    def pickup_markers(self, value: bool):
        self._edit_field("cosmetic_patches",
                         dataclasses.replace(self.cosmetic_patches, pickup_markers=value))

    @property
    def user_preferences(self) -> EchoesUserPreferences:
        return self.cosmetic_patches.user_preferences

    @user_preferences.setter
    def user_preferences(self, value: EchoesUserPreferences):
        self._edit_field("cosmetic_patches",
                         dataclasses.replace(self.cosmetic_patches, user_preferences=value))

    ######

    def _check_editable_and_mark_dirty(self):
        """Checks if _nested_autosave_level is not 0 and marks at least one value was changed."""
        assert self._nested_autosave_level != 0, "Attempting to edit an Options, but it wasn't made editable"
        self._is_dirty = True

    def _edit_field(self, field_name: str, new_value):
        current_value = getattr(self, field_name)
        if current_value != new_value:
            self._check_editable_and_mark_dirty()
            self._set_field(field_name, new_value)
