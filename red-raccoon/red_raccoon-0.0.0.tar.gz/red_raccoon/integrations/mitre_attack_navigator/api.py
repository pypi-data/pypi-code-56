import logging

import hodgepodge.helpers
import red_raccoon.log as log

from hodgepodge.helpers import ensure_type

from red_raccoon.integrations.mitre_attack import DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_PATH, \
    DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_URL

from red_raccoon.integrations.mitre_attack.api import MitreAttack

from red_raccoon.integrations.mitre_attack_evaluations import DEFAULT_MITRE_ATTACK_EVALUATIONS_DIRECTORY, \
    DEFAULT_MITRE_ATTACK_EVALUATIONS_SCREENSHOTS_DIRECTORY

from red_raccoon.integrations.mitre_attack_evaluations.api import MitreAttackEvaluations

from red_raccoon.integrations.mitre_attack_navigator import MITRE_ATTACK_ENTERPRISE, MITRE_ATTACK_MOBILE, \
    DEFAULT_LAYER_NAME, DEFAULT_LAYER_DOMAIN, DEFAULT_LAYER_DESCRIPTION, DEFAULT_LAYER_VERSION, DEFAULT_COLOR, \
    DEFAULT_COLOR_FOR_TECHNIQUES_ONLY_IN_FIRST_LAYER, DEFAULT_COLOR_FOR_TECHNIQUES_ONLY_IN_SECOND_LAYER, \
    DEFAULT_COLOR_FOR_TECHNIQUES_IN_BOTH_LAYERS, DEFAULT_MINIMUM_COLOR_FOR_GRADIENT, \
    DEFAULT_MAXIMUM_COLOR_FOR_GRADIENT, SUPPORTED_LAYER_DOMAINS, \
    IN_SCOPE_MITRE_ATTACK_ENTERPRISE_TACTIC_IDS_FOR_MITRE_ATTACK_EVALUATIONS, DEFAULT_COLOR_FOR_DETECTED_TECHNIQUES, \
    DEFAULT_COLOR_FOR_UNDETECTED_TECHNIQUES, DEFAULT_COLOR_FOR_UNTESTED_TECHNIQUES

from red_raccoon.integrations.mitre_attack_navigator.types import Layer, Technique, Gradient

logger = logging.getLogger(__name__)


