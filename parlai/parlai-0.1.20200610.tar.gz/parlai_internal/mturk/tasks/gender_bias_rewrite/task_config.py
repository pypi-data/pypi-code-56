#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

task_config = {}


task_config['frontend_version'] = 1

"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = 'Rewrite conversational messages'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config[
    'hit_description'
] = 'Rewrite conversational messages so that most people could guess the gender of the person you are speaking to or about.'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'evaluate'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config[
    'task_description'
] = """
In this task, you'll need to evaluate 5 messages.<br><br>

<h2><b>PLEASE READ THE FOLLOWING CAREFULLY:</b></h2>
For each message you will be asked to rewrite conversational messages such that
most people would guess the message is either <b>spoken by</b>, <b>spoken to</b>,
or <b>about</b> a <b><span style='color:purple'>MAN</span></b> or a <b><span style='color:green'>WOMAN</span></b>.
<br>
<br>
Afterwards, you will be asked how <b>sure you would be</b> that the message you just wrote is is either <b>spoken by</b>, <b>spoken to</b>,
or <b>about</b> a <b><span style='color:purple'>MAN</span></b> or a <b><span style='color:green'>WOMAN</span></b>.
<br>
<br>
<b>EXAMPLE:</b> Rewrite: <i>Hey how are you today? Just got back from work.</i>
<ul>
  <li><b>Spoken <span style='color:blue'>TO</span> a <span style='color:green'>WOMAN</span></b>: Hey, how are you today, Melissa?  Just got back from work.</li>
  <b>Confidence level: PRETTY SURE</b><i> (Melissa is usually a name used by women.) </i> <br><br>
  <li><b>Spoken <span style='color:blue'>ABOUT</span> a <span style='color:green'>WOMAN</span></b>: Hey, how are you today? Did you see her show?</li>
  <b>Confidence level: CERTAIN</b> <i> (You use the word HER when you talk about a woman.)</i> <br><br>
  <li><b>Spoken <span style='color:blue'>BY</span> a <span style='color:green'>WOMAN</span></b>: Hey, how are you today? Just got back from work at the hair salon.</li>
  <b>Confidence level: PRETTY SURE</b> <i> (Statistically, more women work in hair salons, so it is probably about a woman.)</i> <br><br>
  <li><b>Spoken <span style='color:blue'>TO</span> a <span style='color:purple'>MAN</span></b>: Hi, how are you today, sir? Just got back from work. </li>
  <b>Confidence level: CERTAIN</b><i> (Men are addressed with SIR. ) </i> <br><br>
  <li><b>Spoken <span style='color:blue'>ABOUT</span> a <span style='color:purple'>MAN</span></b>: Hey, how are you today? Just got back from Mark's house. </li>
  <b>Confidence level: PRETTY SURE</b> <i> (Most people named Mark are men.)</i> <br><br>
  <li><b>Spoken <span style='color:blue'>BY</span> a <span style='color:purple'>MAN</span></b>: Hey, how are you today? Just got back from football practice.</li>
  <b>Confidence level: PRETTY SURE</b> <i> (More men play football, so most people would guess a man said this.)</i> <br><br>
</ul>
<br>

If you are ready, please click "Accept HIT" to start this task.
"""
