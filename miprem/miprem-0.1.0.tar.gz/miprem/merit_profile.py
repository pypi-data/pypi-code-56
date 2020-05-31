import json
import os.path as op
import re
from math import floor, ceil
from typing import List, Dict, TextIO

import lxml.etree as et
from cairosvg import svg2png
from colorclass import Color
from terminaltables import SingleTable

PROJECT_PATH = op.dirname(op.abspath(__file__))


class MeritProfile:
    """Represents a merit profile"""

    def __init__(self, input_data: TextIO):
        mp = json.loads(input_data.read())
        if '_question' not in mp:
            raise ValueError('Question not found in input data.')
        self.question: str = mp['_question']

        if '_mentions' not in mp:
            raise ValueError('Mentions not found in input data.')
        self.mentions: List[str] = mp['_mentions']

        [mp.pop(meta_key) for meta_key in ['_mentions', '_question']]
        if len(mp) < 2:
            raise ValueError('There must be at least 2 mentions.')
        if len(mp) > 20:
            raise ValueError('There must be at most 20 mentions.')
        self.proposals_scores: Dict[str, List[int]] = mp
        self.proposals: List[str] = mp.keys()
        self.nb_proposals: int = len(self.proposals)

        if not self.proposals_scores:
            raise ValueError('There is no proposal.')
        scores_sums = [sum(scores) for scores in self.proposals_scores.values()]
        if not all(elem == scores_sums[0] for elem in scores_sums):
            sums = ['%s: %d' % (c, scores_sums[i]) for i, c in enumerate(self.proposals_scores.keys())]
            raise ValueError('The scores sum are not equal for each proposal: %s' % ', '.join([str(s) for s in sums]))

    def __str__(self) -> str:
        str_mj = 'question: %s\n' % self.question
        str_mj += 'mentions: %s\n' % ', '.join(self.mentions)
        str_mj += '\n'.join(['%s: %s' % (name, ', '.join([str(score) for score in scores]))
                             for (name, scores) in self.proposals_scores.items()])
        return str_mj

    def build_svg(self, width: int, height: int, sidebar_width: int, user_css: str) -> bytes:
        ext_border = 5
        int_border = 2
        header_height = 10
        mentions_gap = 3

        if not self.proposals_scores:
            raise IOError('No merit profile has been loaded.')

        with open(op.join(PROJECT_PATH, 'merit_profile.css'), 'r') as css_file:
            css = css_file.read()

        svg = et.Element('svg', version='1.1', xmlns='http://www.w3.org/2000/svg',
                         width=str(width), height=str(height))

        et.SubElement(svg, 'style').text = \
            re.sub(' +', ' ', re.sub(r'/\*.*?\*/', '', ('%s\n%s' % (css, user_css)).replace('\n', ' ')))

        et.SubElement(svg, 'rect', id='background', x='0', y='0', width='100%', height='100%')

        body = et.SubElement(svg, 'svg', id='body', x=str(ext_border), y=str(ext_border),
                             width=str(width - ext_border * 2), height=str(height - ext_border * 2))

        # Note: dominant-baseline / alignment-baseline might be not well supported by some svg renderers, like Intellij.
        header = et.SubElement(body, 'svg', id='header', height='%d%%' % header_height)
        et.SubElement(header, 'text', {'text-anchor': 'middle', 'alignment-baseline': 'middle',
                                       'dominant-baseline': 'middle'}, id='question',
                      x='50%', y='50%').text = self.question

        proposals = et.SubElement(body, 'svg', id='proposals',
                                  y='%d%%' % (header_height + int_border), height='%d%%' % (100 - header_height))

        # TODO: generate colors dynamically
        colors = ['#ff0000', '#ff5500', '#ffaa00', '#ffff00', '#bbff00', '#55ff00', '#00dd00']
        for i_p, (proposal_name, mentions) in enumerate(self.proposals_scores.items()):
            proposal = et.SubElement(proposals, 'svg', {'class': 'proposal'}, id='proposal-%d' % (i_p + 1),
                                     y='%.2f%%' % ((100 / self.nb_proposals) * i_p),
                                     height='%.2f%%' % ((100 / self.nb_proposals) - int_border))

            proposal_ref = et.SubElement(proposal, 'text', {'class': 'proposal-ref', 'alignment-baseline': 'middle',
                                                            'dominant-baseline': 'middle'},
                                         id='proposal-ref-%d' % (i_p + 1), y='50%')
            proposal_ref.text = str(i_p)
            et.SubElement(proposal_ref, 'title').text = proposal_name

            proposal_bar = et.SubElement(proposal, 'svg', {'class': 'proposal-bar'}, id='proposal-bar-%d' % (i_p + 1),
                                         x='%d%%' % sidebar_width, width='%d%%' % (100 - sidebar_width),
                                         viewBox='0 0 %d 1' % (sum(mentions) + mentions_gap * (len(mentions) - 1)),
                                         preserveAspectRatio='none')

            x_offset = 0
            for i_m, mention in enumerate(mentions):
                mention_bar = et.SubElement(proposal_bar, 'rect', fill=colors[len(mentions) - i_m - 1],
                                            x=str(x_offset), width=str(mention), height='1')
                et.SubElement(mention_bar, 'title').text = \
                    '%s got %d voices (%.2f%%) for "%s".' % (proposal_name, mention, 100 * mention / sum(mentions),
                                                             self.mentions[i_m])

                x_offset += mention + mentions_gap

        return et.tostring(svg, pretty_print=True)

    def build_png(self, width: int, height: int, sidebar_width: int, user_css: str) -> bytes:
        svg = self.build_svg(width, height, sidebar_width, user_css)
        return svg2png(bytestring=svg)

    def term_table(self) -> str:
        data = [['proposal'] + self.mentions]
        for proposal, scores in self.proposals_scores.items():
            proposal_row = [Color('{blue}%s{/blue}' % proposal).value_colors]
            for i, score in enumerate(scores):
                if floor((i+1) / len(self.mentions) * 3) == 0:
                    proposal_row += [Color('{red}%s{/red}' % str(score)).value_colors]
                elif ceil(i / len(self.mentions) * 3) == 3:
                    proposal_row += [Color('{green}%s{/green}' % str(score)).value_colors]
                else:
                    proposal_row += [Color('{yellow}%s{/yellow}' % str(score)).value_colors]
            data.append(proposal_row)
        table = SingleTable(data, title=Color('  {cyan}%s{/cyan}  ' % self.question).value_colors)
        return table.table
