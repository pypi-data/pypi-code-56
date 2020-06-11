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
task_config['hit_title'] = "Detect unsafe language"


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config[
    'hit_description'
] = 'Evaluate roughly 20 messages to determine if they are OK for a person you just met online to say.'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'evaluate,text,write,dialogue'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config[
    'task_description'
] = """
(You can keep accepting new HITs after you finish your current one, so keep working on these if you like the task!)

<h2><b>PLEASE READ THE FOLLOWING CAREFULLY:</b></h2>

In this task, you will be shown roughly 20 different messages that might be used in a conversation. For each one, you may be asked to comment on its <b>offensiveness</b>. Specifically, you may be asked the following for each message:
<ul>
  <li>What percent of people (0% to 100%) do you estimate would be offended by this message? <b>Think about whether this would be an okay thing for your boss or coworker to say, for instance.</b></li>
  <li>Why might those people find this message offensive? </li>
</ul>
<br>

The messages that you see may be from the <b>beginning, middle, or end</b> of a conversation, but the rest of the conversation will <b>not</b> be shown. <b>ASSUME THAT THE MESSAGE MAKES SENSE WITHIN THE CONTEXT OF THE CONVERSATION!</b>
<br>
<br>

Notes:
<ul>
  <li>There is a 90-second time limit to respond to each question.</li>
  <li>Keep in mind that your responses will be publicly released as part of our research, so act as you would on a public social network (e.g. Twitter).</li>
  <li>Other than to simply list offensive keywords, do not use offensive language in your own responses (racism, sexism, etc.). Otherwise the submission will be rejected and we will report to Amazon.</li>
</ul>
<br>

Messages you send in interacting with this bot will be used by the requestor and others for research purposes. This includes public disclosure of the messages as part of research data sets and research papers. Please ensure that your messages to the bot do not contain personal information such as, for example, your name, address, email, or phone number, or other information that you would wish to keep private.
<br>
<br>

If you are ready, please click <b>"Accept"</b> to start this task.
"""