class MitreAttackNavigator:
    def __init__(self, mitre_attack_enterprise_stix_data=None,
                 mitre_attack_enterprise_stix_data_path=DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_PATH,
                 mitre_attack_enterprise_stix_data_url=DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_URL,
                 mitre_attack_evaluations_directory=DEFAULT_MITRE_ATTACK_EVALUATIONS_DIRECTORY,
                 mitre_attack_evaluations_screenshot_directory=DEFAULT_MITRE_ATTACK_EVALUATIONS_SCREENSHOTS_DIRECTORY):

        self.mitre_attack_api = MitreAttack(
            enterprise_stix_data=mitre_attack_enterprise_stix_data,
            enterprise_stix_data_path=mitre_attack_enterprise_stix_data_path,
            enterprise_stix_data_url=mitre_attack_enterprise_stix_data_url,
        )

        self.mitre_attack_evaluations_api = MitreAttackEvaluations(
            evaluations_directory=mitre_attack_evaluations_directory,
            screenshots_directory=mitre_attack_evaluations_screenshot_directory,
        )

    def get_enterprise_layer_from_evaluation(self, evaluation, output_layer_name=None, output_layer_description=None,
                                             output_layer_version=DEFAULT_LAYER_VERSION,
                                             color_for_detected_techniques=DEFAULT_COLOR_FOR_DETECTED_TECHNIQUES,
                                             color_for_undetected_techniques=DEFAULT_COLOR_FOR_UNDETECTED_TECHNIQUES,
                                             color_for_untested_techniques=DEFAULT_COLOR_FOR_UNTESTED_TECHNIQUES):
        #: Prepare the output layer.
        output_layer_name = output_layer_name or self._get_default_layer_name_from_evaluation(evaluation)
        output_layer_description = output_layer_description or self._get_default_layer_description_from_evaluation(evaluation)

        hint = log.get_hint(
            vendor_names=evaluation.vendor_name,
            group_names=evaluation.group_name,
            output_layer_name=output_layer_name,
            output_layer_version=output_layer_version,
        )
        log.info(logger, "Translating MITRE ATT&CK Evaluation into MITRE ATT&CK Navigator layer", hint=hint)

        layer = Layer(
            name=output_layer_name,
            description=output_layer_description,
            version=output_layer_version,
            domain=MITRE_ATTACK_ENTERPRISE,
        )

        #: Lookup all techniques.
        all_techniques = self.mitre_attack_api.get_enterprise_techniques()
        all_technique_ids = {t.external_id for t in all_techniques}

        #: Lookup all techniques related to the specified group.
        related_techniques = self.mitre_attack_api.get_enterprise_techniques(
            tactic_ids=IN_SCOPE_MITRE_ATTACK_ENTERPRISE_TACTIC_IDS_FOR_MITRE_ATTACK_EVALUATIONS,
            group_names=[evaluation.group_name],
        )
        related_technique_ids = {t.external_id for t in related_techniques}

        #: Add any detected techniques.
        detected_techniques = evaluation.detected_techniques
        if detected_techniques:
            for technique in detected_techniques:
                technique = self.get_technique(technique_id=technique.id, color=color_for_detected_techniques)
                layer.add_technique(technique)

        #: Add any undetected techniques.
        undetected_techniques = evaluation.undetected_techniques
        if undetected_techniques:
            for technique in undetected_techniques:
                technique = self.get_technique(technique_id=technique.id, color=color_for_undetected_techniques)
                layer.add_technique(technique)

        #: Add any untested techniques.
        untested_technique_ids = related_technique_ids - set(layer.technique_ids)
        if untested_technique_ids:
            for technique_id in untested_technique_ids:
                technique = self.get_technique(technique_id=technique_id, color=color_for_untested_techniques)
                layer.add_technique(technique)

        #: Hide any unrelated techniques.
        unrelated_technique_ids = all_technique_ids - set(layer.technique_ids)
        if unrelated_technique_ids:
            for technique_id in unrelated_technique_ids:
                technique = self.get_technique(technique_id=technique_id, enabled=False)
                layer.add_technique(technique)

        return layer

    def _get_default_layer_name_from_evaluation(self, evaluation):
        return 'MITRE ATT&CK Evaluation: {} ({})'.format(evaluation.group_name, evaluation.vendor_name)

    def _get_default_layer_description_from_evaluation(self, evaluation):
        return 'This evaluation includes {} observations related to {} techniques across {} ' \
                                     'adversary tactics'.format(len(evaluation.observations),
                                                                len(evaluation.technique_ids),
                                                                len(evaluation.tactic_ids))

    def _get_layer_from_techniques(self, technique_ids=None, technique_names=None, platforms=None,
                                   name=DEFAULT_LAYER_NAME, domain=DEFAULT_LAYER_DOMAIN,
                                   description=DEFAULT_LAYER_DESCRIPTION, version=DEFAULT_LAYER_VERSION,
                                   color=DEFAULT_COLOR, hide_unrelated_techniques=False):
        mitre_attack_query = {
            'technique_ids': technique_ids,
            'technique_names': technique_names,
            'platforms': platforms,
        }
        mitre_attack_query_hint = log.get_hint(**mitre_attack_query)

        layer_configuration = {
            'name': name,
            'description': description,
            'domain': domain,
            'version': version,
            'color': color,
            'hide_unrelated_techniques': hide_unrelated_techniques,
        }
        layer_configuration.update(mitre_attack_query)
        layer_configuration_hint = log.get_hint(**layer_configuration)

        #: Log information about the
        log.info(logger, "Generating a MITRE ATT&CK Navigator layer", hint=layer_configuration_hint)

        #: Lookup the specified techniques.
        if domain == MITRE_ATTACK_ENTERPRISE:
            log.info(logger, "Looking up selected MITRE ATT&CK Enterprise techniques", hint=mitre_attack_query_hint)
            selected_techniques = self.mitre_attack_api.get_enterprise_techniques(**mitre_attack_query)
        elif domain == MITRE_ATTACK_MOBILE:
            log.info(logger, "Looking up selected MITRE ATT&CK Mobile techniques", hint=mitre_attack_query_hint)
            selected_techniques = self.mitre_attack_api.get_mobile_techniques(**mitre_attack_query)
        else:
            raise ValueError("Unsupported domain: %s - supported domains: %s", domain, SUPPORTED_LAYER_DOMAINS)

        #: If no matching techniques were identified, bail out.
        if selected_techniques:
            selected_technique_ids = {t.external_id for t in selected_techniques}
        else:
            log.error(logger, "No matching MITRE ATT&CK techniques found", hint=mitre_attack_query_hint)
            return None

        #: Prepare the output layer.
        layer = self.get_layer(
            name=name,
            description=description,
            version=version,
            hide_disabled=hide_unrelated_techniques,
        )
        techniques = self.get_techniques(technique_ids=selected_technique_ids, color=color, enabled=True)
        layer.add_techniques(techniques)

        #: Lookup all techniques.
        if domain == MITRE_ATTACK_ENTERPRISE:
            all_techniques = self.mitre_attack_api.get_enterprise_techniques()
        else:
            all_techniques = self.mitre_attack_api.get_mobile_techniques()

        all_technique_ids = {t.external_id for t in all_techniques}
        unselected_technique_ids = all_technique_ids - selected_technique_ids

        #: By disabling the technique, it will be 'greyed out' in the resulting layer.
        for technique_id in unselected_technique_ids:
            technique = self.get_technique(technique_id=technique_id, enabled=False)
            layer.add_technique(technique)
        return layer

    def get_layer(self, name=DEFAULT_LAYER_NAME, domain=DEFAULT_LAYER_DOMAIN, description=DEFAULT_LAYER_DESCRIPTION,
                  version=DEFAULT_LAYER_VERSION, hide_disabled=False, gradient=None):
        data = {
            'name': name,
            'domain': domain,
            'description': description,
            'version': version,
            'hide_disabled': hide_disabled,
        }
        if gradient:
            data['gradient'] = gradient
        return hodgepodge.helpers.dict_to_dataclass(data, data_class=Layer)

    def get_technique(self, technique_id, color=DEFAULT_COLOR, comment=None, score=None, enabled=True,
                      tactic_name=None):
        data = {
            'tactic_name': tactic_name,
            'technique_id': technique_id,
            'color': color,
            'comment': comment,
            'score': score,
            'enabled': enabled,
        }
        return hodgepodge.helpers.dict_to_dataclass(data, data_class=Technique)

    def get_techniques(self, technique_ids, color=DEFAULT_COLOR, comment=None, score=None, enabled=True,
                       tactic_name=None):
        techniques = []
        for technique_id in hodgepodge.helpers.as_set(technique_ids, str):
            technique = self.get_technique(
                technique_id=technique_id,
                tactic_name=tactic_name,
                color=color,
                comment=comment,
                score=score,
                enabled=enabled,
            )
            techniques.append(technique)
        return techniques

    def get_gradient(self, colors, min_value, max_value):
        data = {
            'colors': colors,
            'min_value': min_value,
            'max_value': max_value,
        }
        return hodgepodge.helpers.dict_to_dataclass(data, data_class=Gradient)

    def _get_diff(self, first_layer, second_layer, output_layer_name=DEFAULT_LAYER_NAME,
                  output_layer_domain=DEFAULT_LAYER_DOMAIN, output_layer_description=DEFAULT_LAYER_DESCRIPTION,
                  output_layer_version=DEFAULT_LAYER_VERSION,
                  color_for_techniques_only_in_first_layer=DEFAULT_COLOR_FOR_TECHNIQUES_ONLY_IN_FIRST_LAYER,
                  color_for_techniques_only_in_second_layer=DEFAULT_COLOR_FOR_TECHNIQUES_ONLY_IN_SECOND_LAYER,
                  color_for_techniques_in_both_layers=DEFAULT_COLOR_FOR_TECHNIQUES_IN_BOTH_LAYERS):

        techniques_in_first_layer = {t.technique_id for t in ensure_type(first_layer, Layer).techniques}
        techniques_in_second_layer = {t.technique_id for t in ensure_type(second_layer, Layer).techniques}

        techniques_only_in_first_layer = techniques_in_first_layer - techniques_in_second_layer
        techniques_only_in_second_layer = techniques_in_second_layer - techniques_in_first_layer
        techniques_in_both_layers = techniques_in_first_layer & techniques_in_second_layer

        #: Prepare the output layer.
        layer = self.get_layer(
            name=output_layer_name,
            description=output_layer_description,
            domain=output_layer_domain,
            version=output_layer_version,
        )
        for technique_ids, color in (
            (techniques_only_in_first_layer, color_for_techniques_only_in_first_layer),
            (techniques_only_in_second_layer, color_for_techniques_only_in_second_layer),
            (techniques_in_both_layers, color_for_techniques_in_both_layers),
        ):
            techniques = self.get_techniques(technique_ids=technique_ids, color=color)
            layer.add_techniques(techniques)
        return layer

    def get_diff_of_enterprise_layers(self, first_layer, second_layer, output_layer_name=DEFAULT_LAYER_NAME,
                                      output_layer_description=DEFAULT_LAYER_DESCRIPTION,
                                      output_layer_version=DEFAULT_LAYER_VERSION,
                                      color_for_techniques_only_in_first_layer=DEFAULT_COLOR_FOR_TECHNIQUES_ONLY_IN_FIRST_LAYER,
                                      color_for_techniques_only_in_second_layer=DEFAULT_COLOR_FOR_TECHNIQUES_ONLY_IN_SECOND_LAYER,
                                      color_for_techniques_in_both_layers=DEFAULT_COLOR_FOR_TECHNIQUES_IN_BOTH_LAYERS):
        return self._get_diff(
            first_layer=first_layer,
            second_layer=second_layer,
            output_layer_name=output_layer_name,
            output_layer_domain=MITRE_ATTACK_ENTERPRISE,
            output_layer_description=output_layer_description,
            output_layer_version=output_layer_version,
            color_for_techniques_only_in_first_layer=color_for_techniques_only_in_first_layer,
            color_for_techniques_only_in_second_layer=color_for_techniques_only_in_second_layer,
            color_for_techniques_in_both_layers=color_for_techniques_in_both_layers,
        )

    def get_heatmap_from_enterprise_layers(self, layers, gradient_min_color=DEFAULT_MINIMUM_COLOR_FOR_GRADIENT,
                                           gradient_max_color=DEFAULT_MAXIMUM_COLOR_FOR_GRADIENT,
                                           output_layer_name=DEFAULT_LAYER_NAME,
                                           output_layer_description=DEFAULT_LAYER_DESCRIPTION,
                                           output_layer_version=DEFAULT_LAYER_VERSION):
        return self._get_heatmap(
            layers=layers,
            gradient_min_color=gradient_min_color,
            gradient_max_color=gradient_max_color,
            output_layer_name=output_layer_name,
            output_layer_description=output_layer_description,
            output_layer_version=output_layer_version,
            output_layer_domain=MITRE_ATTACK_ENTERPRISE,
        )

    def _get_heatmap(self, layers, gradient_min_color=DEFAULT_MINIMUM_COLOR_FOR_GRADIENT,
                     gradient_max_color=DEFAULT_MAXIMUM_COLOR_FOR_GRADIENT, output_layer_name=DEFAULT_LAYER_NAME,
                     output_layer_domain=DEFAULT_LAYER_DOMAIN, output_layer_description=DEFAULT_LAYER_DESCRIPTION,
                     output_layer_version=DEFAULT_LAYER_VERSION):

        layers = [ensure_type(layer, Layer) for layer in layers]
        if len(layers) < 2:
            raise ValueError("At least two layers are required for comparison.")

        #: Score each technique based on how often it is observed across each of the layers.
        max_score = 0
        scores = {}

        technique_ids = []
        for layer in layers:
            technique_ids.extend(layer.technique_ids)

        for technique_id in technique_ids:
            if technique_id not in scores:
                score = technique_ids.count(technique_id)
                scores[technique_id] = score
                max_score = max(score, max_score)

        #: Prepare the output layer.
        layer = self.get_layer(
            name=output_layer_name,
            description=output_layer_description,
            domain=output_layer_domain,
            version=output_layer_version,
            gradient=self.get_gradient(
                colors=[gradient_min_color, gradient_max_color],
                min_value=0,
                max_value=max_score,
            )
        )
        for technique_id, score in scores.items():
            technique = self.get_technique(technique_id=technique_id, score=score)
            layer.add_technique(technique)
        return layer
